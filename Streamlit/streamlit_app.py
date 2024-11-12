import streamlit as st
import pandas as pd
import pymysql
from datetime import datetime

# Función para obtener la lista de símbolos desde la base de datos
def obtener_simbolos():
    try:
        # Conectar a la base de datos
        connection = pymysql.connect(
            host="pfb.cp2wsq8yih32.eu-north-1.rds.amazonaws.com",
            user="admin",
            password="11jablum11",
            database="yfinance",
            port=3306
        )
        cursor = connection.cursor()

        # Consulta para obtener los símbolos de la tabla empresas_sp500
        query = "SELECT simbolo FROM empresas_sp500"
        cursor.execute(query)
        simbolos = cursor.fetchall()
        
        # Convertir la lista de tuplas en una lista simple de strings
        simbolos = [simbolo[0] for simbolo in simbolos]

        # Cerrar conexión
        cursor.close()
        connection.close()

        return simbolos

    except pymysql.MySQLError as e:
        st.error(f"Error al conectar a la base de datos para obtener símbolos: {e}")
        return []

# Función calcular ROI actualizada
def calcular_roi(simbolo, fecha_compra, fecha_venta):
    try:
        # Conexión a la base de datos RDS
        db_connection = pymysql.connect(
            host="pfb.cp2wsq8yih32.eu-north-1.rds.amazonaws.com",
            user="admin",
            password="11jablum11",
            database="yfinance",
            port=3306
        )
        cursor = db_connection.cursor()

        # Consulta para el precio de compra (precio de cierre en la fecha de compra)
        query_compra = """
        SELECT precio_cierre
        FROM precios_historicos
        WHERE id_empresa = %s AND fecha = %s
        """
        cursor.execute(query_compra, (simbolo, fecha_compra))
        resultado_compra = cursor.fetchone()

        # Consulta para el precio de venta (precio de cierre en la fecha de venta)
        query_venta = """
        SELECT precio_cierre
        FROM precios_historicos
        WHERE id_empresa = %s AND fecha = %s
        """
        cursor.execute(query_venta, (simbolo, fecha_venta))
        resultado_venta = cursor.fetchone()

        # Cerrar el cursor y la conexión
        cursor.close()
        db_connection.close()

        # Verificar que se encontraron precios en ambas fechas
        if resultado_compra and resultado_venta:
            precio_compra = resultado_compra[0]
            precio_venta = resultado_venta[0]

            # Calcular ROI
            ganancia = precio_venta - precio_compra
            roi = (ganancia / precio_compra) * 100

            # Crear un DataFrame con los precios consultados
            precios_df = pd.DataFrame(
                {
                    'Fecha': [fecha_compra, fecha_venta],
                    'Precio Cierre': [precio_compra, precio_venta]
                }
            )
            return roi, precios_df

        else:
            st.warning("No se encontraron precios de cierre para una o ambas fechas seleccionadas.")
            return None, None

    except pymysql.MySQLError as err:
        st.error(f"Error al conectar a la base de datos: {err}")
        return None, None

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

    # Obtener la lista de símbolos para el desplegable
    simbolos = obtener_simbolos()
    simbolo = st.selectbox("Seleccione el símbolo de la acción", simbolos)

    # Entradas para las fechas
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


