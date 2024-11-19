import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sqlalchemy import create_engine
import plotly.express as px
import pickle
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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
    ("Landing Page", "Análisis de Precios", "Clustering de Empresas del S&P 500"))


st.title(pagina_seleccionada)


engine = create_connection()


# Página de Landing Page
if pagina_seleccionada == "Landing Page":
    st.write("Bienvenido al análisis de acciones del S&P 500.")
    st.image(
        "C:/Users/Khalid/Desktop/PFB/yahoo.png",
        caption="Análisis del S&P 500",)
    st.write("Navega por las secciones para explorar los datos.")


# Página de Análisis de Precios
elif pagina_seleccionada == "Análisis de Precios":
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


# Página de Clustering 
elif pagina_seleccionada == "Clustering de Empresas del S&P 500":
    
    @st.cache_data
    def cargar_encoders(simbolo_path, sector_path, industria_path):
        with open(simbolo_path, "rb") as f:
            simbolo_encoder = pickle.load(f)
        with open(sector_path, "rb") as f:
            sector_encoder = pickle.load(f)
        with open(industria_path, "rb") as f:
            industria_encoder = pickle.load(f)
        return simbolo_encoder, sector_encoder, industria_encoder

    @st.cache_data
    def cargar_datos():
        query_empresas = "SELECT * FROM empresas_sp500"
        empresas_df = pd.read_sql(query_empresas, engine)

        query_precios = """
        SELECT id_empresa, fecha, precio_apertura, precio_cierre, maximo, minimo, volumen 
        FROM precios_historicos
        """
        precios_df = pd.read_sql(query_precios, engine)
        return empresas_df, precios_df

    @st.cache_data
    def procesar_datos(empresas_df, precios_df, _simbolo_encoder):
        if 'simbolo_encoded' not in empresas_df.columns:
            empresas_df['simbolo_encoded'] = _simbolo_encoder.transform(empresas_df['simbolo'])

        precios_df['fecha'] = pd.to_datetime(precios_df['fecha'])
        resumen_precios = precios_df.groupby('id_empresa').agg({
            'precio_apertura': ['mean', 'std'],
            'precio_cierre': ['mean', 'std'],
            'maximo': ['mean', 'std'],
            'minimo': ['mean', 'std'],
            'volumen': ['mean', 'std']
        }).reset_index()

        resumen_precios.columns = [
            'id_empresa' if col[0] == 'id_empresa' else '_'.join(col).rstrip('_')
            for col in resumen_precios.columns]

        caracteristicas_empresas = empresas_df.filter(like='sector_').join(
            empresas_df.filter(like='industria_')
        ).join(empresas_df[['simbolo_encoded', 'id_empresa']])

        caracteristicas_combinadas = pd.merge(
            caracteristicas_empresas,
            resumen_precios,
            on='id_empresa',
            how='inner')

        return caracteristicas_combinadas

    simbolo_encoder_path = "simbolo_encoder.pkl"
    sector_encoder_path = "sector_encoder.pkl"
    industria_encoder_path = "industria_encoder.pkl"

    simbolo_encoder, sector_encoder, industria_encoder = cargar_encoders(
        simbolo_encoder_path, sector_encoder_path, industria_encoder_path)

    empresas_df, precios_df = cargar_datos()
    caracteristicas_combinadas = procesar_datos(empresas_df, precios_df, simbolo_encoder)

    num_clusters = st.sidebar.slider("Número de Clústeres", min_value=2, max_value=10, value=4, step=1)

    caracteristicas_finales = caracteristicas_combinadas.drop(columns=['id_empresa'])
    scaler = StandardScaler()
    caracteristicas_normalizadas = scaler.fit_transform(caracteristicas_finales)

    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    caracteristicas_combinadas['cluster'] = kmeans.fit_predict(caracteristicas_normalizadas)

    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(caracteristicas_normalizadas)

    pca_df = pd.DataFrame({
        'Componente Principal 1': pca_result[:, 0],
        'Componente Principal 2': pca_result[:, 1],
        'Clúster': caracteristicas_combinadas['cluster']})

    fig = px.scatter(
        pca_df,
        x='Componente Principal 1',
        y='Componente Principal 2',
        color=pca_df['Clúster'].astype(str),
        title=f'Clústeres (PCA) con {num_clusters} Clústeres',
        template='plotly_white')
    st.plotly_chart(fig)


st.subheader("Características de los Clústeres")

cluster_stats = caracteristicas_combinadas.groupby('cluster').mean()

st.write("Estadísticas promedio de cada clúster:")
st.dataframe(cluster_stats)
st.write("Desviación estándar de las características por clúster:")
st.dataframe(caracteristicas_combinadas.groupby('cluster').std())
st.subheader("Acciones en cada Clúster")
for cluster_id in caracteristicas_combinadas['cluster'].unique():
    st.write(f"### Clúster {cluster_id}")
    acciones = empresas_df.loc[
        empresas_df['id_empresa'].isin(
            caracteristicas_combinadas[caracteristicas_combinadas['cluster'] == cluster_id]['id_empresa']),
        ['simbolo', 'nombre_empresa']]
    st.write(acciones)

# Convertir estadísticas de clústeres a CSV
cluster_stats_csv = cluster_stats.to_csv().encode('utf-8')
std_dev_csv = caracteristicas_combinadas.groupby('cluster').std().to_csv().encode('utf-8')

st.download_button(
    label="Descargar Características Promedio (CSV)",
    data=cluster_stats_csv,
    file_name='cluster_stats.csv',
    mime='text/csv',
    key="descarga_promedio")

st.download_button(
    label="Descargar Desviaciones Estándar (CSV)",
    data=std_dev_csv,
    file_name='cluster_std_dev.csv',
    mime='text/csv',
    key="descarga_desviacion")

empresas_por_cluster = caracteristicas_combinadas[['cluster', 'id_empresa']].merge(
    empresas_df[['id_empresa', 'nombre_empresa', 'simbolo']],
    on='id_empresa')

empresas_cluster_csv = empresas_por_cluster.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Descargar Empresas por Clúster (CSV)",
    data=empresas_cluster_csv,
    file_name='empresas_por_cluster.csv',
    mime='text/csv',
    key="descarga_empresas")
