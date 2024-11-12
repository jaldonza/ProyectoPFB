import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime

# Definir la función calcular_roi
def calcular_roi(simbolo, fecha_inicio, fecha_fin):
    try:
        # Conexión a la base de datos
        db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",  # Cambia esto por tu usuario de MySQL
            password="11jablum11",  # Cambia esto por tu contraseña de MySQL
            database="yfinance"
        )
        cursor = db_connection.cursor()

        # Consulta SQL para obtener el precio inicial y final en el periodo
        query = """
        SELECT fecha, precio_cierre
        FROM precios_historicos
        WHERE id_empresa = (SELECT id_empresa FROM empresas_sp500 WHERE simbolo = %s)
          AND fecha BETWEEN %s AND %s
        ORDER BY fecha ASC;
        """
        
        cursor.execute(query, (simbolo, fecha_inicio, fecha_fin))
        precios = cursor.fetchall()
        
    except mysql.connector.Error as err:
        st.error(f"Error al conectar a la base de datos: {err}")
        return None, None
    finally:
        # Cerrar conexión
        cursor.close()
        db_connection.close()

    # Verifica si se obtuvieron precios en el rango de fechas
    if len(precios) < 2:
        st.warning("No se encontraron datos suficientes en el rango de fechas seleccionado.")
        return None, None

    # Precio inicial y final
    precio_inicial = precios[0][1]
    precio_final = precios[-1][1]
    
    # Calcular ROI
    roi = (precio_final - precio_inicial) / precio_inicial * 100

    return roi, pd.DataFrame(precios, columns=['Fecha', 'Precio Cierre'])

# Configuración de la aplicación Streamlit
st.set_page_config(page_title="Yahoo Finance app", layout="wide")

# Contenido principal
with st.container():
    st.title("Proyecto fin de bootcamp")
    st.image("Streamlit/Yahoo!_Finance_image.png", use_column_width=True)

st.sidebar.title("Navegación")
pagina = st.sidebar.radio("Ir a", ["Landing Page", "Presentación de Datos", "Búsqueda de Acción", "Calculadora ROI"])

# Página de inicio
if pagina == "Landing Page":
    st.header("Información básica de las empresas del SP500")
    st.write("""
    Esta es una aplicación de análisis financiero donde puedes:
    - Visualizar datos financieros.
    - Buscar y analizar información detallada sobre acciones específicas.
    """)

    # Display Data
    df = pd.read_csv(filepath_or_buffer="Streamlit/infoSP500.csv", sep=",")
    st.dataframe(df)

    df2 = pd.read_csv(filepath_or_buffer="Streamlit/infoSP500_API.csv", sep=",")
    st.dataframe(df2)

# Página de presentación de datos
elif pagina == "Presentación de Datos":
    st.header("Presentación de Datos Financieros")

# Página de búsqueda de una acción específica
elif pagina == "Búsqueda de Acción":
    st.header("Búsqueda de una Acción Específica")
    
    # Crear una barra de búsqueda para encontrar una acción
    accion = st.text_input("Buscar una acción", "")
    
    if accion:
        st.write(f"Resultados para la acción: {accion}")
        # Aquí puedes agregar la lógica para buscar y mostrar detalles de la acción en base a tu base de datos
        st.write("Información detallada de la acción seleccionada...")
        # Ejemplo de datos de muestra (reemplaza con datos reales)
        st.write({
            "Ticker": accion,
            "Precio Actual": "$100",
            "Cambio (%)": "+2%",
            "Volumen": "1M"
        })

# Página de calculadora de ROI
elif pagina == "Calculadora ROI":
    st.header("Calculadora de ROI")

    # Entradas para el cálculo de ROI
    simbolo = st.text_input("Símbolo de la acción (ej. AAPL para Apple)")
    fecha_inicio = st.date_input("Fecha de inicio", value=datetime(2000, 1, 1))
    fecha_fin = st.date_input("Fecha de fin", value=datetime(2020, 1, 1))

    if simbolo and fecha_inicio and fecha_fin:
        # Convertir fechas a formato de cadena
        fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
        fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')

        # Calcular ROI
        roi, precios_df = calcular_roi(simbolo, fecha_inicio_str, fecha_fin_str)

        if roi is not None:
            st.write(f"El ROI para {simbolo} desde {fecha_inicio_str} hasta {fecha_fin_str} es: {roi:.2f}%")
            st.subheader("Precios históricos en el período seleccionado")
            st.dataframe(precios_df)
        else:
            st.warning("No se pudo calcular el ROI debido a datos insuficientes o errores en la base de datos.")

# Pie de página o cualquier otra información adicional
st.sidebar.write("Aplicación creada con Streamlit")
