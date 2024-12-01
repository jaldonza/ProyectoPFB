import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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
    "About Us",
    "Base de Datos"
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

    # Cargar datos de cotización
    cotizaciones_df = obtener_cotizaciones()

    # Asegurar que la columna 'Date' sea del tipo datetime
    if cotizaciones_df['Date'].dtype != 'datetime64[ns]':
        cotizaciones_df['Date'] = pd.to_datetime(cotizaciones_df['Date'])

    # Selección de activo
    empresas = cotizaciones_df['Company'].unique()
    empresa_seleccionada = st.selectbox("Seleccione la empresa", empresas)

    # Selección de periodo
    min_date = cotizaciones_df['Date'].min()
    max_date = cotizaciones_df['Date'].max()
    fecha_inicio = st.date_input("Fecha de inicio", value=min_date, min_value=min_date, max_value=max_date)
    fecha_fin = st.date_input("Fecha de fin", value=max_date, min_value=min_date, max_value=max_date)

    # Convertir fechas seleccionadas a datetime
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    # Validar el rango de fechas
    if fecha_inicio > fecha_fin:
        st.error("La fecha de inicio no puede ser posterior a la fecha de fin.")
    else:
        # Filtrar los datos para el rango de fechas seleccionado
        df_filtrado = cotizaciones_df[
            (cotizaciones_df['Company'] == empresa_seleccionada) &
            (cotizaciones_df['Date'] >= fecha_inicio) &
            (cotizaciones_df['Date'] <= fecha_fin)
        ]

        # Verificar si hay datos después del filtrado
        if not df_filtrado.empty:
            # Calcular métricas
            cotizaciones = df_filtrado['Close']
            metricas = calcular_metricas(cotizaciones)

            # Mostrar resultados
            st.subheader(f"Métricas para {empresa_seleccionada} del {fecha_inicio.date()} al {fecha_fin.date()}")
            st.write(f"**Volatilidad diaria**: {metricas['volatilidad_diaria']:.4f}")
            st.write(f"**Sharpe Ratio**: {metricas['sharpe_ratio']:.4f}" if metricas['sharpe_ratio'] else "Sharpe Ratio no calculable.")
            st.write(f"**Sortino Ratio**: {metricas['sortino_ratio']:.4f}" if metricas['sortino_ratio'] else "Sortino Ratio no calculable.")

            # Graficar retornos diarios
            retornos_diarios = cotizaciones.pct_change().dropna()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=retornos_diarios.index, y=retornos_diarios, mode='lines', name="Retornos Diarios"))
            fig.update_layout(title="Evolución de Retornos Diarios", xaxis_title="Fecha", yaxis_title="Retornos Diarios")
            st.plotly_chart(fig)
        else:
            st.warning(f"No se encontraron datos para {empresa_seleccionada} entre {fecha_inicio.date()} y {fecha_fin.date()}.")
# Base de Datos
elif pagina == "Base de Datos":
    st.header("Arquitectura de la Base de Datos")

    # Mostrar la imagen del diagrama de la base de datos
    st.image("Streamlit/diagrama_bbdd.png", use_column_width=True, caption="Diagrama de la Base de Datos")

    # Explicación del diseño de la base de datos
    st.subheader("Estructura y Creación")
    st.write("""
    La base de datos utilizada en este proyecto fue diseñada para almacenar información financiera del S&P500 y proporcionar soporte para los análisis presentados en esta aplicación.
    
    **Tablas principales:**
    - **empresas_sp500**: Contiene información básica de las empresas, como su símbolo, nombre, sector, industria y capitalización de mercado.
    - **precios_historicos**: Almacena los precios históricos de las acciones, incluyendo la fecha, precios de apertura y cierre, máximos y mínimos diarios, así como el volumen negociado.
    - **portafolios_usuarios**: Permite a los usuarios crear portafolios personalizados y almacenar información relevante.
    - **portafolio_empresas**: Relaciona los portafolios de los usuarios con las empresas, incluyendo la cantidad de acciones y precios de compra.
    - **indicadores_sp500**: Almacena cálculos de indicadores financieros como medias móviles, RSI, y volatilidad.

    **Proceso de creación:**
    1. **Diseño del esquema:** El diagrama presentado arriba fue diseñado utilizando una herramienta de modelado de bases de datos.
    2. **Creación de la base de datos:** Se utilizó MySQL para implementar el esquema en un servidor RDS de AWS.
    3. **Población de datos:** Los datos fueron recolectados de fuentes como Yahoo Finance, y almacenados en las tablas correspondientes.

    **Relaciones entre tablas:**
    - La tabla `precios_historicos` se relaciona con `empresas_sp500` a través de la clave primaria `id_empresa`.
    - La tabla `portafolio_empresas` relaciona los portafolios de usuarios con las empresas correspondientes.
    """)

    st.write("Este diseño asegura flexibilidad y escalabilidad, permitiendo almacenar grandes volúmenes de datos y realizar consultas eficientes para el análisis.")

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
    - [Javier Aldonza](https://linkedin.com/javier-aldonza/)
    - [Roberto Gonzalez Álvarez](https://www.linkedin.com/in/roberto-gonz%C3%A1lez-%C3%A1lvarez-959552140/?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app)
    - [Nombre del Integrante 3](https://linkedin.com)

    ¡Gracias por explorar nuestra aplicación!
    """)

# Pie de página
st.sidebar.write("Aplicación creada con Streamlit")





