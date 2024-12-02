import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from funciones import obtener_cotizaciones, graficar_precios_historicos, graficar_medias_moviles, graficar_rsi, calcular_metricas

# Configuración de la aplicación Streamlit
st.set_page_config(page_title="Yahoo Finance App", layout="wide")

# Barra lateral de navegación
st.sidebar.title("Navegación")
pagina = st.sidebar.radio("Ir a", [
    "Landing Page",
    "Análisis Exploratorio",
    "Dashboard Financiero",
    "Análisis de Métricas Financieras",
    "Modelo de Clustering",
    "Base de Datos",
    "About Us"
])

# Página de inicio
if pagina == "Landing Page":
    st.title("Yahoo Finance - Proyecto Final")
    st.image("Streamlit/Yahoo!_Finance_image.png", use_container_width=True)
    st.header("Descripción General del Proyecto")
    st.write("""
    Bienvenido a nuestra aplicación de análisis financiero diseñada para trabajar con datos del S&P500. En este proyecto podrás explorar:
    
    - **Análisis Exploratorio:** Visualiza gráficos históricos y analiza la correlación entre activos.
    - **Dashboard Financiero:** Unifica toda la información en un tablero dinámico (Power BI).
    - **Análisis de Métricas Financieras:** Calcula métricas clave como volatilidad diaria, ratios de Sharpe y Sortino.
    - **About Us:** Conoce al equipo y descubre cómo creamos esta aplicación.
    """)

# Análisis Exploratorio
elif pagina == "Análisis Exploratorio":
    st.header("Análisis Exploratorio")
    # Introducción a la sección
    st.write("""
    En esta sección puedes explorar visualizaciones clave y relaciones entre activos del S&P500. 
    Estas herramientas permiten analizar tendencias, correlaciones y comportamientos históricos para una mejor toma de decisiones financieras.
    """)
    cotizaciones_df = obtener_cotizaciones()

    # Cargar datos de cotización
    cotizaciones_df = obtener_cotizaciones()

    # Verificar y convertir la columna 'Date' a datetime si no lo es
    if cotizaciones_df['Date'].dtype != 'datetime64[ns]':
        cotizaciones_df['Date'] = pd.to_datetime(cotizaciones_df['Date'])

    # Dropdown para seleccionar la empresa
    empresas = cotizaciones_df['Company'].unique()
    empresa_seleccionada = st.selectbox("Seleccione la empresa", empresas)

    # Seleccionar el rango de fechas
    min_date = cotizaciones_df['Date'].min()
    max_date = cotizaciones_df['Date'].max()
    fecha_inicio = st.date_input("Fecha de inicio", value=min_date, min_value=min_date, max_value=max_date)
    fecha_fin = st.date_input("Fecha de fin", value=max_date, min_value=min_date, max_value=max_date)

    # Convertir fechas seleccionadas a datetime si no lo están
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    # Validar que fecha_inicio no sea posterior a fecha_fin
    if fecha_inicio > fecha_fin:
        st.error("La fecha de inicio no puede ser posterior a la fecha de fin.")
    else:
        # Filtrar los datos para el rango de fechas
        df = cotizaciones_df[
            (cotizaciones_df['Company'] == empresa_seleccionada) & 
            (cotizaciones_df['Date'] >= fecha_inicio) & 
            (cotizaciones_df['Date'] <= fecha_fin)
        ]

        # Seleccionar el tipo de gráfico
        tab = st.selectbox("Seleccione una visualización", ["Precios Históricos", "Medias Móviles", "RSI"])
    
        # Mostrar gráfico según la pestaña seleccionada
        if not df.empty:
            if tab == "Precios Históricos":
                st.plotly_chart(graficar_precios_historicos(df, empresa_seleccionada))
                st.write("""
                **Precios Históricos:**
                Este gráfico muestra la evolución histórica de los precios de cierre del activo seleccionado.
                Es útil para identificar tendencias generales y períodos de alta o baja volatilidad.
                """)
            elif tab == "Medias Móviles":
                st.plotly_chart(graficar_medias_moviles(df, empresa_seleccionada))
                st.write("""
                **Medias Móviles Simples (SMA):**
                - La SMA50 (50 días) es una medida de corto plazo que suaviza los movimientos diarios del precio para identificar tendencias inmediatas.
                - La SMA200 (200 días) es una medida de largo plazo que muestra la tendencia general de un activo.
                
                **Cómo Interpretar:**
                - Cuando la SMA50 cruza por encima de la SMA200, puede ser una señal de compra (cambio a tendencia alcista).
                - Cuando la SMA50 cruza por debajo de la SMA200, puede ser una señal de venta (cambio a tendencia bajista).
                """)
            elif tab == "RSI":
                st.plotly_chart(graficar_rsi(df, empresa_seleccionada))
                st.write("""
                **Índice de Fuerza Relativa (RSI):**
                - El RSI mide la velocidad y el cambio de los movimientos de precios.
                - Escala de 0 a 100.
                
                **Cómo Interpretar:**
                - Un RSI por encima de 70 indica un activo sobrecomprado (potencial corrección o reversión a la baja).
                - Un RSI por debajo de 30 indica un activo sobrevendido (potencial rebote o recuperación).
                
                **Uso Práctico:**
                Ayuda a identificar condiciones extremas del mercado y posibles puntos de entrada/salida.
                """)
        else:
            st.warning(f"No hay datos disponibles para {empresa_seleccionada} en el rango de fechas seleccionado.")

    # Subsección: Análisis de correlación
    st.subheader("Análisis de Correlación entre Activos")
    st.write("""
    Este análisis muestra cómo se relacionan los precios de diferentes activos. 
    Una alta correlación positiva indica que los activos tienden a moverse en la misma dirección, mientras que una correlación negativa indica movimientos opuestos.
    """)
    activo_principal = st.selectbox("Seleccione el activo principal", empresas)
    activos_comparar = st.multiselect("Seleccione hasta 4 activos para comparar", empresas, default=empresas[:4])

    if activo_principal and len(activos_comparar) > 0:
        activos_seleccionados = [activo_principal] + activos_comparar
        df_seleccionados = cotizaciones_df[cotizaciones_df['Company'].isin(activos_seleccionados)]
        precios_df = df_seleccionados.pivot(index='Date', columns='Company', values='Close')
        correlacion = precios_df.corr()

        st.subheader("Matriz de Correlación")
        st.dataframe(correlacion)
        st.write("""
        **Interpretación:**
        - Valores cercanos a 1 indican una relación positiva fuerte entre los activos.
        - Valores cercanos a -1 indican una relación negativa fuerte.
        - Valores cercanos a 0 indican una relación débil o inexistente.
        """)

        st.subheader("Mapa de Calor de Correlación")
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=correlacion.values,
            x=correlacion.columns,
            y=correlacion.index,
            colorscale='Viridis',
            colorbar=dict(title="Correlación")
        ))
        fig_heatmap.update_layout(title="Mapa de Calor de Correlación", xaxis_title="Activos", yaxis_title="Activos")
        st.plotly_chart(fig_heatmap)
    # Explicaciones al final
    st.subheader("Explicaciones")
    st.write("""
    ### Medias Móviles (SMA)
    Las medias móviles suavizan las fluctuaciones de precios para identificar tendencias más fácilmente. 
    - **Interpretación:** Cuando el precio actual está por encima de una media móvil, puede indicar una tendencia alcista.
    - **SMA-50:** Utilizada para analizar tendencias de corto plazo.
    - **SMA-200:** Ayuda a identificar tendencias de largo plazo.

    ### RSI (Índice de Fuerza Relativa)
    El RSI mide la fuerza de las recientes ganancias frente a las recientes pérdidas en un rango de tiempo.
    - **Interpretación:** Un RSI superior a 70 puede indicar una acción sobrecomprada, mientras que un RSI inferior a 30 puede señalar una acción sobrevendida.
    
    ### Análisis de Correlación
    Evalúa cómo los movimientos de diferentes activos están relacionados.
    - **Interpretación:** Una correlación cercana a 1 indica una relación directa fuerte, mientras que una correlación cercana a -1 indica una relación inversa fuerte.
    """)
# Dashboard Financiero
elif pagina == "Dashboard Financiero":
    st.header("Dashboard Financiero")
    # Configuración del iframe de Power BI
    powerbi_width = 1920
    powerbi_height = 1080  # Ajusta según tu preferencia

    powerbi_iframe = f"""
        <iframe title="TableroYfinance - grupo c" 
            width="{powerbi_width}" 
            height="{powerbi_height}" 
            src="https://app.powerbi.com/view?r=eyJrIjoiZTA0ODYwODgtNmQyMC00MzZlLWJiNDYtMTQ3YmM0MTYzODQ2IiwidCI6IjVlNzNkZTM1LWU4MjUtNGVkNS1iZTIyLTg4NTYzNTI3MDkxZSIsImMiOjl9&pageName=9cd2d53aa30bd0c09883" 
            frameborder="0" 
            allowFullScreen="true"></iframe>
        """

    # Renderizar el iframe en Streamlit
    st.components.v1.html(powerbi_iframe, height=powerbi_height, width=powerbi_width)   
    # Explicaciones del tablero
    st.header("Descripción del Tablero Power BI")
    st.write("""
    Este tablero interactivo en Power BI permite analizar el desempeño del índice S&P500 y las empresas que lo conforman mediante varias páginas:
    """)

    st.subheader("**1. Portada - Análisis General del Índice**")
    st.write("""
    La portada ofrece un análisis general del índice S&P500, destacando:
    - **Número de empresas y sectores** presentes en el análisis.
    - **Volumen de transacciones** durante los años analizados.
    - **Número de años** incluidos en el análisis.
    - **Gráfico de evolución del S&P500** para observar tendencias generales.
    - **Valoración por sectores** para identificar los sectores más destacados en términos de crecimiento y rendimiento.
    """)

    st.subheader("**2. Dashboard Financiero por Empresa**")
    st.write("""
    En esta página puedes analizar:
    - **Evolución de un valor específico** seleccionado por el usuario.
    - **Indicadores técnicos:**
    - **RSI (Índice de Fuerza Relativa):** Indica si un valor está sobrecomprado (por encima de 70) o sobrevendido (por debajo de 30).
    - **SMA (Media Móvil Simple):** 
        - **SMA 50:** Indica la tendencia a corto plazo.
        - **SMA 200:** Muestra la tendencia a largo plazo.
    - **Interpretación:**
        - Si el precio está por encima del SMA 200, generalmente se considera que el valor está en una tendencia alcista.
        - El cruce de SMA 50 por encima o por debajo de SMA 200 puede indicar señales de compra o venta.
    """)

    st.subheader("**3. Análisis de Rentabilidad por Empresa**")
    st.write("""
    Esta página permite analizar la rentabilidad de una empresa entre dos fechas seleccionadas por el usuario:
    - **Precio de apertura y cierre** para las fechas seleccionadas.
    - **ROI (Retorno de la Inversión):** Calcula el rendimiento porcentual en el periodo seleccionado.
    - **Evolución del rendimiento:**
    - **Diario:** Cambios porcentuales diarios en el precio.
    - **Mensual:** Rendimientos promedio mensuales.
    - **Anual:** Tendencias de rendimiento anual.
    
    **Conceptos Clave:**
    - **ROI (Retorno de la Inversión):** Una métrica importante para evaluar la eficiencia de una inversión.
    - **Interpretación:** Un ROI positivo indica ganancias; un ROI negativo refleja pérdidas en el periodo analizado.
    """)

    st.subheader("**4. Análisis de Rentabilidad Sectorial**")
    st.write("""
    Permite analizar la rentabilidad a nivel de sector:
    - Selección de un **sector** y un rango de fechas.
    - Desglose por:
    - **Sector.**
    - **Industria.**
    - **Empresas.**
    - Visualización de las métricas:
    - **Precio de apertura y cierre.**
    - **ROI del sector, industria y empresas.**
    - **Rendimientos anuales, mensuales y diarios.**
    """)

    st.subheader("**5. Análisis de Momentum**")
    st.write("""
    El análisis de momentum mide la aceleración o desaceleración del precio de un activo en el tiempo.
    - Un momentum positivo indica una tendencia alcista.
    - Un momentum negativo refleja una tendencia bajista.
    - **Interpretación:** Permite anticipar posibles cambios de tendencia y oportunidades de compra o venta.
    """)

    st.subheader("**6. Análisis de Ratios de Riesgo y Rendimiento**")
    st.write("""
    En esta página se analizan las siguientes métricas:
    - **Drawdown Máximo:** Muestra la pérdida máxima desde un pico hasta un valle.
    - **Calmar Ratio:** Relación entre el rendimiento y el drawdown máximo.
    - **Sharpe Ratio:** Indica la relación entre la rentabilidad y la volatilidad. Un Sharpe Ratio positivo y alto sugiere una inversión eficiente.
    - **Sortino Ratio:** Similar al Sharpe Ratio, pero ajustado para medir el rendimiento frente a riesgos negativos.
    """)

    st.subheader("**7. Comparador de Calmar Ratio por Empresa**")
    st.write("""
    Permite comparar el Calmar Ratio para todas las empresas en el análisis.
    - Ayuda a identificar qué empresas tienen un mejor rendimiento ajustado por el riesgo máximo asumido.
    """)

# Análisis de Métricas Financieras
elif pagina == "Análisis de Métricas Financieras":
    st.header("Análisis de Métricas Financieras")
# Introducción a la sección
    st.write("""
    En esta sección puedes calcular y analizar métricas financieras clave, como volatilidad diaria, ratio de Sharpe y ratio de Sortino. 
    Estas métricas ayudan a evaluar el rendimiento y el riesgo de un activo financiero.
    """)

    # Cargar datos de cotización
    cotizaciones_df = obtener_cotizaciones()

    # Asegurar que la columna 'Date' sea del tipo datetime
    if cotizaciones_df['Date'].dtype != 'datetime64[ns]':
        cotizaciones_df['Date'] = pd.to_datetime(cotizaciones_df['Date'])

    # Selección de activo
    empresas = cotizaciones_df['Company'].unique()
    empresa_seleccionada = st.selectbox("Seleccione la empresa", empresas)

    # Selección de periodo
    min_date = cotizaciones_df['Date'].min()
    max_date = cotizaciones_df['Date'].max()
    fecha_inicio = st.date_input("Fecha de inicio", value=min_date, min_value=min_date, max_value=max_date)
    fecha_fin = st.date_input("Fecha de fin", value=max_date, min_value=min_date, max_value=max_date)

    # Convertir fechas seleccionadas a datetime
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    # Validar el rango de fechas
    if fecha_inicio > fecha_fin:
        st.error("La fecha de inicio no puede ser posterior a la fecha de fin.")
    else:
        # Filtrar los datos para el rango de fechas seleccionado
        df_filtrado = cotizaciones_df[
            (cotizaciones_df['Company'] == empresa_seleccionada) &
            (cotizaciones_df['Date'] >= fecha_inicio) &
            (cotizaciones_df['Date'] <= fecha_fin)
        ]

        # Verificar si hay datos después del filtrado
        if not df_filtrado.empty:
            # Calcular métricas
            cotizaciones = df_filtrado['Close']
            metricas = calcular_metricas(cotizaciones)

            # Mostrar resultados
            st.subheader(f"Métricas para {empresa_seleccionada} del {fecha_inicio.date()} al {fecha_fin.date()}")
            st.write(f"**Volatilidad diaria**: {metricas['volatilidad_diaria']:.4f}")
            st.write(f"**Sharpe Ratio**: {metricas['sharpe_ratio']:.4f}" if metricas['sharpe_ratio'] else "Sharpe Ratio no calculable.")
            st.write(f"**Sortino Ratio**: {metricas['sortino_ratio']:.4f}" if metricas['sortino_ratio'] else "Sortino Ratio no calculable.")
 # Explicaciones de las métricas
            st.write("""
            ### Explicaciones de las métricas:
            - **Volatilidad diaria:** Mide cuánto fluctúan los precios del activo diariamente. Una alta volatilidad indica mayor riesgo, pero también mayores oportunidades de retorno.
            - **Sharpe Ratio:** Evalúa el rendimiento ajustado al riesgo del activo. 
              - Un Sharpe Ratio positivo indica que el activo ofrece un retorno superior a la tasa libre de riesgo ajustado por su volatilidad.
              - Valores típicos: 
                - > 1.0: Bueno.
                - > 2.0: Muy bueno.
                - > 3.0: Excelente.
            - **Sortino Ratio:** Similar al Sharpe Ratio, pero considera únicamente el riesgo asociado a retornos negativos.
              - Es más adecuado para evaluar activos en los que los inversores quieren evitar pérdidas en lugar de volatilidad general.
              - Un Sortino Ratio alto indica que el activo ofrece un buen retorno por unidad de riesgo de pérdida.
            """)
            # Graficar retornos diarios
            retornos_diarios = cotizaciones.pct_change().dropna()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=retornos_diarios.index, y=retornos_diarios, mode='lines', name="Retornos Diarios"))
            fig.update_layout(title="Evolución de Retornos Diarios", xaxis_title="Fecha", yaxis_title="Retornos Diarios")
            st.plotly_chart(fig)
        else:
            st.warning(f"No se encontraron datos para {empresa_seleccionada} entre {fecha_inicio.date()} y {fecha_fin.date()}.")
# Base de Datos
elif pagina == "Base de Datos":
    st.header("Arquitectura de la Base de Datos")

    # Mostrar la imagen del diagrama de la base de datos
    st.image("Streamlit/diagrama_bbdd.png", use_column_width=True, caption="Diagrama de la Base de Datos")

    # Explicación del diseño de la base de datos
    st.subheader("Estructura y Creación")
    st.write("""
    La base de datos utilizada en este proyecto fue diseñada para almacenar información financiera del S&P500 y proporcionar soporte para los análisis presentados en esta aplicación.
    
    **Tablas principales:**
    - **empresas_sp500**: Contiene información básica de las empresas, como su símbolo, nombre, sector, industria y capitalización de mercado.
    - **precios_historicos**: Almacena los precios históricos de las acciones, incluyendo la fecha, precios de apertura y cierre, máximos y mínimos diarios, así como el volumen negociado.
    - **portafolios_usuarios**: Permite a los usuarios crear portafolios personalizados y almacenar información relevante.
    - **portafolio_empresas**: Relaciona los portafolios de los usuarios con las empresas, incluyendo la cantidad de acciones y precios de compra.
    - **indicadores_sp500**: Almacena cálculos de indicadores financieros como medias móviles, RSI, y volatilidad.

    **Proceso de creación:**
    1. **Diseño del esquema:** El diagrama presentado arriba fue diseñado utilizando una herramienta de modelado de bases de datos.
    2. **Creación de la base de datos:** Se utilizó MySQL para implementar el esquema en un servidor RDS de AWS.
    3. **Población de datos:** Los datos fueron recolectados de fuentes como Yahoo Finance, y almacenados en las tablas correspondientes.

    **Relaciones entre tablas:**
    - La tabla `precios_historicos` se relaciona con `empresas_sp500` a través de la clave primaria `id_empresa`.
    - La tabla `portafolio_empresas` relaciona los portafolios de usuarios con las empresas correspondientes.
    """)

    st.write("Este diseño asegura flexibilidad y escalabilidad, permitiendo almacenar grandes volúmenes de datos y realizar consultas eficientes para el análisis.")
# Modelo de CLusterig
elif pagina == "Modelo de Clustering":
    st.header("Modelo de Clustering")
    st.write("""
    en desarrollo...
    """)


# About Us
elif pagina == "About Us":
    st.header("About Us")
    st.write("""
    Esta aplicación fue creada como parte de un proyecto final para explorar el análisis financiero utilizando Python y Streamlit. 

    **Tecnologías Utilizadas:**
    - Python (pandas, numpy, plotly, matplotlib, yfinance)
    - Streamlit
    - MySQL (Base de datos en AWS RDS)
    - Power BI

    **Proceso de Creación:**
    1. Diseño de la base de datos para almacenar información financiera.
    2. Creación de funciones para conectar y analizar datos.
    3. Construcción de la aplicación interactiva utilizando Streamlit.
    4. Integración de Power BI para análisis avanzado.
    
    **Equipo:**
    - [Javier Aldonza](https://www.linkedin.com/in/javier-aldonza/)
    - [Roberto Gonzalez Álvarez](https://www.linkedin.com/in/roberto-gonz%C3%A1lez-%C3%A1lvarez-959552140/?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app)
    - [Khalid el Afi Guerban](https://www.linkedin.com/in/khalid-el-afi-guerban-95212a270)

    ¡Gracias por explorar nuestra aplicación!
    """)

# Pie de página
st.sidebar.write("Aplicación creada con Streamlit")





