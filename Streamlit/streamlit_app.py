import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from funciones import obtener_empresas, calcular_roi, obtener_cotizaciones, graficar_precios_historicos, graficar_medias_moviles, graficar_rsi, calcular_metricas  # Importar funciones

# Configuración de la aplicación Streamlit
st.set_page_config(page_title="Yahoo Finance app", layout="wide")

# Barra lateral de navegación
st.sidebar.title("Navegación")
pagina = st.sidebar.radio("Ir a", [
    "Landing Page", 
    "Presentación de Datos", 
    "Búsqueda de Acción", 
    "Calculadora ROI", 
    "Dashboard Financiero", 
    "Análisis de Correlación",
    "Análisis de Métricas Financieras"
])

# Página de inicio
if pagina == "Landing Page":
    st.title("Yahoo Finance - Proyecto Final")
    st.image("Streamlit/Yahoo!_Finance_image.png", use_container_width=True)
    st.header("Descripción General del Proyecto")
    st.write("""
    Bienvenido a la aplicación de análisis financiero del S&P500. Aquí podrás explorar diferentes funcionalidades:
    
    - **Presentación de Datos:** Visualización de información básica de las empresas del S&P500.
    - **Búsqueda de Acción:** Consulta los precios históricos de una acción específica y visualiza gráficos de velas.
    - **Calculadora ROI:** Calcula el retorno de la inversión para un periodo seleccionado (disponible en Power BI).
    - **Dashboard Financiero:** Gráficos dinámicos para analizar el rendimiento de las acciones.
    - **Análisis de Correlación:** Estudia las relaciones entre diferentes activos financieros.
    - **Análisis de Métricas Financieras:** Consulta métricas como volatilidad diaria, Sharpe Ratio, y más.
    """)

# Página de presentación de datos
elif pagina == "Presentación de Datos":
    st.header("Presentación de Datos Financieros")
    # Resto de la lógica para esta página...

# Página de búsqueda de una acción específica
elif pagina == "Búsqueda de Acción":
    st.header("Búsqueda de una Acción Específica")
    # Resto de la lógica para esta página...

# Página de calculadora de ROI
elif pagina == "Calculadora ROI":
    st.header("Calculadora de ROI")
    # Resto de la lógica para esta página...

# Página del Dashboard Financiero
elif pagina == "Dashboard Financiero":
    st.header("Dashboard Financiero - Datos de Cotización")
    # Resto de la lógica para esta página...

# Página de análisis de correlación
elif pagina == "Análisis de Correlación":
    st.header("Análisis de Correlación entre Activos")
    # Resto de la lógica para esta página...

# Página de análisis de métricas financieras
elif pagina == "Análisis de Métricas Financieras":
    st.header("Análisis de Métricas Financieras")
    # Resto de la lógica para esta página...

# Pie de página
st.sidebar.write("Aplicación creada con Streamlit")
