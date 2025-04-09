import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
import seaborn as sns

from scoring_utils import (
    obtener_score,
    clasificar_necesidad,
    categorizar,
    obtener_recomendacion
)

# Cargar variables de entorno
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Título
st.title("🔍 Lead Scoring con IA")
# Botón destacado
st.markdown("### ¿Primera vez aquí?")
if st.button("ℹ️ Ver guía de uso paso a paso"):
    st.switch_page("1_como_funciona.py")


# Cargar archivo CSV
archivo = st.file_uploader("📂 Sube un archivo CSV con tus leads", type=["csv"])
if archivo is not None:
    df = pd.read_csv(archivo)

    # Configuración de columnas
    columnas = df.columns.tolist()
    col_mensaje = st.selectbox("📨 ¿Qué columna contiene el mensaje o deseo del lead?", columnas, key="mensaje")
    col_nombre = st.selectbox("🙋 ¿Qué columna usar como nombre?", columnas, key="nombre")
    col_email = st.selectbox("✉️ ¿Qué columna usar como email?", columnas, key="email")

    # Valores por defecto
    df["empresa"] = df.get("empresa", "Sin datos")
    df["tamaño_empresa"] = df.get("tamaño_empresa", "pequeña")

    if st.button("✨ Analizar Leads"):
        with st.spinner("🤖 Analizando intención de compra..."):
            resultados = df.copy()

            resultados["score"] = resultados.apply(
                lambda row: obtener_score(client, row[col_mensaje], row["empresa"], row["tamaño_empresa"]),
                axis=1
            )
            resultados["justificación"] = resultados[col_mensaje].apply(lambda msg: "Score generado por IA")
            resultados["categoría"] = resultados["score"].apply(categorizar)
            resultados["recomendación"] = resultados["categoría"].apply(obtener_recomendacion)

            # Combinar resultados con DataFrame original
            df["lead_score"] = resultados["score"]
            df["justificación"] = resultados["justificación"]
            df["categoría"] = resultados["categoría"]
            df["recomendación"] = resultados["recomendación"]

        st.success("✅ Análisis completado")
        st.dataframe(df, use_container_width=True)

        st.dataframe(df, use_container_width=True)

        # 👇 Mostrar gráficos solo si 'lead_score' ya existe
        if "lead_score" in df.columns:
            st.markdown("### 📈 Distribución de Lead Scores")
            fig1, ax1 = plt.subplots()
            sns.histplot(df["lead_score"], bins=5, kde=True, ax=ax1)
            st.pyplot(fig1)

            st.markdown("### 📊 Clasificación por categoría")
            fig2, ax2 = plt.subplots()
            df["categoría"].value_counts().plot(kind="bar", ax=ax2)
            st.pyplot(fig2)
        else:
            st.info("⚠️ Aún no se ha generado el análisis. Presiona '✨ Analizar Leads' primero.")


        

    # Exportar resultados
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar CSV", csv, "leads_analizados.csv", "text/csv")

st.markdown(
    """
    ### 📥 Descarga un archivo de ejemplo

    Puedes usar este archivo CSV para probar la app rápidamente.
    """,
    unsafe_allow_html=True
)

try:
    with open("leads.csv", "rb") as file:
        st.download_button(
            label="⬇️ Descargar CSV de ejemplo",
            data=file,
            file_name="leads.csv",
            mime="text/csv"
        )
except FileNotFoundError:
    st.warning("⚠️ No se encontró el archivo `leads.csv`. Verifica que esté en la raíz del proyecto.")

# Header moderno y responsive
st.markdown("""
<style>
    /* Animación */
    @keyframes fadeSlideIn {
        0% {
            opacity: 0;
            transform: translateY(-30px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .custom-header {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        animation: fadeSlideIn 1s ease-out;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .custom-header:hover {
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
    }

    .custom-header h3 {
        color: #ffffff;
        margin-bottom: 0.5rem;
        font-size: 2rem;
        font-family: 'Segoe UI', sans-serif;
    }

    @media (max-width: 768px) {
        .custom-header h3 {
            font-size: 1.5rem;
        }
    }

    @media (max-width: 480px) {
        .custom-header h3 {
            font-size: 1.2rem;
        }
    }
</style>

<div class='custom-header'>
    <h3>Evalúa automáticamente la intención de compra de tus leads y clasifícalos como Frío, Tibio o Caliente.</h3>
</div>
""", unsafe_allow_html=True)

# Sidebar con estilo pro y roadmap
with st.sidebar:
    st.image("logo.png", width=160)
    st.markdown(
        """
        <style>
        .sidebar-title {
            font-size: 1.2rem;
            font-weight: bold;
            color: #4f46e5;
            margin-top: 1rem;
        }
        .sidebar-section {
            margin-bottom: 1.5rem;
        }
        .sidebar-section ul {
            padding-left: 1.2rem;
        }
        .sidebar-section li {
            margin-bottom: 0.5rem;
        }
        .sidebar-footer {
            font-size: 0.8rem;
            color: #999;
            text-align: center;
            margin-top: 2rem;
        }
        </style>

        <div class="sidebar-section">
            <div class="sidebar-title">📌 Funcionalidades actuales</div>
            <ul>
                <li>⬆️ Subida de archivo CSV</li>
                <li>🤖 Análisis con IA (GPT)</li>
                <li>📊 Puntuación del 1 al 5</li>
                <li>⬇️ Exportación a Excel / CSV</li>
                <li>📋 Tabla de resultados</li>
                <li>📈 Gráficos de distribución</li>
            </ul>
        </div>

        <div class="sidebar-section">
            <div class="sidebar-title">🌐 Deploys</div>
            <ul>
                <li>🖥️ Local</li>
                <li>☁️ Streamlit Cloud</li>
                <li>🚧 Vercel (en desarrollo)</li>
            </ul>
        </div>

        <div class="sidebar-section">
            <div class="sidebar-title">🚀 Futuras funcionalidades</div>
            <ul>
                <li>📊 Dashboard con filtros</li>
                <li>🔐 Autenticación de usuarios</li>
                <li>📲 Integración WhatsApp / Telegram</li>
                <li>🔔 Alertas por score</li>
                <li>🧠 Entrenamiento con tus leads</li>
                <li>👥 Soporte multiusuario</li>
            </ul>
        </div>
        st.sidebar.page_link("pages/1_Cómo_funciona.py", label="ℹ️ Cómo usar la app")

        <div class="sidebar-footer">
            Desarrollado por <a href="https://elsaltoweb.es" target="_blank">Andrés Tobío</a> 🚀
        </div>
        """,
        unsafe_allow_html=True
    )


# Markdown con estilo moderno mejorado
st.markdown("""
<style>
.intro-box {
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    border: 1px solid #333;
}
.intro-box h3 {
    
    font-weight: 700;
    font-size: 1.6rem;
    margin-top: 0;
}
.intro-box ul {
    padding-left: 1.5rem;
    line-height: 1.6;
}
footer {visibility: hidden;}
</style>

<div class="intro-box">
<h3>🧠 ¿Qué hace esta app?</h3>

Esta herramienta analiza leads (clientes potenciales) utilizando <strong>inteligencia artificial</strong> para predecir su intención de contratar servicios digitales.

Evalúa cada mensaje teniendo en cuenta:
<ul>
  <li>💬 El contenido del mensaje del cliente</li>
  <li>🏢 El tipo de empresa</li>
  <li>📊 El tamaño de la empresa</li>
</ul>

<hr/>

<h3>👥 Ideal para:</h3>
<ul>
  <li>📈 Agencias de marketing digital</li>
  <li>🧑‍💻 Freelancers que ofrecen servicios web o redes sociales</li>
  <li>🏢 Equipos comerciales que gestionan grandes listas de contactos</li>
</ul>

<hr/>

⚡ Pulsa en <strong>“Analizar Leads”</strong> para obtener una puntuación de intención de contratación (Lead Score) del 1 al 5, junto con su categoría: <strong>Frío, Tibio o Caliente</strong>.
</div>
""", unsafe_allow_html=True)

# Footer moderno y responsive

st.markdown(
    """
    <style>
    .custom-footer {
        position: sticky-bottom;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f9f9f9;
        color: #666;
        text-align: center;
        padding: 1rem;
        font-size: 0.9rem;
        border-top: 1px solid #ddd;
        z-index: 9999;
    }

    .custom-footer a {
        color: #4f46e5;
        text-decoration: none;
        font-weight: 600;
    }

    .custom-footer a:hover {
        text-decoration: underline;
    }

    /* Para dar espacio abajo y que no tape contenido */
    .block-container {
        padding-bottom: 100px;
    }
    </style>

    <div class="custom-footer">
        Desarrollado con ❤️ por 
        <a href="https://www.linkedin.com/in/andrestobio/" target="_blank">Andrés Tobío</a> · Potenciado con 
        <a href="https://streamlit.io" target="_blank">Streamlit</a> y 
        <a href="https://openai.com" target="_blank">OpenAI</a><br />
        <span style="font-size: 0.8rem;">© 2025 · Todos los derechos reservados</span>
    </div>
    """,
    unsafe_allow_html=True
)



