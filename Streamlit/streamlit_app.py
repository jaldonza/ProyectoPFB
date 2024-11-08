

import streamlit as st
import pandas as pd
from datetime import datetime
from calculadora_roi import calcular_roi  # Importa la función desde calculadora_roi.py

# Configuración de conexión a la base de datos
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
