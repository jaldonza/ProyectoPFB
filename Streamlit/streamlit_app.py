import streamlit as st
import pandas as pd
from datetime import datetime
from funciones import obtener_empresas, obtener_cotizaciones, crear_grafico_velas  # Importar las funciones necesarias

# Configuración de la aplicación Streamlit
st.set_page_config(page_title="Yahoo Finance app", layout="wide")

# Barra lateral de navegación
st.sidebar.title("Navegación")
pagina = st.sidebar.radio("Ir a", [
    "Landing Page",
    "Análisis Exploratorio",
    "Calculadora ROI",
    "Análisis de Métricas Financieras"
])

# Página de inicio
if pagina == "Landing Page":
    st.title("Yahoo Finance - Proyecto Final")
    st.image("Streamlit/Yahoo!_Finance_image.png", use_container_width=True)
    st.header("Descripción General del Proyecto")
    st.write("""
    Bienvenido a la aplicación de análisis financiero del S&P500. Aquí podrás explorar diferentes funcionalidades:
    
    - **Análisis Exploratorio:** Consulta gráficos financieros y análisis de correlación.
    - **Calculadora ROI:** Calcula el retorno de la inversión para un periodo seleccionado (disponible en Power BI).
    - **Análisis de Métricas Financieras:** Consulta métricas como volatilidad diaria, Sharpe Ratio, y más.
    """)

# Análisis Exploratorio
elif pagina == "Análisis Exploratorio":
    st.header("Análisis Exploratorio")
    cotizaciones_df = obtener_cotizaciones()

    # Subsección: Dashboard Financiero
    st.subheader("Dashboard Financiero - Datos de Cotización")
    empresas = cotizaciones_df['Company'].unique()
    empresa_seleccionada = st.selectbox("Seleccione la empresa", empresas)
    fecha_inicio = st.date_input("Fecha de inicio", value=cotizaciones_df['Date'].min())
    fecha_fin = st.date_input("Fecha de fin", value=cotizaciones_df['Date'].max())

    if fecha_inicio and fecha_fin:
        df_filtrado = cotizaciones_df[
            (cotizaciones_df['Company'] == empresa_seleccionada) &
            (cotizaciones_df['Date'] >= fecha_inicio) &
            (cotizaciones_df['Date'] <= fecha_fin)
        ]
        tab = st.selectbox("Seleccione una visualización", ["Precios Históricos", "Medias Móviles", "RSI"])

        if tab == "Precios Históricos":
            st.plotly_chart(graficar_precios_historicos(df_filtrado, empresa_seleccionada))
        elif tab == "Medias Móviles":
            st.plotly_chart(graficar_medias_moviles(df_filtrado, empresa_seleccionada))
        elif tab == "RSI":
            st.plotly_chart(graficar_rsi(df_filtrado, empresa_seleccionada))

    # Subsección: Análisis de Correlación
    st.subheader("Análisis de Correlación entre Activos")
    activo_principal = st.selectbox("Seleccione el activo principal", empresas)
    activos_comparar = st.multiselect("Seleccione hasta 4 activos para comparar", empresas, default=empresas[:4])

    if activo_principal and len(activos_comparar) > 0:
        activos_seleccionados = [activo_principal] + activos_comparar
        df_seleccionados = cotizaciones_df[cotizaciones_df['Company'].isin(activos_seleccionados)]
        precios_df = df_seleccionados.pivot(index='Date', columns='Company', values='Close')
        correlacion = precios_df.corr()

        # Matriz de correlación
        st.subheader("Matriz de Correlación")
        st.dataframe(correlacion)

        # Heatmap
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

        # Gráfico de líneas
        st.subheader("Evolución de Precios")
        fig = go.Figure()
        for activo in activos_seleccionados:
            fig.add_trace(go.Scatter(x=precios_df.index, y=precios_df[activo], mode='lines', name=activo))
        fig.update_layout(title="Evolución de los Precios de los Activos", xaxis_title="Fecha", yaxis_title="Precio de Cierre")
        st.plotly_chart(fig)

# Calculadora ROI
elif pagina == "Calculadora ROI":
    st.header("Calculadora de ROI")
    empresas = obtener_empresas()
    nombres_empresas = list(empresas.keys())
    nombre_empresa = st.selectbox("Seleccione la empresa", nombres_empresas)
    simbolo = empresas[nombre_empresa]
    fecha_inicio = st.date_input("Fecha de inicio", value=datetime(2000, 1, 3))
    fecha_fin = st.date_input("Fecha de fin", value=datetime(2020, 1, 3))

    if simbolo and fecha_inicio and fecha_fin:
        fecha_inicio_str = fecha_inicio.strftime('%Y-%m-%d')
        fecha_fin_str = fecha_fin.strftime('%Y-%m-%d')
        roi, precios_df = calcular_roi(simbolo, fecha_inicio_str, fecha_fin_str)
        if roi is not None:
            st.write(f"El ROI para {nombre_empresa} ({simbolo}) desde {fecha_inicio_str} hasta {fecha_fin_str} es: {roi:.2f}%")
            st.subheader("Precios históricos en el período seleccionado")
            st.dataframe(precios_df)
        else:
            st.warning("No se pudo calcular el ROI debido a datos insuficientes o errores en la base de datos.")

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

# Pie de página
st.sidebar.write("Aplicación creada con Streamlit")
