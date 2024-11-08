
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import mysql.connector

# Configura la conexión a la base de datos
db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="11jablum11",
    database="yfinance"
)
cursor = db_connection.cursor(dictionary=True)

# Función para cargar datos de cotizaciones desde la base de datos
def cargar_cotizaciones():
    query = """
    SELECT e.nombre_empresa AS Company, ph.fecha AS Date, ph.precio_cierre AS Close, e.id_empresa
    FROM precios_historicos ph
    JOIN empresas_sp500 e ON ph.id_empresa = e.id_empresa
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return pd.DataFrame(result)

# Función principal para mostrar el análisis técnico en el dashboard
def mostrar_dashboard():
    st.title("Análisis Exploratorio de Datos")
    st.write("Selecciona una empresa para explorar sus datos de cotización y análisis técnico.")

    # Cargar datos de cotización
    cotizaciones_df = cargar_cotizaciones()
    empresas = cotizaciones_df['Company'].unique()
    empresa_seleccionada = st.selectbox("Selecciona una empresa:", empresas)

    # Filtrar datos de la empresa seleccionada
    df_empresa = cotizaciones_df[cotizaciones_df['Company'] == empresa_seleccionada].copy()

    # Gráfico de Precios Históricos
    st.subheader("Precios Históricos")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_empresa['Date'], y=df_empresa['Close'], mode='lines', name='Precio de Cierre'))
    fig.update_layout(title="Precios Históricos", xaxis_title="Fecha", yaxis_title="Precio de Cierre")
    st.plotly_chart(fig, use_container_width=True)

    # Calcular y mostrar Medias Móviles (SMA 50 y SMA 200)
    st.subheader("Medias Móviles")
    df_empresa['SMA_50'] = df_empresa['Close'].rolling(window=50).mean()
    df_empresa['SMA_200'] = df_empresa['Close'].rolling(window=200).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_empresa['Date'], y=df_empresa['Close'], mode='lines', name='Precio de Cierre'))
    fig.add_trace(go.Scatter(x=df_empresa['Date'], y=df_empresa['SMA_50'], mode='lines', name='SMA 50'))
    fig.add_trace(go.Scatter(x=df_empresa['Date'], y=df_empresa['SMA_200'], mode='lines', name='SMA 200'))
    fig.update_layout(title="Medias Móviles", xaxis_title="Fecha", yaxis_title="Precio")
    st.plotly_chart(fig, use_container_width=True)

# Configuración de la página principal de Streamlit
st.set_page_config(page_title="Yahoo Finance app", layout="wide")

with st.container():
    st.title("Proyecto Fin de Bootcamp")
    st.image("Streamlit/Yahoo!_Finance_image.png", use_column_width=True)

st.sidebar.title("Navegación")
pagina = st.sidebar.radio("Ir a", ["Landing Page", "Presentación de Datos", "Búsqueda de Acción", "Análisis Técnico"])

if pagina == "Landing Page":
    st.header("Información básica de las empresas del SP500")
    st.write("""
    Esta es una aplicación de análisis financiero donde puedes:
    - Visualizar datos financieros.
    - Buscar y analizar información detallada sobre acciones específicas.
    """)

    # Mostrar datos básicos de las empresas
    df = pd.read_csv(filepath_or_buffer="Streamlit/infoSP500.csv", sep=",")
    st.dataframe(df)

    df2 = pd.read_csv(filepath_or_buffer="Streamlit/infoSP500_API.csv", sep=",")
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

elif pagina == "Análisis Técnico":
    mostrar_dashboard()

# Pie de página o cualquier otra información adicional
st.sidebar.write("Aplicación creada con Streamlit")
