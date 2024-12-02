import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
import mysql.connector

# Configuración de la base de datos
st.sidebar.subheader("Configuración de Base de Datos")
db_host = st.sidebar.text_input("Host de la Base de Datos", value="127.0.0.1")
db_user = st.sidebar.text_input("Usuario", value="root")
db_password = st.sidebar.text_input("Contraseña", type="password")
db_name = st.sidebar.text_input("Nombre de la Base de Datos", value="yfinance")

# Conectar y cargar datos
if st.sidebar.button("Conectar y Cargar Datos"):
    try:
        # Conectar a la base de datos
        conexion = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        st.success("Conexión exitosa a la base de datos")

        # Consulta SQL
        query = "SELECT precios_historicos.precio_apertura,precios_historicos.precio_cierre,precios_historicos.maximo,precios_historicos.minimo,precios_historicos.volumen,empresas_sp500.sector,empresas_sp500.industria FROM precios_historicos INNER JOIN empresas_sp500 ON precios_historicos.id_empresa = empresas_sp500.id_empresa;"
        empresas_df = pd.read_sql(query, conexion)

        st.write("Datos cargados desde la base de datos:")
        st.dataframe(empresas_df.head())

        # Clustering con K-Means
        columnas_numericas = ['precio_apertura', 'precio_cierre', 'maximo', 'minimo', 'volumen']
        X = empresas_df[columnas_numericas].dropna()

        st.sidebar.subheader("Configuración de K-Means")
        n_clusters = st.sidebar.slider("Número de Clusters (K)", min_value=2, max_value=10, value=5, step=1)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X)

        empresas_df['Cluster'] = clusters

        st.write("Clustering completado. Vista previa de los clusters:")
        st.dataframe(empresas_df[['Cluster'] + columnas_numericas].head())

        # Clasificación con RandomForest
        st.sidebar.subheader("Entrenar Modelo de Clasificación")
        max_depth = st.sidebar.slider("Profundidad Máxima del Árbol", min_value=2, max_value=20, value=10, step=1)
        n_estimators = st.sidebar.slider("Número de Estimadores", min_value=10, max_value=100, value=20, step=10)

        y = empresas_df['Cluster']
        X_clasificacion = X

        modelo = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
        modelo.fit(X_clasificacion, y)

        predicciones = modelo.predict(X_clasificacion)

        st.write("Resultados del modelo de clasificación:")
        empresas_df['Predicción_Cluster'] = predicciones
        st.dataframe(empresas_df[['Cluster', 'Predicción_Cluster'] + columnas_numericas].head())

        # Cerrar la conexión
        conexion.close()
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")

# Nota final
st.sidebar.info("Desarrollado con Streamlit")
