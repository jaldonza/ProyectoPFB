import yfinance as yf
import pandas as pd
from datetime import datetime
import uuid

def SP_500_Stockdata(tickers, start_date='2000-01-01'):
    """
    Extrae datos históricos de precios de las empresas del S&P 500 desde Yahoo Finance,
    combinándolos en un único DataFrame con un ID único para cada empresa y una columna de timestamp
    para indicar la fecha de extracción. Incluye el nombre completo de cada empresa.

    Args:
        tickers (list): Lista de tickers de empresas.
        start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'. Por defecto es '2000-01-01'.
        
    Returns:
        pd.DataFrame: Un DataFrame con los datos históricos de precios de las empresas del S&P 500,
                      incluyendo el ticker, un ID único, el nombre de la empresa y el timestamp de extracción.
    """
    end_date = datetime.now().strftime('%Y-%m-%d')
    extraction_timestamp = datetime.now()
    
    all_data = pd.DataFrame()

    for ticker in tickers:

        company_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, ticker))
        
        stock_info = yf.Ticker(ticker).info
        company_name = stock_info.get('longName', 'N/A') 

        stock_data = yf.download(ticker, start=start_date, end=end_date)

        stock_data['Ticker'] = ticker
        stock_data['Company_ID'] = company_id
        stock_data['Company_Name'] = company_name
        stock_data['Extraction_Timestamp'] = extraction_timestamp

        all_data = pd.concat([all_data, stock_data])
    
    return all_data


def sp500_sector_industria(tickers):
    """
    Obtiene información de nombre, sector e industria para una lista de empresas del S&P 500 y 
    la almacena en un DataFrame de pandas. Incluye un ID único y un timestamp de extracción.
    
    Args:
        tickers (list): Lista de tickers de empresas.
        delay (float): Tiempo de espera entre solicitudes para evitar limitaciones del servidor.
        
    Returns:
        pd.DataFrame: Un DataFrame que contiene un ID único, el ticker, nombre de la empresa,
                      sector, industria y un timestamp de extracción de cada empresa.
    """
    data = {
        'ID': [], 
        'Ticker': [], 
        'Company Name': [], 
        'Sector': [], 
        'Industry': [], 
        'Timestamp': []
    }
    
    extraction_time = datetime.now()
    

    for ticker in tickers:
        company_name = 'Información No Disponible'
        sector = 'Información No Disponible'
        industry = 'Información No Disponible'
        
        try:
            info = yf.Ticker(ticker).info
            company_name = info.get('longName', 'Información No Disponible')
            sector = info.get('sector', 'Información No Disponible')
            industry = info.get('industry', 'Información No Disponible')
        except:
            pass  

        data['ID'].append(str(uuid.uuid4()))  
        data['Ticker'].append(ticker)
        data['Company Name'].append(company_name)
        data['Sector'].append(sector)
        data['Industry'].append(industry)
        data['Timestamp'].append(extraction_time)  
    
    return pd.DataFrame(data)