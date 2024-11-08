

import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(page_title="Yahoo Finance app" , layout="wide")

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

# Display Data
    df = pd.read_csv(filepath_or_buffer = "Streamlit/infoSP500.csv", sep = ",")
    
# Dinamic Data
    st.dataframe(df)

    df2 = pd.read_csv(filepath_or_buffer = "Streamlit/infoSP500_API.csv", sep = ",")
    st.dataframe(df2)

elif pagina == "Presentación de Datos":
    st.header("Presentación de Datos Financieros")

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

# Pie de página o cualquier otra información adicional
st.sidebar.write("Aplicación creada con Streamlit")