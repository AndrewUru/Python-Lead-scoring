import streamlit as st
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

# Cargar claves desde .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Config de la página
st.set_page_config(page_title="Lead Scoring", layout="wide")
st.title("🔍 Lead Scoring App con IA")

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

# Descarga de ejemplo
with open("leads.csv", "rb") as file:
    st.download_button("⬇️ Descargar CSV de ejemplo", file, "leads.csv", "text/csv")

# Subida de archivo
uploaded_file = st.file_uploader("📤 Sube tu archivo CSV de leads", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Vista previa del archivo subido")
    st.dataframe(df, use_container_width=True)

    st.markdown("### ⚙️ Configura tu análisis")
    col_mensaje = st.selectbox("📝 ¿Qué columna contiene el mensaje o deseo del lead?", df.columns)
    col_nombre = st.selectbox("👤 ¿Qué columna usar como nombre?", df.columns, index=0)
    col_email = st.selectbox("📧 ¿Qué columna usar como email?", df.columns, index=1)

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
                lambda row: obtener_score(row[col_mensaje], row["empresa"], row["tamaño_empresa"]),
                axis=1
            )
            df["categoría"] = df["lead_score"].apply(categorizar)
            df["necesidad"] = df[col_mensaje].apply(clasificar_necesidad)

        st.success("✅ Análisis completado")
        st.dataframe(df, use_container_width=True)

        # Exportar
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV", csv, "leads_analizados.csv", "text/csv")

        df.to_excel("leads_analizados.xlsx", index=False)
        with open("leads_analizados.xlsx", "rb") as f:
            st.download_button("📥 Descargar Excel", f, "leads_analizados.xlsx", "application/vnd.ms-excel")
