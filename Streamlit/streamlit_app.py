import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from funciones import obtener_empresas, calcular_roi, obtener_cotizaciones  # Importar funciones

# Configuración de la aplicación Streamlit
st.set_page_config(page_title="Yahoo Finance app", layout="wide")

# Contenido principal
with st.container():
    st.title("Proyecto fin de bootcamp")
    st.image("Streamlit/Yahoo!_Finance_image.png", use_column_width=True)

st.sidebar.title("Navegación")
pagina = st.sidebar.radio("Ir a", ["Landing Page", "Presentación de Datos", "Búsqueda de Acción", "Calculadora ROI", "Dashboard Financiero"])

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
        st.write({
            "Ticker": accion,
            "Precio Actual": "$100",
            "Cambio (%)": "+2%",
            "Volumen": "1M"
        })

# Página de calculadora de ROI
elif pagina == "Calculadora ROI":
    st.header("Calculadora de ROI")

    # Obtener el diccionario de empresas {nombre_empresa: simbolo}
    empresas = obtener_empresas()
    nombres_empresas = list(empresas.keys())

    # Desplegable para seleccionar el nombre de la empresa
    nombre_empresa = st.selectbox("Seleccione la empresa", nombres_empresas)
    simbolo = empresas[nombre_empresa]  # Obtener el símbolo de la empresa seleccionada

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
            st.write(f"El ROI para {nombre_empresa} ({simbolo}) desde {fecha_inicio_str} hasta {fecha_fin_str} es: {roi:.2f}%")
            st.subheader("Precios históricos en el período seleccionado")
            st.dataframe(precios_df)
        else:
            st.warning("No se pudo calcular el ROI debido a datos insuficientes o errores en la base de datos.")

# Página del Dashboard Financiero
elif pagina == "Dashboard Financiero":
    st.header("Dashboard Financiero - Datos de Cotización")
    
    # Cargar datos de cotización
    cotizaciones_df = obtener_cotizaciones()

    # Dropdown para seleccionar la empresa
    empresas = cotizaciones_df['Company'].unique()
    empresa_seleccionada = st.selectbox("Seleccione la empresa", empresas)

    # Seleccionar el tipo de gráfico
    tab = st.selectbox("Seleccione una visualización", ["Precios Históricos", "Medias Móviles", "RSI"])

    # Filtrar datos para la empresa seleccionada
    df = cotizaciones_df[cotizaciones_df['Company'] == empresa_seleccionada]

    # Funciones para gráficos
    def graficar_precios_historicos(df, empresa_seleccionada):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Precio de Cierre'))
        fig.update_layout(title=f"Precios Históricos - {empresa_seleccionada}", xaxis_title="Fecha", yaxis_title="Precio de Cierre")
        return fig

    def graficar_medias_moviles(df, empresa_seleccionada):
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Precio de Cierre'))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'], mode='lines', name='SMA 50'))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_200'], mode='lines', name='SMA 200'))
        fig.update_layout(title=f"Medias Móviles - {empresa_seleccionada}", xaxis_title="Fecha", yaxis_title="Precio")
        return fig

    def graficar_rsi(df, empresa_seleccionada):
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], mode='lines', name='RSI'))
        fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Sobrecompra", annotation_position="top right")
        fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Sobreventa", annotation_position="bottom right")
        fig.update_layout(title=f"RSI (Relative Strength Index) - {empresa_seleccionada}", xaxis_title="Fecha", yaxis_title="RSI")
        return fig

    # Mostrar gráfico según la pestaña seleccionada
    if tab == "Precios Históricos":
        st.plotly_chart(graficar_precios_historicos(df, empresa_seleccionada))
    elif tab == "Medias Móviles":
        st.plotly_chart(graficar_medias_moviles(df, empresa_seleccionada))
    elif tab == "RSI":
        st.plotly_chart(graficar_rsi(df, empresa_seleccionada))

# Pie de página o cualquier otra información adicional
st.sidebar.write("Aplicación creada con Streamlit")



