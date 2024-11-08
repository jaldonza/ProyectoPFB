

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Yahoo Finance app", layout="wide")

with st.container():
    st.title("Proyecto fin de bootcamp")
    st.image("Streamlit/Yahoo!_Finance_image.png", use_column_width=True)

st.sidebar.title("Navegación")
pagina = st.sidebar.radio("Ir a", ["Landing Page", "Presentación de Datos", "Búsqueda de Acción"])

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

elif pagina == "Presentación de Datos":
    st.header("Presentación de Datos Financieros")

elif pagina == "Búsqueda de Acción":
    st.header("Búsqueda de una Acción Específica")

    # Crear una barra de búsqueda para encontrar una acción
    accion = st.text_input("Buscar una acción", "")

    if accion:
        st.write(f"Resultados para la acción: {accion}")
        # Aquí puedes agregar la lógica para buscar y mostrar detalles de la acción en base a tu base de datos

        # Ejemplo de datos de muestra (reemplaza con datos reales)
        st.write({
            "Ticker": accion,
            "Precio Actual": "$100",
            "Cambio (%)": "+2%",
            "Volumen": "1M"
        })

        # Cargar datos de cotizaciones para la acción (reemplaza con tu propio DataFrame)
        cotizaciones_df = pd.read_pickle("Streamlit/cotizaciones_sp500.pkl")

        # Filtrar datos de la empresa seleccionada por el símbolo
        df_empresa = cotizaciones_df[cotizaciones_df['Symbol'] == accion].copy()

        if not df_empresa.empty:
            # Selección de rango de fechas para el cálculo de ROI
            st.subheader("Cálculo del Retorno de la Inversión (ROI)")
            fecha_inicio = st.date_input("Fecha de inicio", df_empresa['Date'].min())
            fecha_fin = st.date_input("Fecha de fin", df_empresa['Date'].max())

            # Calcular ROI al hacer clic
            if st.button("Calcular ROI"):
                # Filtrar los datos en el rango de fechas seleccionado
                df_periodo = df_empresa[(df_empresa['Date'] >= pd.to_datetime(fecha_inicio)) & (df_empresa['Date'] <= pd.to_datetime(fecha_fin))]
                
                if not df_periodo.empty:
                    # Precio inicial y final
                    precio_inicial = df_periodo['Close'].iloc[0]
                    precio_final = df_periodo['Close'].iloc[-1]

                    # Cálculo de ROI
                    roi = ((precio_final - precio_inicial) / precio_inicial) * 100
                    st.write(f"**ROI Total para el periodo seleccionado:** {roi:.2f}%")
                else:
                    st.warning("No se encontraron datos para el periodo seleccionado.")
        else:
            st.warning("No se encontró información para la acción especificada.")

# Pie de página o cualquier otra información adicional
st.sidebar.write("Aplicación creada con Streamlit")
