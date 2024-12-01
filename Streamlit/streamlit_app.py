import streamlit as st
import pandas as pd
from datetime import datetime
from funciones import obtener_cotizaciones, graficar_precios_historicos, graficar_medias_moviles, graficar_rsi, calcular_metricas

# Configuración de la aplicación Streamlit
st.set_page_config(page_title="Yahoo Finance App", layout="wide")

# Barra lateral de navegación
st.sidebar.title("Navegación")
pagina = st.sidebar.radio("Ir a", [
    "Landing Page",
    "Análisis Exploratorio",
    "Dashboard Financiero",
    "Análisis de Métricas Financieras",
    "About Us"
])

# Página de inicio
if pagina == "Landing Page":
    st.title("Yahoo Finance - Proyecto Final")
    st.image("Streamlit/Yahoo!_Finance_image.png", use_container_width=True)
    st.header("Descripción General del Proyecto")
    st.write("""
    Bienvenido a nuestra aplicación de análisis financiero diseñada para trabajar con datos del S&P500. En este proyecto podrás explorar:
    
    - **Análisis Exploratorio:** Visualiza gráficos históricos y analiza la correlación entre activos.
    - **Dashboard Financiero:** Unifica toda la información en un tablero dinámico (Power BI).
    - **Análisis de Métricas Financieras:** Calcula métricas clave como volatilidad diaria, ratios de Sharpe y Sortino.
    - **About Us:** Conoce al equipo y descubre cómo creamos esta aplicación.
    """)

# Análisis Exploratorio
elif pagina == "Análisis Exploratorio":
    st.header("Análisis Exploratorio")
    cotizaciones_df = obtener_cotizaciones()

    # Cargar datos de cotización
    cotizaciones_df = obtener_cotizaciones()

    # Verificar y convertir la columna 'Date' a datetime si no lo es
    if cotizaciones_df['Date'].dtype != 'datetime64[ns]':
        cotizaciones_df['Date'] = pd.to_datetime(cotizaciones_df['Date'])

    # Dropdown para seleccionar la empresa
    empresas = cotizaciones_df['Company'].unique()
    empresa_seleccionada = st.selectbox("Seleccione la empresa", empresas)

    # Seleccionar el rango de fechas
    min_date = cotizaciones_df['Date'].min()
    max_date = cotizaciones_df['Date'].max()
    fecha_inicio = st.date_input("Fecha de inicio", value=min_date, min_value=min_date, max_value=max_date)
    fecha_fin = st.date_input("Fecha de fin", value=max_date, min_value=min_date, max_value=max_date)

    # Convertir fechas seleccionadas a datetime si no lo están
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    # Validar que fecha_inicio no sea posterior a fecha_fin
    if fecha_inicio > fecha_fin:
        st.error("La fecha de inicio no puede ser posterior a la fecha de fin.")
    else:
        # Filtrar los datos para el rango de fechas
        df = cotizaciones_df[
            (cotizaciones_df['Company'] == empresa_seleccionada) & 
            (cotizaciones_df['Date'] >= fecha_inicio) & 
            (cotizaciones_df['Date'] <= fecha_fin)
        ]

        # Seleccionar el tipo de gráfico
        tab = st.selectbox("Seleccione una visualización", ["Precios Históricos", "Medias Móviles", "RSI"])
    
        # Mostrar gráfico según la pestaña seleccionada
        if not df.empty:
            if tab == "Precios Históricos":
                st.plotly_chart(graficar_precios_historicos(df, empresa_seleccionada))
            elif tab == "Medias Móviles":
                st.plotly_chart(graficar_medias_moviles(df, empresa_seleccionada))
            elif tab == "RSI":
                st.plotly_chart(graficar_rsi(df, empresa_seleccionada))
        else:
            st.warning(f"No hay datos disponibles para {empresa_seleccionada} en el rango de fechas seleccionado.")

    # Subsección: Análisis de correlación
    st.subheader("Análisis de Correlación entre Activos")
    activo_principal = st.selectbox("Seleccione el activo principal", empresas)
    activos_comparar = st.multiselect("Seleccione hasta 4 activos para comparar", empresas, default=empresas[:4])

    if activo_principal and len(activos_comparar) > 0:
        activos_seleccionados = [activo_principal] + activos_comparar
        df_seleccionados = cotizaciones_df[cotizaciones_df['Company'].isin(activos_seleccionados)]
        precios_df = df_seleccionados.pivot(index='Date', columns='Company', values='Close')
        correlacion = precios_df.corr()

        st.subheader("Matriz de Correlación")
        st.dataframe(correlacion)

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

# Dashboard Financiero
elif pagina == "Dashboard Financiero":
    st.header("Dashboard Financiero")
    st.write("Aquí se integrará el tablero de Power BI.")
    st.write("**Nota:** Una vez que tengas el enlace del tablero, actualiza esta sección.")

# Análisis de Métricas Financieras
elif pagina == "Análisis de Métricas Financieras":
    st.header("Análisis de Métricas Financieras")
    cotizaciones_df = obtener_cotizaciones()

    empresas = cotizaciones_df['Company'].unique()
    empresa_seleccionada = st.selectbox("Seleccione la empresa", empresas)
    fecha_inicio = st.date_input("Fecha de inicio", value=cotizaciones_df['Date'].min())
    fecha_fin = st.date_input("Fecha de fin", value=cotizaciones_df['Date'].max())

    df_filtrado = cotizaciones_df[
        (cotizaciones_df['Company'] == empresa_seleccionada) &
        (cotizaciones_df['Date'] >= fecha_inicio) &
        (cotizaciones_df['Date'] <= fecha_fin)
    ]

    if not df_filtrado.empty:
        cotizaciones = df_filtrado['Close']
        metricas = calcular_metricas(cotizaciones)

        st.subheader(f"Métricas para {empresa_seleccionada} del {fecha_inicio} al {fecha_fin}")
        st.write(f"**Volatilidad diaria**: {metricas['volatilidad_diaria']:.4f}")
        st.write(f"**Sharpe Ratio**: {metricas['sharpe_ratio']:.4f}")
        st.write(f"**Sortino Ratio**: {metricas['sortino_ratio']:.4f}")

# About Us
elif pagina == "About Us":
    st.header("About Us")
    st.write("""
    Esta aplicación fue creada como parte de un proyecto final para explorar el análisis financiero utilizando Python y Streamlit. 

    **Tecnologías Utilizadas:**
    - Python (pandas, numpy, plotly, matplotlib, yfinance)
    - Streamlit
    - MySQL (Base de datos en AWS RDS)
    - Power BI

    **Proceso de Creación:**
    1. Diseño de la base de datos para almacenar información financiera.
    2. Creación de funciones para conectar y analizar datos.
    3. Construcción de la aplicación interactiva utilizando Streamlit.
    4. Integración de Power BI para análisis avanzado.
    
    **Equipo:**
    - [Nombre del Integrante 1](https://linkedin.com)
    - [Nombre del Integrante 2](https://linkedin.com)
    - [Nombre del Integrante 3](https://linkedin.com)

    ¡Gracias por explorar nuestra aplicación!
    """)

# Pie de página
st.sidebar.write("Aplicación creada con Streamlit")





