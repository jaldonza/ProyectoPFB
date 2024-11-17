import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine


DB_PATH = "C:/Users/Khalid/Desktop/PFB/sp500.db"  # Ruta a tu base de datos


@st.cache_resource
def create_connection():
    engine = create_engine(f'sqlite:///{DB_PATH}')
    return engine


def obtener_empresas(engine):
    query = """
        SELECT DISTINCT id_empresa, simbolo, nombre_empresa 
        FROM empresas_sp500 
        ORDER BY nombre_empresa
    """
    empresas_df = pd.read_sql(query, engine)
    return empresas_df


def obtener_datos_empresa(engine, id_empresa, periodo_inicio, periodo_fin):
    query = f"""
        SELECT ph.fecha, ph.precio_apertura, ph.precio_cierre, ph.maximo, ph.minimo, ph.volumen
        FROM precios_historicos ph
        WHERE ph.id_empresa = {id_empresa} 
        AND ph.fecha BETWEEN '{periodo_inicio}' AND '{periodo_fin}'
        ORDER BY ph.fecha
    """
    return pd.read_sql(query, engine)


def generar_grafico(datos_accion, empresa, company_name):
    fig = go.Figure(
        go.Box(
            y=datos_accion['precio_cierre'],
            name=f'{empresa} - {company_name}',
            boxmean='sd',
            line=dict(width=2, color='yellow'),
            marker=dict(color='lightgreen'),
            boxpoints='all'))           
    
    
    fig.update_layout(
        title=f'Distribución de Precios de Cierre de {empresa} - {company_name}',
        xaxis_title='Precio de Cierre',
        yaxis_title='Frecuencia',
        template='plotly',
        height=600,
        showlegend=False)
    
    return fig


st.set_page_config(page_title="Análisis de Acciones S&P 500", layout="wide")


st.sidebar.title("Navegación")
pagina_seleccionada = st.sidebar.radio(
    "Ir a",
    ("Landing Page", "Análisis de Precios"))


st.title(pagina_seleccionada)


engine = create_connection()


if pagina_seleccionada == "Análisis de Precios":
    st.header("Distribución de Precios de Cierre por Empresa")

    
    empresas_df = obtener_empresas(engine)
    empresas = empresas_df['nombre_empresa'].tolist()
    simbolos = empresas_df['simbolo'].tolist()
    ids_empresa = empresas_df['id_empresa'].tolist()

    
    company_name = st.selectbox("Seleccione la empresa", empresas)
    empresa_index = empresas.index(company_name)
    simbolo = simbolos[empresa_index]
    id_empresa = ids_empresa[empresa_index]

    
    periodo_inicio = st.date_input("Fecha de inicio", value=pd.to_datetime("2023-01-01"))
    periodo_fin = st.date_input("Fecha de fin", value=pd.to_datetime("2023-12-31"))

    
    datos_empresa = obtener_datos_empresa(engine, id_empresa, periodo_inicio, periodo_fin)

    if datos_empresa.empty:
        st.warning("No se encontraron datos para el rango de fechas seleccionado.")
    else:
        
        fig = generar_grafico(datos_empresa, simbolo, company_name)
        st.plotly_chart(fig)

          
          # Página de Landing Page
elif pagina_seleccionada == "Landing Page":
    st.write("Bienvenido al análisis de acciones del S&P 500.")
    st.image("C:/Users/Khalid/Desktop/PFB/yahoo.png",
        caption="Análisis del S&P 500",)
    st.write("Navega por las secciones para explorar los datos.")
    