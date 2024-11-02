import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Cargar datos de cotización
cotizaciones_df = pd.read_pickle('Streamlit/cotizaciones_sp500.pkl') 

def mostrar_dashboard():
    st.title("Análisis Exploratorio de Datos")
    st.write("Selecciona una empresa para explorar sus datos de cotización y análisis técnico.")

    # Selección de empresa
    empresas = cotizaciones_df['Company'].unique()
    empresa_seleccionada = st.selectbox("Selecciona una empresa:", empresas)

    # Filtramos los datos de la empresa seleccionada
    df_empresa = cotizaciones_df[cotizaciones_df['Company'] == empresa_seleccionada].copy()

    # Gráfico de Precios Históricos
    st.subheader("Precios Históricos")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_empresa['Date'], y=df_empresa['Close'], mode='lines', name='Precio de Cierre'))
    fig.update_layout(title="Precios Históricos", xaxis_title="Fecha", yaxis_title="Precio de Cierre")
    st.plotly_chart(fig, use_container_width=True)

    # Gráfico de Medias Móviles
    st.subheader("Medias Móviles")
    df_empresa['SMA_50'] = df_empresa['Close'].rolling(window=50).mean()
    df_empresa['SMA_200'] = df_empresa['Close'].rolling(window=200).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_empresa['Date'], y=df_empresa['Close'], mode='lines', name='Precio de Cierre'))
    fig.add_trace(go.Scatter(x=df_empresa['Date'], y=df_empresa['SMA_50'], mode='lines', name='SMA 50'))
    fig.add_trace(go.Scatter(x=df_empresa['Date'], y=df_empresa['SMA_200'], mode='lines', name='SMA 200'))
    fig.update_layout(title="Medias Móviles", xaxis_title="Fecha", yaxis_title="Precio")
    st.plotly_chart(fig, use_container_width=True)

    # Gráfico de RSI
    st.subheader("Relative Strength Index (RSI)")
    delta = df_empresa['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df_empresa['RSI'] = 100 - (100 / (1 + rs))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_empresa['Date'], y=df_empresa['RSI'], mode='lines', name='RSI'))
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Sobrecompra", annotation_position="top right")
    fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Sobreventa", annotation_position="bottom right")
    fig.update_layout(title="RSI (Relative Strength Index)", xaxis_title="Fecha", yaxis_title="RSI")
    st.plotly_chart(fig, use_container_width=True)
