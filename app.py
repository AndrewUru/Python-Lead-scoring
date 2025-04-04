import streamlit as st
import pandas as pd
import openai
import os
from dotenv import load_dotenv

# Cargar claves desde .env
load_dotenv()
client = openai

# Config de la página
st.set_page_config(page_title="Lead Scoring con IA",
                   page_icon="🧠", layout="wide")


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
        transform: scale(1.02);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
    }

    .custom-header h3 {
        color: #4FC3F7;
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

# Sidebar
with st.sidebar:
    st.image("logo.png", width=150)
    st.title("📊 Lead Scoring App")
    st.markdown("---")
    st.markdown("📁 Subir archivo CSV")
    st.markdown("📥 Descargar ejemplo")
    st.markdown("📈 Ver resultados")
    st.markdown("---")
    st.caption("Desarrollado por [Andrés Tobío](https://elsaltoweb.es)")


st.markdown("""
### 🧠 ¿Qué hace esta app?

Esta herramienta analiza leads (clientes potenciales) usando inteligencia artificial.  
Evalúa el nivel de intención de compra de cada lead en base a su mensaje, el tipo de empresa y su tamaño.

Ideal para:

- Agencias de marketing digital.
- Freelancers que ofrecen servicios web o en redes sociales.
- Empresas que quieren priorizar contactos.

---

### 📥 Descarga un archivo de ejemplo

Puedes usar este archivo CSV para probar la app rápidamente.
""")

# Cargar archivo de ejemplo
with open("leads.csv", "rb") as file:
    st.download_button("⬇️ Descargar CSV de ejemplo",
                       file, "leads.csv", "text/csv")

# Subida de archivo
uploaded_file = st.file_uploader("📤 Sube tu archivo CSV de leads", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Vista previa del archivo subido")
    st.dataframe(df, use_container_width=True)

    st.markdown("### ⚙️ Configura tu análisis")
    col_mensaje = st.selectbox(
        "📝 ¿Qué columna contiene el mensaje o deseo del lead?", df.columns)
    col_nombre = st.selectbox(
        "👤 ¿Qué columna usar como nombre?", df.columns, index=0)
    col_email = st.selectbox(
        "📧 ¿Qué columna usar como email?", df.columns, index=1)

    # Columnas por defecto para el análisis
    df["empresa"] = "Sin datos"
    df["tamaño_empresa"] = "pequeña"

    if st.button("✨ Analizar Leads"):

        def obtener_score(mensaje, empresa, tamaño_empresa):
            prompt = f"""
Eres un asesor experto en marketing digital. Evalúa del 1 al 5 la intención de contratar (1 = baja, 5 = alta):

Lead:
- Empresa: {empresa}
- Tamaño: {tamaño_empresa}
- Mensaje: "{mensaje}"

Solo responde con un número del 1 al 5.
"""
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0
                )
                score = response.choices[0].message.content.strip()
                return int(score)
            except Exception as e:
                st.warning(f"⚠️ Error al analizar: '{mensaje[:40]}...'\n{e}")
                return None

        def clasificar_necesidad(mensaje):
            if not isinstance(mensaje, str):
                return "Otro"
            mensaje = mensaje.lower()
            if "tienda" in mensaje or "ecommerce" in mensaje:
                return "E-commerce"
            elif "web" in mensaje or "página" in mensaje:
                return "Sitio Web"
            elif "instagram" in mensaje or "redes" in mensaje:
                return "Redes Sociales"
            else:
                return "Otro"

        def categorizar(score):
            if score is None:
                return "❓"
            elif score >= 4:
                return "🟢 Caliente"
            elif score == 3:
                return "🟡 Tibio"
            else:
                return "🔴 Frío"

        with st.spinner("🤖 Analizando intención de compra..."):
            df["lead_score"] = df.apply(
                lambda row: obtener_score(
                    row[col_mensaje], row["empresa"], row["tamaño_empresa"]
                ),
                axis=1
            )
            df["categoría"] = df["lead_score"].apply(categorizar)
            df["necesidad"] = df[col_mensaje].apply(clasificar_necesidad)

        st.success("✅ Análisis completado")
        st.dataframe(df, use_container_width=True)

        # Exportar
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV", csv,
                           "leads_analizados.csv", "text/csv")

        df.to_excel("leads_analizados.xlsx", index=False)
        with open("leads_analizados.xlsx", "rb") as f:
            st.download_button(
                "📥 Descargar Excel", f, "leads_analizados.xlsx", "application/vnd.ms-excel")


# Markdown con estilo moderno mejorado
st.markdown("""
<style>
.intro-box {
    background-color: #1E1E1E;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    border: 1px solid #333;
}
.intro-box h3 {
    color: #4FC3F7;
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


# Footer oculto y personalizado (si lo necesitas visible con branding tuyo)
st.markdown("""
<style>
footer {visibility: visible;}
footer:after {
    content: 'Desarrollado con ❤️ por Andrés Tobío · Potenciado con Streamlit y OpenAI';
    display: block;
    text-align: center;
    color: #888;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)
