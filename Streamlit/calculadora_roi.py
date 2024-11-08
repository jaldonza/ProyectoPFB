import mysql.connector
import pandas as pd

def calcular_roi(simbolo, fecha_inicio, fecha_fin):
    # Conexión a la base de datos
    db_connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",               # Cambia por tu usuario de MySQL
        password="11jablum11",     # Cambia por tu contraseña de MySQL
        database="yfinance"
    )
    cursor = db_connection.cursor()

    # Consulta SQL para obtener el precio inicial y final en el periodo
    query = """
    SELECT fecha, precio_cierre
    FROM precios_historicos
    WHERE id_empresa = (SELECT id_empresa FROM empresas_sp500 WHERE simbolo = %s)
      AND fecha BETWEEN %s AND %s
    ORDER BY fecha ASC;
    """
    
    cursor.execute(query, (simbolo, fecha_inicio, fecha_fin))
    precios = cursor.fetchall()

    # Cerrar conexión
    cursor.close()
    db_connection.close()

    # Verifica si se obtuvieron precios en el rango de fechas
    if len(precios) < 2:
        return None, None  # No hay datos suficientes en el rango de fechas

    # Precio inicial y final
    precio_inicial = precios[0][1]
    precio_final = precios[-1][1]
    
    # Calcular ROI
    roi = (precio_final - precio_inicial) / precio_inicial * 100

    return roi, pd.DataFrame(precios, columns=['Fecha', 'Precio Cierre'])
