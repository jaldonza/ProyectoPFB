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
def calcular_roi(simbolo, fecha_compra, fecha_venta):
    try:
        # Conexión a la base de datos RDS
        db_connection = pymysql.connect(
            host="pfb.cp2wsq8yih32.eu-north-1.rds.amazonaws.com",
            user="admin",
            password="11jablum11",
            database="yfinance",
            port=3306
        )
        cursor = db_connection.cursor()

          # Obtener id_empresa para el símbolo
        query_id = "SELECT id_empresa FROM empresas_sp500 WHERE simbolo = %s"
        cursor.execute(query_id, (simbolo,))
        id_empresa = cursor.fetchone()
        
        if not id_empresa:
            print(f"No se encontró id_empresa para el símbolo: {simbolo}")
            return None, None
        id_empresa = id_empresa[0]

        # Asegurar que las fechas están en el formato correcto
        fecha_inicio = pd.to_datetime(fecha_inicio).strftime('%Y-%m-%d')
        fecha_fin = pd.to_datetime(fecha_fin).strftime('%Y-%m-%d')

        # Consulta para obtener los precios de cierre en las fechas de inicio y fin
        query_precios = """
        SELECT fecha, precio_cierre
        FROM precios_historicos
        WHERE id_empresa = %s AND fecha BETWEEN %s AND %s
        ORDER BY fecha ASC
        """
        cursor.execute(query_precios, (id_empresa, fecha_inicio, fecha_fin))
        precios = cursor.fetchall()

        # Cerrar la conexión
        cursor.close()
        connection.close()

        # Verificar si se obtuvieron precios en el rango de fechas
        if len(precios) < 2:
            print("No se encontraron suficientes datos en el rango de fechas seleccionado.")
            return None, None

        # Precio inicial y final para el cálculo de ROI
        precio_inicial = precios[0][1]
        precio_final = precios[-1][1]
        
        # Calcular ROI
        roi = (precio_final - precio_inicial) / precio_inicial * 100

        # Crear un DataFrame con los precios consultados
        precios_df = pd.DataFrame(precios, columns=['Fecha', 'Precio Cierre'])
        return roi, precios_df

    except pymysql.MySQLError as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None, None
    except Exception as e:
        print(f"Error general: {e}")
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




