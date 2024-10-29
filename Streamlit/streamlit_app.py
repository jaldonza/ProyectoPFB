

import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(page_title="Yahoo Finance app" , layout="wide")

with st.container():
    st.title("Proyecto fin de bootcamp")
    st.header("Esto es una prueba")
    st.write("Información básica de las empresas del SP500")

 # Display Data
    df = pd.read_csv(filepath_or_buffer = "Streamlit/infoSP500.csv", sep = ",")
    
# Dinamic Data
    st.dataframe(df)

with st.container():
    st.header("Sigue siendo una prueba")

# Display data 2
    df2 = pd.read_csv(filepath_or_buffer = "Streamlit/infoSP500_API.csv", sep = ",")

# Dinamic Data Tabla 2 
    st.dataframe(df2)
