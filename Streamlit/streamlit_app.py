import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from funciones import (
    obtener_empresas, 
    obtener_cotizaciones, 
    graficar_precios_historicos, 
    calcular_metricas
)

# Configuración de la aplicación Streamlit
st.set_page_config(page_title="Yahoo Finance app", layout="wide")

# Contenido principal
with st.container():
    st.title("Yahoo Finance - Proyecto Final")
    st.image("Streamlit/Yahoo!_Finance_image.png", use_container_width=True)

# Barra lateral de navegación
st.sidebar.title("Navegación")
pagina = st.sidebar.radio("Ir a", [
    "Página Principal",
    "Exploratory Data Analysis",
    "Dashboard en Power BI",
    "Clustering y Clasificación",
    "Base de Datos",
    "About Us"
])

# Página principal
if pagina == "Página Principal":
    st.header("Bienvenido al Proyecto Final")
    st.write("""
    Este proyecto se centra en el análisis financiero utilizando datos de acciones del S&P500. A continuación, podrás explorar diferentes secciones:
    - Exploratory Data Analysis: Visualización de datos financieros.
    - Dashboard en Power BI: Analiza el rendimiento financiero.
    - Clustering y Clasificación: Modelos de machine learning para agrupar y clasificar acciones.
    - Base de Datos: Descripción de la arquitectura de la base de datos utilizada.
    - About Us: Conoce al equipo detrás del proyecto.
    """)

# Exploratory Data Analysis
elif pagina == "Exploratory Data Analysis":
    st.header("Exploratory Data Analysis")

    # Selección de funcionalidad
    funcionalidad = st.selectbox("Seleccione la funcionalidad", ["Búsqueda de Acción", "Análisis de Correlación", "Análisis de Métricas Financieras"])

    # Búsqueda de acción
    if funcionalidad == "Búsqueda de Acción":
        st.subheader("Búsqueda de una Acción Específica")

        # Seleccionar empresa
        empresas = obtener_empresas()
        nombres_empresas = list(empresas.keys())
        nombre_empresa = st.selectbox("Seleccione la empresa", nombres_empresas)
        simbolo = empresas[nombre_empresa]

        # Selección de fecha específica
        fecha = st.date_input("Seleccione la fecha")
        if fecha:
            fecha_str = fecha.strftime('%Y-%m-%d')
            cotizaciones_df = obtener_cotizaciones()
            datos_fecha = cotizaciones_df[
                (cotizaciones_df['Company'] == nombre_empresa) & 
                (cotizaciones_df['Date'] == fecha_str)
            ]

            if not datos_fecha.empty:
                st.write(f"Datos para {nombre_empresa} ({simbolo}) en la fecha {fecha_str}:")
                st.write(datos_fecha[['Open', 'High', 'Low', 'Close']])
            else:
                st.warning(f"No se encontraron datos para {nombre_empresa} en la fecha {fecha_str}.")

        # Gráficos de velas
        st.subheader("Gráfico de Velas")
        fecha_inicio = st.date_input("Fecha de inicio")
        fecha_fin = st.date_input("Fecha de fin")

        if fecha_inicio and fecha_fin:
            fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
            fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')
            df_filtrado = cotizaciones_df[
                (cotizaciones_df['Company'] == nombre_empresa) &
                (cotizaciones_df['Date'] >= fecha_inicio_str) &
                (cotizaciones_df['Date'] <= fecha_fin_str)
            ]

            if not df_filtrado.empty:
                fig = go.Figure(data=[go.Candlestick(
                    x=df_filtrado['Date'],
                    open=df_filtrado['Open'],
                    high=df_filtrado['High'],
                    low=df_filtrado['Low'],
                    close=df_filtrado['Close']
                )])
                fig.update_layout(
                    title=f"Gráfico de Velas para {nombre_empresa}",
                    xaxis_title="Fecha",
                    yaxis_title="Precio"
                )
                st.plotly_chart(fig)
            else:
                st.warning(f"No se encontraron datos entre {fecha_inicio_str} y {fecha_fin_str} para {nombre_empresa}.")

    # Análisis de Correlación
    elif funcionalidad == "Análisis de Correlación":
        st.subheader("Análisis de Correlación entre Activos")

        # Cargar cotizaciones
        cotizaciones_df = obtener_cotizaciones()
        empresas = cotizaciones_df['Company'].unique()

        # Selección de activos
        activo_principal = st.selectbox("Seleccione el activo principal", empresas)
        activos_comparar = st.multiselect("Seleccione hasta 4 activos para comparar", empresas, default=empresas[:4])

        if activo_principal and len(activos_comparar) > 0:
            # Preparar los datos
            activos_seleccionados = [activo_principal] + activos_comparar
            df_seleccionados = cotizaciones_df[cotizaciones_df['Company'].isin(activos_seleccionados)]
            precios_df = df_seleccionados.pivot(index='Date', columns='Company', values='Close')
            correlacion = precios_df.corr()

            # Mostrar la matriz de correlación
            st.subheader("Matriz de Correlación")
            st.dataframe(correlacion)

            # Crear y mostrar el heatmap
            st.subheader("Mapa de Calor de Correlación")
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=correlacion.values,
                x=correlacion.columns,
                y=correlacion.index,
                colorscale='Viridis',
                colorbar=dict(title="Correlación")
            ))
            fig_heatmap.update_layout(title="Mapa de Calor de Correlación", xaxis_title="Activos", yaxis_title="Activos")
            st.plotly_chart(fig_heatmap)

            # Graficar las líneas de tiempo
            st.subheader("Evolución de Precios")
            fig = go.Figure()
            for activo in activos_seleccionados:
                fig.add_trace(go.Scatter(x=precios_df.index, y=precios_df[activo], mode='lines', name=activo))
            fig.update_layout(title="Evolución de los Precios de los Activos", xaxis_title="Fecha", yaxis_title="Precio de Cierre")
            st.plotly_chart(fig)

    # Análisis de Métricas Financieras
    elif funcionalidad == "Análisis de Métricas Financieras":
        st.subheader("Análisis de Métricas Financieras")
        st.write("Funcionalidad en desarrollo...")

# Dashboard en Power BI
elif pagina == "Dashboard en Power BI":
    st.header("Dashboard en Power BI")
    st.write("Integra tu dashboard de Power BI utilizando el siguiente iframe:")
    st.write("**Nota:** Asegúrate de incluir el enlace al dashboard aquí.")

# Clustering y Clasificación
elif pagina == "Clustering y Clasificación":
    st.header("Modelos de Clustering y Clasificación")
    st.write("En desarrollo...")

# Base de Datos
elif pagina == "Base de Datos":
    st.header("Arquitectura de la Base de Datos")
    st.write("""
    La base de datos utilizada en este proyecto consta de las siguientes tablas:
    - **empresas_sp500**: Información de las empresas del S&P500.
    - **precios_historicos**: Precios históricos de las acciones.
    - **portafolios_usuarios**: Datos de portafolios creados por usuarios.
    - **portafolio_empresas**: Relación entre portafolios y empresas.
    - **indicadores_sp500**: Indicadores financieros como medias móviles y RSI.
    """)
    st.image("Streamlit/diagrama_bbdd.png", use_column_width=True)

# About Us
elif pagina == "About Us":
    st.header("Sobre Nosotros")
    st.write("""
    Somos un equipo apasionado por el análisis financiero y el machine learning. 
    Conéctate con nosotros:
    - [LinkedIn](https://linkedin.com)
    - [GitHub](https://github.com)
    """)





