

import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime

# Conexión a la base de datos y cálculo de ROI
def calcular_roi(simbolo, fecha_inicio, fecha_fin):
    # Conexión a la base de datos
    db_connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",               # Cambia por tu usuario de MySQL
        password="11jablum11",     # Cambia por tu contraseña de MySQL
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

# Función para obtener los nombres de las acciones
def obtener_nombres_acciones():
    db_connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="11jablum11",
        database="yfinance"
    )
    query = "SELECT simbolo FROM empresas_sp500 ORDER BY simbolo"
    nombres_df = pd.read_sql(query, db_connection)
    db_connection.close()
    return nombres_df['simbolo'].tolist()

# Configuración de la página de Streamlit
st.set_page_config(page_title="Yahoo Finance app", layout="wide")

with st.container():
    st.title("Proyecto fin de bootcamp")
    st.image("Streamlit/Yahoo!_Finance_image.png", use_column_width=True)

st.sidebar.title("Navegación")
pagina = st.sidebar.radio("Ir a", ["Landing Page", "Presentación de Datos", "Búsqueda de Acción"])

if pagina == "Landing Page":
    st.header("Información básica de las empresas del SP500")
    st.write("""
    Esta es una aplicación de análisis financiero donde puedes:
    - Visualizar datos financieros.
    - Buscar y analizar información detallada sobre acciones específicas.
    """)

    # Cargar y mostrar datos básicos de empresas
    try:
        db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="11jablum11",
            database="yfinance"
        )
        df = pd.read_sql("SELECT * FROM empresas_sp500", db_connection)
        st.dataframe(df)
        db_connection.close()
    except mysql.connector.Error as e:
        st.error("Error al conectar con la base de datos: {}".format(e))

elif pagina == "Presentación de Datos":
    st.header("Presentación de Datos Financieros")

elif pagina == "Búsqueda de Acción":
    st.header("Búsqueda de una Acción Específica")

    # Obtener nombres de acciones para el desplegable
    acciones = obtener_nombres_acciones()
    accion_seleccionada = st.selectbox("Selecciona una acción:", acciones)

    if accion_seleccionada:
        st.write(f"Resultados para la acción: {accion_seleccionada}")

        # Selección de rango de fechas usando un calendario
        st.subheader("Cálculo del Retorno de la Inversión (ROI)")
        fecha_inicio = st.date_input("Fecha de inicio", datetime(2023, 1, 1))
        fecha_fin = st.date_input("Fecha de fin", datetime(2023, 12, 31))

        # Validar fechas y calcular ROI
        if fecha_inicio > fecha_fin:
            st.error("La fecha de inicio debe ser anterior a la fecha de fin.")
        elif st.button("Calcular ROI"):
            roi, precios_df = calcular_roi(accion_seleccionada, fecha_inicio, fecha_fin)
            if roi is not None:
                st.write(f"**ROI Total para el periodo seleccionado:** {roi:.2f}%")
                st.write("**Precios en el periodo:**")
                st.dataframe(precios_df)
            else:
                st.warning("No se encontraron datos suficientes para calcular el ROI en el rango de fechas seleccionado.")

# Pie de página o cualquier otra información adicional
st.sidebar.write("Aplicación creada con Streamlit")
