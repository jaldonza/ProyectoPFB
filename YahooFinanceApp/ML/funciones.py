import pymysql
import pandas as pd
import streamlit as st

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

        # Consulta SQL
        query = """
        SELECT ph.fecha AS Date, ph.precio_cierre AS Close, es.nombre_empresa AS Company
        FROM precios_historicos ph
        INNER JOIN empresas_sp500 es ON ph.id_empresa = es.id_empresa
        ORDER BY es.nombre_empresa, ph.fecha
        """

        # Ejecutar la consulta y almacenar los resultados
        cursor.execute(query)
        rows = cursor.fetchall()

        # Crear el DataFrame manualmente
        cotizaciones_df = pd.DataFrame(rows, columns=["Date", "Close", "Company"])

        # Cerrar la conexión
        cursor.close()
        connection.close()

        return cotizaciones_df

    except pymysql.MySQLError as e:
        print(f"Error al conectar a la base de datos o ejecutar la consulta: {e}")
        return pd.DataFrame()




