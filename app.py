import streamlit as st
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Lead Scoring", layout="wide")
st.title("🔍 Análisis de Leads con IA")

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

- Agencias de marketing digital
- Freelancers que ofrecen servicios web o en redes sociales
- Empresas que quieren priorizar contactos

---

### 📥 Descarga un archivo de ejemplo

Puedes usar este archivo CSV para probar la app rápidamente.
""")

with open("leads.csv", "rb") as file:
    st.download_button("⬇️ Descargar CSV de ejemplo", file, "leads.csv", "text/csv")


# Subir archivo
uploaded_file = st.file_uploader("📤 Sube tu archivo CSV de leads", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df, use_container_width=True)

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
                return int(response.choices[0].message.content.strip())
            except:
                return None

        def categorizar(score):
            if score >= 4:
                return "🟢 Caliente"
            elif score == 3:
                return "🟡 Tibio"
            elif score <= 2:
                return "🔴 Frío"
            else:
                return "❓"

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

        with st.spinner("Analizando leads..."):
            df["lead_score"] = df.apply(
                lambda row: obtener_score(row["mensaje"], row["empresa"], row["tamaño_empresa"]),
                axis=1
            )
            df["categoría"] = df["lead_score"].apply(categorizar)
            df["necesidad"] = df["mensaje"].apply(clasificar_necesidad)

        st.success("✅ Análisis completado")
        st.dataframe(df, use_container_width=True)

        # Exportar
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV", csv, "leads_analizados.csv", "text/csv")

        xlsx = df.to_excel("leads_analizados.xlsx", index=False)
        with open("leads_analizados.xlsx", "rb") as f:
            st.download_button("📥 Descargar Excel", f, "leads_analizados.xlsx", "application/vnd.ms-excel")

            st.markdown("""
<hr style="border:1px solid #ccc">
<center>
    Hecho con ❤️ por [Andrés Tobío](https://elsaltoweb.es) · Powered by OpenAI & Streamlit
</center>
""", unsafe_allow_html=True)

