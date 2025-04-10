import streamlit as st

st.set_page_config(page_title="Cómo funciona?", page_icon="🧭")

st.title("🧭 Cómo usar la app Lead Scoring con IA")
st.markdown("---")

st.markdown(
    """
## ✨ ¿Qué es esta app?

Esta aplicación utiliza **Inteligencia Artificial (OpenAI)** para analizar los mensajes de tus leads y clasificarlos automáticamente en función de su **intención de compra**.

Te ayuda a priorizar clientes potenciales y tomar mejores decisiones comerciales.

---

## ⚙️ ¿Cómo funciona?

1. **Sube un archivo CSV** con tus leads.
2. El sistema analiza automáticamente cada mensaje con un modelo de IA.
3. Se asigna un **lead score** del 1 (bajo interés) al 5 (alta intención de compra).
4. Se genera una **clasificación automática**: Frío, Tibio o Caliente.
5. Puedes **ver los resultados en tabla, descargar un Excel**, y explorar **gráficos de distribución**.

---

## 🧾 ¿Qué debe contener el CSV?

Tu archivo debe tener una columna con los mensajes o consultas de los leads. También puedes incluir:

- 📩 Email del contacto
- 👤 Nombre
- 🏢 Empresa (opcional)
- 📊 Tamaño de la empresa (opcional)

> **Formato recomendado:** UTF-8, separado por comas, extensión `.csv`.

---

## 🌐 ¿Dónde puedo usarla?

- ✅ En local (con `streamlit run app.py`)
- ☁️ En la nube: [Streamlit Cloud](https://python-lead-scoring.streamlit.app/)
- 🚧 En desarrollo: versión web estática en [Vercel](https://vercel.com/)

---

## 🚀 ¿Qué viene después?

- 📈 Dashboard interactivo con filtros
- 🔐 Autenticación de usuarios
- 📲 Integración con WhatsApp y Telegram
- 🔔 Alertas automáticas según el score
- 🧠 Entrenamiento de modelos personalizados con tus propios leads
- 👥 Soporte multiusuario y multiempresa

---

## 👨‍💻 Desarrollado por

**Andrés Tobío** · [elsaltoweb.es](https://elsaltoweb.es)

🚀 Con Streamlit + OpenAI · Código abierto en [GitHub](https://github.com/AndrewUru/Python-Lead-scoring)
    """,
    unsafe_allow_html=True
)
