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

        # Consulta para el precio de compra (precio de cierre en la fecha de compra)
        query_compra = """
        SELECT precio_cierre
        FROM precios_historicos
        WHERE id_empresa = %s AND fecha = %s
        """
        cursor.execute(query_compra, (simbolo, fecha_compra))
        resultado_compra = cursor.fetchone()

        # Consulta para el precio de venta (precio de cierre en la fecha de venta)
        query_venta = """
        SELECT precio_cierre
        FROM precios_historicos
        WHERE id_empresa = %s AND fecha = %s
        """
        cursor.execute(query_venta, (simbolo, fecha_venta))
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
            st.warning("No se encontraron precios de cierre para una o ambas fechas seleccionadas.")
            return None, None

    except pymysql.MySQLError as err:
        st.error(f"Error al conectar a la base de datos: {err}")
        return None, None
