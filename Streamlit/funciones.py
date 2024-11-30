import pymysql
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Función para obtener la lista de nombres de empresa y símbolos desde la base de datos
def obtener_empresas():
    try:
        # Conectar a la base de datos
        connection = pymysql.connect(
            host="pfb.cp2wsq8yih32.eu-north-1.rds.amazonaws.com",
            user="admin",
            password="11jablum11",
            database="yfinance",
            port=3306
        )
        cursor = connection.cursor()

        # Consulta para obtener los nombres y símbolos de las empresas
        query = "SELECT nombre_empresa, simbolo FROM empresas_sp500"
        cursor.execute(query)
        empresas = cursor.fetchall()
        
        # Cerrar conexión
        cursor.close()
        connection.close()

        # Convertir el resultado en un diccionario {nombre_empresa: simbolo}
        return {empresa[0]: empresa[1] for empresa in empresas}

    except pymysql.MySQLError as e:
        st.error(f"Error al conectar a la base de datos para obtener nombres de empresas: {e}")
        return {}

# Función calcular ROI
import pymysql
import pandas as pd

# Datos de conexión a la base de datos
host = 'pfb.cp2wsq8yih32.eu-north-1.rds.amazonaws.com'
user = 'admin'
password = '11jablum11'
database = 'yfinance'
port = 3306

def calcular_roi(simbolo, fecha_compra, fecha_venta):
    try:
        # Conexión a la base de datos RDS
        db_connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        cursor = db_connection.cursor()

        # Obtener id_empresa para el símbolo
        query_id = "SELECT id_empresa FROM empresas_sp500 WHERE simbolo = %s"
        cursor.execute(query_id, (simbolo,))
        id_empresa = cursor.fetchone()

        if not id_empresa:
            print(f"[Error] No se encontró id_empresa para el símbolo: {simbolo}")
            return None, None
        id_empresa = id_empresa[0]

        # Consulta para el precio de compra (precio de cierre en la fecha de compra)
        query_compra = """
        SELECT precio_cierre
        FROM precios_historicos
        WHERE id_empresa = %s AND fecha = %s
        """
        cursor.execute(query_compra, (id_empresa, fecha_compra))
        resultado_compra = cursor.fetchone()

        # Consulta para el precio de venta (precio de cierre en la fecha de venta)
        query_venta = """
        SELECT precio_cierre
        FROM precios_historicos
        WHERE id_empresa = %s AND fecha = %s
        """
        cursor.execute(query_venta, (id_empresa, fecha_venta))
        resultado_venta = cursor.fetchone()

        # Cerrar el cursor y la conexión
        cursor.close()
        db_connection.close()

        # Verificar que se encontraron precios en ambas fechas
        if resultado_compra and resultado_venta:
            precio_compra = resultado_compra[0]
            precio_venta = resultado_venta[0]

            # Calcular ROI
            ganancia = precio_venta - precio_compra
            roi = (ganancia / precio_compra) * 100

            # Crear un DataFrame con los precios consultados
            precios_df = pd.DataFrame(
                {
                    'Fecha': [fecha_compra, fecha_venta],
                    'Precio Cierre': [precio_compra, precio_venta]
                }
            )
            return roi, precios_df

        else:
            print("No se encontraron precios de cierre para una o ambas fechas seleccionadas.")
            return None, None

    except pymysql.MySQLError as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None, None


import pymysql
import pandas as pd

def obtener_cotizaciones():
    try:
        # Conectar a la base de datos
        connection = pymysql.connect(
            host="pfb.cp2wsq8yih32.eu-north-1.rds.amazonaws.com",
            user="admin",
            password="11jablum11",
            database="yfinance",
            port=3306
        )

        # Crear cursor para ejecutar la consulta
        cursor = connection.cursor()

        # Consulta SQL con todas las columnas necesarias
        query = """
        SELECT 
            ph.fecha AS Date,
            ph.precio_apertura AS Open,
            ph.precio_cierre AS Close,
            ph.maximo AS High,
            ph.minimo AS Low,
            ph.volumen AS Volume,
            es.nombre_empresa AS Company
        FROM precios_historicos ph
        INNER JOIN empresas_sp500 es ON ph.id_empresa = es.id_empresa
        ORDER BY es.nombre_empresa, ph.fecha
        """

        # Ejecutar la consulta y almacenar los resultados
        cursor.execute(query)
        rows = cursor.fetchall()

        # Crear el DataFrame manualmente con las columnas necesarias
        cotizaciones_df = pd.DataFrame(rows, columns=["Date", "Open", "Close", "High", "Low", "Volume", "Company"])

        # Convertir la columna 'Date' a tipo datetime para facilitar el manejo posterior
        cotizaciones_df['Date'] = pd.to_datetime(cotizaciones_df['Date'])

        # Cerrar la conexión
        cursor.close()
        connection.close()

        return cotizaciones_df

    except pymysql.MySQLError as e:
        print(f"Error al conectar a la base de datos o ejecutar la consulta: {e}")
        return pd.DataFrame()


def graficar_precios_historicos(df, empresa_seleccionada):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Precio de Cierre'))
        fig.update_layout(title=f"Precios Históricos - {empresa_seleccionada}", xaxis_title="Fecha", yaxis_title="Precio de Cierre")
        return fig

def graficar_medias_moviles(df, empresa_seleccionada):
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Precio de Cierre'))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'], mode='lines', name='SMA 50'))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_200'], mode='lines', name='SMA 200'))
        fig.update_layout(title=f"Medias Móviles - {empresa_seleccionada}", xaxis_title="Fecha", yaxis_title="Precio")
        return fig

def graficar_rsi(df, empresa_seleccionada):
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], mode='lines', name='RSI'))
        fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Sobrecompra", annotation_position="top right")
        fig.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Sobreventa", annotation_position="bottom right")
        fig.update_layout(title=f"RSI (Relative Strength Index) - {empresa_seleccionada}", xaxis_title="Fecha", yaxis_title="RSI")
        return fig




def calcular_metricas(cotizaciones, tasa_libre_riesgo=0):
    """
    Calcula la volatilidad diaria, el Sharpe Ratio y el Sortino Ratio para una serie de cotizaciones.

    Parámetros:
    ----------
    cotizaciones : pandas.Series
        Serie de precios de cierre del activo.

    tasa_libre_riesgo : float, opcional, default=0
        Tasa libre de riesgo.

    Retorno:
    -------
    dict
        Diccionario con volatilidad diaria, Sharpe Ratio y Sortino Ratio.
    """
    # Calcular retornos diarios
    retornos = cotizaciones.pct_change().dropna()

    # Volatilidad diaria
    volatilidad = np.std(retornos)

    # Sharpe Ratio
    exceso_retornos = retornos - tasa_libre_riesgo / 252  # Ajustar tasa a diario
    sharpe = np.mean(exceso_retornos) / volatilidad if volatilidad > 0 else None

    # Sortino Ratio (solo usa retornos negativos)
    retornos_negativos = retornos[retornos < 0]
    downside_deviation = np.std(retornos_negativos) if not retornos_negativos.empty else None
    sortino = (np.mean(exceso_retornos) / downside_deviation) if downside_deviation else None

    return {
        "volatilidad_diaria": volatilidad,
        "sharpe_ratio": sharpe,
        "sortino_ratio": sortino
    }


import plotly.graph_objects as go

def crear_grafico_velas(dataframe, titulo="Gráfico de Velas"):
    """
    Genera un gráfico de velas utilizando Plotly.
    
    Parámetros:
        - dataframe: pandas.DataFrame que contiene las columnas necesarias para el gráfico.
        - titulo: Título del gráfico (opcional).
        
    Columnas requeridas en el DataFrame:
        - Date: Fecha (datetime64)
        - Open: Precio de apertura
        - High: Precio máximo
        - Low: Precio mínimo
        - Close: Precio de cierre
    
    Retorna:
        - fig: Objeto Plotly Figure con el gráfico de velas.
    """
    try:
        # Verificar si las columnas necesarias están en el DataFrame
        columnas_requeridas = ["Date", "Open", "High", "Low", "Close"]
        for columna in columnas_requeridas:
            if columna not in dataframe.columns:
                raise ValueError(f"La columna '{columna}' no está presente en el DataFrame.")

        # Crear el gráfico de velas
        fig = go.Figure(data=[go.Candlestick(
            x=dataframe['Date'],
            open=dataframe['Open'],
            high=dataframe['High'],
            low=dataframe['Low'],
            close=dataframe['Close']
        )])

        # Configuración del diseño
        fig.update_layout(
            title=titulo,
            xaxis_title="Fecha",
            yaxis_title="Precio",
            xaxis_rangeslider_visible=False
        )
        return fig
    except Exception as e:
        print(f"Error al crear el gráfico de velas: {e}")
        return None
