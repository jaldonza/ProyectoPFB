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
    funcionalidad = st.selectbox(
        "Seleccione la funcionalidad", 
        ["Búsqueda de Acción", "Análisis de Correlación", "Análisis de Métricas Financieras"]
    )

    if funcionalidad == "Búsqueda de Acción":
        st.subheader("Búsqueda de una Acción Específica")

        # Seleccionar empresa
        empresas = obtener_empresas()
        if not empresas:
            st.error("Error al obtener las empresas. Verifica la conexión con la base de datos.")
        else:
            nombres_empresas = list(empresas.keys())
            nombre_empresa = st.selectbox("Seleccione la empresa", nombres_empresas)
            simbolo = empresas[nombre_empresa]

            # Seleccionar fechas
            fecha_inicio = st.date_input("Seleccione la fecha inicial")
            fecha_fin = st.date_input("Seleccione la fecha final")

            if fecha_inicio and fecha_fin:
                fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
                fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')

                # Obtener datos de cotización
                cotizaciones_df = obtener_cotizaciones()
                if cotizaciones_df is None or cotizaciones_df.empty:
                    st.error("No se pudieron obtener datos de cotización. Verifica la conexión.")
                else:
                    # Filtrar datos para las fechas seleccionadas
                    df_filtrado = cotizaciones_df[
                        (cotizaciones_df['Company'] == nombre_empresa) &
                        (cotizaciones_df['Date'] >= fecha_inicio_str) &
                        (cotizaciones_df['Date'] <= fecha_fin_str)
                    ]

                    # Mostrar precios de las fechas seleccionadas
                    if not df_filtrado.empty:
                        precios_fecha_inicial = df_filtrado[df_filtrado['Date'] == fecha_inicio_str]
                        precios_fecha_final = df_filtrado[df_filtrado['Date'] == fecha_fin_str]

                        st.write(f"**Datos para {nombre_empresa} ({simbolo})**")
                        if not precios_fecha_inicial.empty:
                            st.write(f"Precios para la fecha inicial ({fecha_inicio_str}):")
                            st.write(precios_fecha_inicial[['precio_apertura', 'maximo', 'minimo', 'precio_cierre']])
                        else:
                            st.warning(f"No se encontraron datos para {nombre_empresa} en la fecha inicial ({fecha_inicio_str}).")

                        if not precios_fecha_final.empty:
                            st.write(f"Precios para la fecha final ({fecha_fin_str}):")
                            st.write(precios_fecha_final[['precio_apertura', 'maximo', 'minimo', 'precio_cierre']])
                        else:
                            st.warning(f"No se encontraron datos para {nombre_empresa} en la fecha final ({fecha_fin_str}).")

                        # Generar gráfico de velas
                        st.subheader("Gráfico de Velas")
                        fig = go.Figure(data=[go.Candlestick(
                            x=df_filtrado['Date'],
                            open=df_filtrado['precio_apertura'],
                            high=df_filtrado['maximo'],
                            low=df_filtrado['minimo'],
                            close=df_filtrado['precio_cierre']
                        )])
                        fig.update_layout(
                            title=f"Gráfico de Velas para {nombre_empresa} ({simbolo})",
                            xaxis_title="Fecha",
                            yaxis_title="Precio"
                        )
                        st.plotly_chart(fig)
                    else:
                        st.warning(f"No se encontraron datos para {nombre_empresa} entre {fecha_inicio_str} y {fecha_fin_str}.")

    elif funcionalidad == "Análisis de Correlación":
        st.subheader("Análisis de Correlación entre Activos")
        cotizaciones_df = obtener_cotizaciones()
        if cotizaciones_df is None or cotizaciones_df.empty:
            st.error("No se pudieron obtener datos de cotización. Verifica la conexión.")
        else:
            empresas = cotizaciones_df['Company'].unique()
            activo_principal = st.selectbox("Seleccione el activo principal", empresas)
            activos_comparar = st.multiselect("Seleccione hasta 4 activos para comparar", empresas, default=empresas[:4])

            if activo_principal and len(activos_comparar) > 0:
                activos_seleccionados = [activo_principal] + activos_comparar
                df_seleccionados = cotizaciones_df[cotizaciones_df['Company'].isin(activos_seleccionados)]
                precios_df = df_seleccionados.pivot(index='Date', columns='Company', values='Close')
                correlacion = precios_df.corr()

                # Mostrar matriz de correlación
                st.dataframe(correlacion)

                # Graficar heatmap
                fig_heatmap = go.Figure(data=go.Heatmap(
                    z=correlacion.values,
                    x=correlacion.columns,
                    y=correlacion.index,
                    colorscale='Viridis'
                ))
                fig_heatmap.update_layout(title="Mapa de Correlación", xaxis_title="Activos", yaxis_title="Activos")
                st.plotly_chart(fig_heatmap)








