import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from funciones import obtener_cotizaciones, graficar_precios_historicos, graficar_medias_moviles, graficar_rsi, calcular_metricas, graficar_velas

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
    # Estilo y título principal con animación de billetes
    st.markdown("""
    <style>
        .title {
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .subtitle {
            font-size: 1.5em;
            text-align: center;
            color: #34495e;
            margin-bottom: 30px;
        }
        .section {
            margin-top: 20px;
            margin-bottom: 30px;
        }
        .section h3 {
            color: #3498db;
            margin-bottom: 10px;
        }
        .section p {
            font-size: 1.1em;
            color: #7f8c8d;
        }
        .highlight {
            background-color: #ecf0f1;
            border-radius: 10px;
            padding: 15px;
            margin-top: 10px;
        }
        @keyframes fall {
            0% { transform: translateY(-200px) rotate(0deg); opacity: 1; }
            100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
        }
        .falling-money {
            position: fixed;
            width: 50px;
            height: 25px;
            background-image: url('https://i.imgur.com/2wWeygR.png');
            background-size: cover;
            animation: fall linear infinite;
        }
    </style>
    <div class="title">Yahoo Finance - Proyecto Final</div>
    <div class="subtitle">Descubre el análisis financiero del S&P500 de forma interactiva</div>
    """, unsafe_allow_html=True)

    # Generar el efecto de billetes cayendo
    st.markdown("""
    <script>
        const createMoney = () => {
            const money = document.createElement('div');
            money.classList.add('falling-money');
            money.style.left = Math.random() * window.innerWidth + 'px';
            money.style.animationDuration = Math.random() * 3 + 2 + 's';
            document.body.appendChild(money);
            setTimeout(() => { money.remove(); }, 5000);
        };
        setInterval(createMoney, 200);
    </script>
    """, unsafe_allow_html=True)

    # Imagen principal más pequeña
    st.image("Streamlit/Yahoo!_Finance_image.png", use_container_width=True)


    # Descripción general del proyecto
    st.markdown("""
    <div class="section">
        <h3>Descripción General del Proyecto</h3>
        <p>
            Bienvenido a nuestra aplicación de análisis financiero diseñada para trabajar con datos del S&P500. 
            Este proyecto combina potentes herramientas de visualización e integración con bases de datos para 
            ofrecer una experiencia interactiva y profesional.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Funcionalidades destacadas
    st.markdown("""
    <div class="section">
        <h3>Principales Funcionalidades</h3>
        <div class="highlight">
            <ul>
                <li><b>Análisis Exploratorio:</b> Visualiza gráficos históricos y analiza la correlación entre activos.</li>
                <li><b>Dashboard Financiero:</b> Unifica toda la información en un tablero dinámico (Power BI).</li>
                <li><b>Análisis de Métricas Financieras:</b> Calcula métricas clave como volatilidad diaria, ratios de Sharpe y Sortino.</li>
                <li><b>About Us:</b> Conoce al equipo y descubre cómo creamos esta aplicación.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Motivación del proyecto
    st.markdown("""
    <div class="section">
        <h3>¿Por Qué Este Proyecto?</h3>
        <p>
            El mercado financiero es un entorno complejo y dinámico. Este proyecto fue desarrollado con el objetivo de
            ofrecer una herramienta práctica para inversores, analistas y entusiastas que desean explorar y analizar 
            los datos financieros del índice S&P500.
        </p>
        <p>
            Gracias a tecnologías como <b>Streamlit</b>, <b>Power BI</b>, y <b>Python</b>, hemos logrado construir 
            una solución que simplifica el análisis financiero de manera visual e intuitiva.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Llamado a la acción
    st.markdown("""
    <div class="section" style="text-align: center;">
        <h3>¡Explora el Proyecto Ahora!</h3>
        <p>
            Usa la barra de navegación a la izquierda para acceder a las distintas secciones y sumérgete en el 
            análisis financiero como nunca antes.
        </p>
    </div>
    """, unsafe_allow_html=True)



# Análisis Exploratorio
elif pagina == "Análisis Exploratorio":
    st.header("Análisis Exploratorio")
    
    # Introducción a la sección
    st.write("""
    En esta sección puedes explorar visualizaciones clave y relaciones entre activos del S&P500. 
    Estas herramientas permiten analizar tendencias, correlaciones y comportamientos históricos para una mejor toma de decisiones financieras.
    """)
    # Título y aclaración antes del gráfico de velas
    st.subheader("Gráfico de Velas: Análisis de Datos Financieros")
    st.write("""
    El gráfico de velas permite visualizar:
    - **Precios de apertura, cierre, máximo y mínimo** de un activo en un periodo de tiempo.
    - Ayuda a identificar tendencias y patrones en los datos históricos.

    Selecciona una empresa, un rango de fechas y presiona el botón **Mostrar gráfico** para generar la visualización.
    """)
    # Cargar datos de cotización
    cotizaciones_df = obtener_cotizaciones()

    # Verificar y convertir la columna 'Date' a datetime si no lo es
    if cotizaciones_df['Date'].dtype != 'datetime64[ns]':
        cotizaciones_df['Date'] = pd.to_datetime(cotizaciones_df['Date'])

    # Seleccionar empresa y rango de fechas
    empresas = cotizaciones_df['Company'].unique()
    empresa_seleccionada = st.selectbox("Seleccione la empresa", empresas)
    min_date = cotizaciones_df['Date'].min()
    max_date = cotizaciones_df['Date'].max()
    fecha_inicio = st.date_input("Fecha de inicio", value=min_date, min_value=min_date, max_value=max_date)
    fecha_fin = st.date_input("Fecha de fin", value=max_date, min_value=min_date, max_value=max_date)

   
    # Botón para mostrar gráfico de velas
    if st.button("Mostrar Gráfico de Velas"):
    # Convertir la columna 'Date' a datetime si no lo está
        if cotizaciones_df['Date'].dtype != 'datetime64[ns]':
            cotizaciones_df['Date'] = pd.to_datetime(cotizaciones_df['Date'])

        # Convertir fechas seleccionadas a datetime si no lo están
        fecha_inicio = pd.to_datetime(fecha_inicio)
        fecha_fin = pd.to_datetime(fecha_fin)

        # Validar rango de fechas
        if fecha_inicio > fecha_fin:
            st.error("La fecha de inicio no puede ser posterior a la fecha de fin.")
        else:
            # Filtrar datos para el rango de fechas y empresa seleccionada
            df_filtrado = cotizaciones_df[
                (cotizaciones_df['Company'] == empresa_seleccionada) &
                (cotizaciones_df['Date'] >= fecha_inicio) &
                (cotizaciones_df['Date'] <= fecha_fin)
            ]

            if not df_filtrado.empty:
                # Mostrar gráfico de velas
                fig = graficar_velas(df_filtrado, empresa_seleccionada)
                st.plotly_chart(fig)
            else:
                st.warning(f"No hay datos disponibles para {empresa_seleccionada} en el rango de fechas seleccionado.")

    # Subsección: Análisis de correlación
    st.subheader("Análisis de Correlación entre Activos")
    st.write("""
    Este análisis muestra cómo se relacionan los precios de diferentes activos. 
    Una alta correlación positiva indica que los activos tienden a moverse en la misma dirección, mientras que una correlación negativa indica movimientos opuestos.
    """)
    activo_principal = st.selectbox("Seleccione el activo principal", empresas, key="activo_principal")
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

    # Caja desplegable para explicaciones
    with st.expander("Ver explicaciones sobre gráficos de velas y correlaciones"):
        st.write("""
        ### Gráfico de Velas
        - **Qué muestra:** Precios de apertura, cierre, máximo y mínimo.
        - **Cómo interpretar:**
            - Las velas verdes indican un precio de cierre superior al de apertura (tendencia alcista).
            - Las velas rojas indican un precio de cierre inferior al de apertura (tendencia bajista).

        ### Gráfico de Líneas
        - **Cuándo se usa:** Para periodos largos, donde las velas pueden no ser legibles.
        - **Qué muestra:** Solo el precio de cierre a lo largo del tiempo.

        ### Análisis de Correlación
        - **Qué muestra:** Relaciones entre activos financieros.
        - **Cómo interpretar:** 
            - Valores cercanos a 1 indican que los activos tienden a moverse en la misma dirección.
            - Valores cercanos a -1 indican que los activos tienden a moverse en direcciones opuestas.
        """)


# Dashboard Financiero
elif pagina == "Dashboard Financiero":
    st.header("Dashboard Financiero")
    # Título de la sección del tablero Power BI
    st.header("Tablero Interactivo de Power BI")

    # Explicación con estilo
    st.markdown("""
    <div style="
        background-color: #f0f2f6; 
        padding: 15px; 
        border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
        font-family: 'Arial', sans-serif; 
        font-size: 16px;
        line-height: 1.5;
        color: #333;">
        Este tablero interactivo en Power BI te permitirá explorar el desempeño del índice S&P500 y las empresas que lo conforman de una manera visual e intuitiva. 
        Puedes analizar:
        <ul>
            <li>El comportamiento histórico del índice y sectores clave.</li>
            <li>Indicadores técnicos como RSI, SMA y más.</li>
            <li>Rentabilidad de empresas y sectores en diferentes periodos.</li>
            <li>Comparar métricas avanzadas como Sharpe Ratio, Sortino Ratio y Calmar Ratio.</li>
        </ul>
        <strong>Descubre insights valiosos con una experiencia dinámica y personalizada.</strong>
    </div>
    """, unsafe_allow_html=True)

    # Configuración del iframe de Power BI
    powerbi_width = 1100
    powerbi_height = 700  # Ajusta según tu preferencia

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
    with st.expander("Descripción del Tablero Power BI"):
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
    st.image("Streamlit/diagrama_bbdd.png", use_container_width=True, caption="Diagrama de la Base de Datos")

    # Explicación del diseño de la base de datos
    st.markdown("""
    <div style="background-color:#f4f4f8; padding:15px; border-radius:10px; box-shadow: 0px 4px 8px rgba(0,0,0,0.2);">
        <h2 style="color:#2c3e50; text-align:center; font-family:Arial, sans-serif;">Estructura y Creación de la Base de Datos</h2>
        <p style="color:#34495e; font-size:16px; line-height:1.6; font-family:Arial, sans-serif;">
            La base de datos utilizada en este proyecto fue diseñada para almacenar información financiera del S&P500 
            y proporcionar soporte para los análisis presentados en esta aplicación.
        </p>
        <h3 style="color:#16a085; font-size:18px;">Tablas principales:</h3>
        <ul style="color:#34495e; font-size:16px; line-height:1.6;">
            <li><strong>empresas_sp500</strong>: Contiene información básica de las empresas, como su símbolo, nombre, sector, industria y capitalización de mercado.</li>
            <li><strong>precios_historicos</strong>: Almacena los precios históricos de las acciones, incluyendo la fecha, precios de apertura y cierre, máximos y mínimos diarios, así como el volumen negociado.</li>
            <li><strong>portafolios_usuarios</strong>: Permite a los usuarios crear portafolios personalizados y almacenar información relevante.</li>
            <li><strong>portafolio_empresas</strong>: Relaciona los portafolios de los usuarios con las empresas, incluyendo la cantidad de acciones y precios de compra.</li>
            <li><strong>indicadores_sp500</strong>: Almacena cálculos de indicadores financieros como medias móviles, RSI, y volatilidad.</li>
        </ul>
        <h3 style="color:#16a085; font-size:18px;">Proceso de creación:</h3>
        <ol style="color:#34495e; font-size:16px; line-height:1.6;">
            <li><strong>Diseño del esquema:</strong> El diagrama presentado arriba fue diseñado utilizando una herramienta de modelado de bases de datos.</li>
            <li><strong>Creación de la base de datos:</strong> Se utilizó MySQL para implementar el esquema en un servidor RDS de AWS.</li>
            <li><strong>Población de datos:</strong> Los datos fueron recolectados de fuentes como Yahoo Finance, y almacenados en las tablas correspondientes.</li>
        </ol>
        <h3 style="color:#16a085; font-size:18px;">Relaciones entre tablas:</h3>
        <p style="color:#34495e; font-size:16px; line-height:1.6;">
            Las relaciones clave son:
        </p>
        <ul style="color:#34495e; font-size:16px; line-height:1.6;">
            <li><strong>precios_historicos</strong> se relaciona con <strong>empresas_sp500</strong> a través de la clave primaria <strong>id_empresa</strong>.</li>
            <li><strong>portafolio_empresas</strong> relaciona los portafolios de usuarios con las empresas correspondientes.</li>
        </ul>
        <p style="color:#34495e; font-size:16px; line-height:1.6;">
            Este diseño asegura flexibilidad y escalabilidad, permitiendo almacenar grandes volúmenes de datos y realizar consultas eficientes para el análisis.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Modelo de CLusterig
elif pagina == "Modelo de Clustering":
    st.header("Modelo de Clustering")
    st.write("""
    en desarrollo...
    """)


# About Us
elif pagina == "About Us":
   # About Us 
    st.markdown("""
    <div style="background-color:#f4f4f8; padding:20px; border-radius:10px; box-shadow: 0px 4px 8px rgba(0,0,0,0.2); margin-bottom:30px;">
        <h2 style="text-align:center; color:#2c3e50; margin-bottom:30px;">Conoce al Equipo</h2>
    </div>
    """, unsafe_allow_html=True)

    # Equipo en tres columnas
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.image("Streamlit/foto_javier.jpeg", caption="Javier Aldonza", width=200)
        st.markdown("""
        <div style="text-align:center;">
            <a href="https://www.linkedin.com/in/javier-aldonza/" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="20"/> Javier Aldonza
            </a>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.image("Streamlit/foto_roberto.jpeg", caption="Roberto Gonzalez Álvarez", width=200)
        st.markdown("""
        <div style="text-align:center;">
            <a href="https://www.linkedin.com/in/roberto-gonz%C3%A1lez-%C3%A1lvarez-959552140" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="20"/> Roberto Gonzalez Álvarez
            </a>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.image("Streamlit/foto_khalid.jpeg", caption="Khalid el Afi Guerban", width=200)
        st.markdown("""
        <div style="text-align:center;">
            <a href="https://www.linkedin.com/in/khalid-el-afi-guerban-95212a270" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="20"/> Khalid el Afi Guerban
            </a>
        </div>
        """, unsafe_allow_html=True)

    # Espaciado antes de Tecnologías
    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)

    # Tecnologías en dos columnas
    st.markdown("""
    <div style="background-color:#f4f4f8; padding:20px; border-radius:10px; box-shadow: 0px 4px 8px rgba(0,0,0,0.2); margin-bottom:30px;">
        <h2 style="text-align:center; color:#2c3e50; margin-bottom:30px;">Tecnologías Utilizadas</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div style="background-color:#ffffff; border:1px solid #dddddd; border-radius:10px; padding:20px; margin-bottom:20px;">
            <h4 style="color:#3498db;">Python</h4>
            <ul>
                <li><a href="https://pandas.pydata.org/" target="_blank">Pandas</a> - Manipulación y análisis de datos.</li>
                <li><a href="https://numpy.org/" target="_blank">NumPy</a> - Cálculos numéricos avanzados.</li>
                <li><a href="https://matplotlib.org/" target="_blank">Matplotlib</a> - Visualización básica de datos.</li>
                <li><a href="https://plotly.com/" target="_blank">Plotly</a> - Gráficos interactivos avanzados.</li>
                <li><a href="https://github.com/ranaroussi/yfinance" target="_blank">yFinance</a> - Descarga de datos financieros.</li>
                <li><a href="https://scikit-learn.org/" target="_blank">Scikit-learn</a> - Modelado y algoritmos de machine learning.</li>
                <li><a href="https://docs.python.org/3/library/os.html" target="_blank">OS</a> - Gestión de archivos y rutas.</li>
                <li><a href="https://docs.python.org/3/library/sys.html" target="_blank">Sys</a> - Configuración de entorno y manejo de excepciones.</li>
            </ul>
        </div>
        <div style="background-color:#ffffff; border:1px solid #dddddd; border-radius:10px; padding:20px; margin-bottom:20px;">
            <h4 style="color:#e67e22;">MySQL</h4>
            <ul>
                <li><a href="https://pypi.org/project/pymysql/" target="_blank">PyMySQL</a> - Conexión a bases de datos MySQL desde Python.</li>
                <li><a href="https://dev.mysql.com/doc/" target="_blank">MySQL Connector</a> - Conexión directa con MySQL.</li>
                <li><a href="https://docs.sqlalchemy.org/en/20/" target="_blank">SQLAlchemy</a> - ORM para consultas más avanzadas (opcional).</li>
            </ul>
            <p>Base de datos en AWS RDS para almacenar y consultar grandes volúmenes de datos financieros.</p>
        </div>
        """, unsafe_allow_html=True)


    with col2:
        st.markdown("""
        <div style="background-color:#ffffff; border:1px solid #dddddd; border-radius:10px; padding:20px; margin-bottom:20px;">
            <h4 style="color:#2ecc71;">Streamlit</h4>
            <p>Framework para la creación de aplicaciones web interactivas.</p>
        </div>
        <div style="background-color:#ffffff; border:1px solid #dddddd; border-radius:10px; padding:20px; margin-bottom:20px;">
            <h4 style="color:#9b59b6;">Power BI</h4>
            <p>Tableros interactivos para análisis avanzado.</p>
        </div>
        <div style="background-color:#ffffff; border:1px solid #dddddd; border-radius:10px; padding:20px; margin-bottom:20px;">
            <h4 style="color:#1abc9c;">Scikit-learn</h4>
            <p>Implementación de algoritmos de clasificación y predicción.</p>
        </div>
        """, unsafe_allow_html=True)

    # Espaciado antes del proceso de creación
    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)

    # Proceso de creación
    st.markdown("""
    <div style="background-color:#f4f4f8; padding:20px; border-radius:10px; box-shadow: 0px 4px 8px rgba(0,0,0,0.2); margin-bottom:30px;">
        <h2 style="text-align:center; color:#2c3e50;">Proceso de Creación</h2>
        <ol style="color:#34495e; font-size:16px; line-height:1.8; font-family:Arial, sans-serif; margin-top:20px;">
            <li><strong>Diseño del esquema:</strong> Utilizamos herramientas de modelado de bases de datos para estructurar el sistema.</li>
            <li><strong>Creación de la base de datos:</strong> Implementación en MySQL con despliegue en un servidor AWS RDS.</li>
            <li><strong>Recolección de datos:</strong> Extracción de información de Yahoo Finance para poblar las tablas.</li>
            <li><strong>Desarrollo de funciones:</strong> Codificación en Python para análisis y visualización.</li>
            <li><strong>Construcción de la aplicación:</strong> Uso de Streamlit para crear una experiencia interactiva.</li>
            <li><strong>Integración de Power BI:</strong> Creación de dashboards para análisis avanzado.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)



# Pie de página
st.sidebar.write("Aplicación creada con Streamlit")





