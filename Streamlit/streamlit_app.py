import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from funciones import obtener_empresas, calcular_roi, obtener_cotizaciones, graficar_precios_historicos, graficar_medias_moviles, graficar_rsi, calcular_metricas  # Importar funciones

# Configuración de la aplicación Streamlit
st.set_page_config(page_title="Yahoo Finance app", layout="wide")

# Contenido principal
with st.container():
    st.title("Proyecto fin de bootcamp")
    st.image("Streamlit/Yahoo!_Finance_image.png", use_container_width=True)

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
    accion = st.text_input("Buscar una acción", "")
    if accion:
        st.write(f"Resultados para la acción: {accion}")
        st.write({
            "Ticker": accion,
            "Precio Actual": "$100",
            "Cambio (%)": "+2%",
            "Volumen": "1M"
        })

# Página de calculadora de ROI
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

# Página del Dashboard Financiero
elif pagina == "Dashboard Financiero":
    st.header("Dashboard Financiero - Datos de Cotización")
    
    # Cargar datos de cotización
    cotizaciones_df = obtener_cotizaciones()

    # Dropdown para seleccionar la empresa
    empresas = cotizaciones_df['Company'].unique()
    empresa_seleccionada = st.selectbox("Seleccione la empresa", empresas)

    # Seleccionar el rango de fechas
    fecha_inicio = st.date_input("Fecha de inicio", value=cotizaciones_df['Date'].min())
    fecha_fin = st.date_input("Fecha de fin", value=cotizaciones_df['Date'].max())
    
    # Filtrar los datos para el rango de fechas
    df = cotizaciones_df[(cotizaciones_df['Company'] == empresa_seleccionada) & 
                         (cotizaciones_df['Date'] >= fecha_inicio) & 
                         (cotizaciones_df['Date'] <= fecha_fin)]

    # Seleccionar el tipo de gráfico
    tab = st.selectbox("Seleccione una visualización", ["Precios Históricos", "Medias Móviles", "RSI"])
   
    # Mostrar gráfico según la pestaña seleccionada
    if tab == "Precios Históricos":
        st.plotly_chart(graficar_precios_historicos(df, empresa_seleccionada))
    elif tab == "Medias Móviles":
        st.plotly_chart(graficar_medias_moviles(df, empresa_seleccionada))
    elif tab == "RSI":
        st.plotly_chart(graficar_rsi(df, empresa_seleccionada))

# Página de análisis de correlación
elif pagina == "Análisis de Correlación":
    st.header("Análisis de Correlación entre Activos")
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

elif pagina == "Análisis de Métricas Financieras":
    st.header("Análisis de Métricas Financieras")

    # Cargar datos de cotización
    cotizaciones_df = obtener_cotizaciones()

    # Selección de activo
    empresas = cotizaciones_df['Company'].unique()
    empresa_seleccionada = st.selectbox("Seleccione la empresa", empresas)

    # Selección de periodo
    fecha_inicio = st.date_input("Fecha de inicio", value=cotizaciones_df['Date'].min())
    fecha_fin = st.date_input("Fecha de fin", value=cotizaciones_df['Date'].max())

    # Filtrar los datos para el activo y periodo seleccionados
    df_filtrado = cotizaciones_df[
        (cotizaciones_df['Company'] == empresa_seleccionada) &
        (cotizaciones_df['Date'] >= fecha_inicio) &
        (cotizaciones_df['Date'] <= fecha_fin)
    ]

    # Verificar si hay datos
    if not df_filtrado.empty:
        # Calcular métricas
        cotizaciones = df_filtrado['Close']
        metricas = calcular_metricas(cotizaciones)

        # Mostrar resultados
        st.subheader(f"Métricas para {empresa_seleccionada} del {fecha_inicio} al {fecha_fin}")
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
        st.warning("No se encontraron datos para el periodo seleccionado.")

# Pie de página
st.sidebar.write("Aplicación creada con Streamlit")




