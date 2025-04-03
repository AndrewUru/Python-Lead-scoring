import streamlit as st
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

# Carga de variables de entorno
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Validación de la API Key
if not api_key:
    st.error("❌ No se encontró la clave de API de OpenAI. Verifica tu archivo `.env` o los secretos en Streamlit Cloud.")
    st.stop()

# Cliente de OpenAI
client = OpenAI(api_key=api_key)

# Configuración de la página
st.set_page_config(page_title="Lead Scoring", layout="wide")
st.title("🔍 Análisis de Leads con IA")

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

Esta herramienta analiza leads (clientes potenciales) utilizando **inteligencia artificial** para predecir su intención de contratar servicios digitales.

Evalúa cada mensaje teniendo en cuenta:

- El contenido del mensaje del cliente
- El tipo de empresa
- El tamaño de la empresa

---

👥 **Ideal para:**

- 📈 Agencias de marketing digital  
- 🧑‍💻 Freelancers que ofrecen servicios web o redes sociales  
- 🏢 Equipos comerciales que gestionan grandes listas de contactos  

---

⚡ Pulsa en “**Analizar Leads**” para obtener una puntuación de intención de contratación (Lead Score) del 1 al 5, junto con su categoría: **Frío, Tibio o Caliente**.
""")


# Subida de archivo
uploaded_file = st.file_uploader("📤 Sube tu archivo CSV de leads", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Vista previa del archivo subido")
    st.dataframe(df, use_container_width=True)

    st.markdown("### ⚙️ Configura tu análisis")

    col_mensaje = st.selectbox("📝 ¿Qué columna contiene el mensaje o intención del lead?", df.columns)
    col_nombre = st.selectbox("👤 ¿Qué columna usar como nombre?", df.columns, index=0)
    col_email = st.selectbox("📧 ¿Qué columna usar como email?", df.columns, index=1)

    # Generar columnas necesarias por defecto
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

        # Análisis con IA
        with st.spinner("🤖 Analizando intención de compra..."):
            df["lead_score"] = df.apply(
                lambda row: obtener_score(row[col_mensaje], row["empresa"], row["tamaño_empresa"]),
                axis=1
            )
            df["categoría"] = df["lead_score"].apply(categorizar)
            df["necesidad"] = df[col_mensaje].apply(clasificar_necesidad)

        st.success("✅ Análisis completado")
        st.dataframe(df, use_container_width=True)

        # Exportar resultados
        with st.spinner("📦 Preparando archivos para descargar..."):
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar CSV", csv, "leads_analizados.csv", "text/csv")

            df.to_excel("leads_analizados.xlsx", index=False)
            with open("leads_analizados.xlsx", "rb") as f:
                st.download_button("📥 Descargar Excel", f, "leads_analizados.xlsx", "application/vnd.ms-excel")

        st.markdown("""<hr style="border:1px solid #ccc">
        <center>
            Hecho con ❤️ por <a href="https://elsaltoweb.es" target="_blank">Andrés Tobío</a> · Powered by OpenAI & Streamlit
        </center>""", unsafe_allow_html=True)
