import streamlit as st
import pandas as pd
from datetime import datetime
from funciones import obtener_empresas, calcular_roi  # Importar las funciones del archivo funciones.py

# Configuración de la aplicación Streamlit
st.set_page_config(page_title="Yahoo Finance app", layout="wide")

# Contenido principal
with st.container():
    st.title("Proyecto fin de bootcamp")
    st.image("Streamlit/Yahoo!_Finance_image.png", use_column_width=True)

st.sidebar.title("Navegación")
pagina = st.sidebar.radio("Ir a", ["Landing Page", "Presentación de Datos", "Búsqueda de Acción", "Calculadora ROI"])

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
        # Ejemplo de datos de muestra (reemplaza con datos reales)
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

# Pie de página o cualquier otra información adicional
st.sidebar.write("Aplicación creada con Streamlit")



