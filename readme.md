# Lead Scoring con Inteligencia Artificial

Este proyecto permite analizar leads (clientes potenciales) mediante el uso de inteligencia artificial, utilizando la API de OpenAI. El sistema evalúa el nivel de intención de compra de cada lead según el mensaje proporcionado, el tipo de empresa y su tamaño. Está diseñado para ayudar a negocios digitales, freelancers, agencias de marketing y equipos comerciales a priorizar contactos de forma automática.

## 📊 Tecnologías utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [OpenAI API](https://platform.openai.com/)
- [Pandas](https://pandas.pydata.org/)

## 📅 Características actuales

- Interfaz web para subir un archivo `.csv` con leads.
- Análisis automático de cada lead usando un modelo GPT de OpenAI.
- Asignación de una puntuación del 1 al 5 a cada lead (lead scoring).
- Exportación de resultados a Excel o CSV.
- Visualización de resultados en tabla.
- Gráficos de distribución.

## 🌐 Deploys

- [x] Compatible con despliegue local
- [x] Desplegado en [Streamlit Cloud](https://streamlit.io/cloud)
- [ ] Despliegue en Vercel para la versión web estática (en desarrollo)

## 🚀 Futuras implementaciones

- 📈 Dashboard con métricas interactivas y filtros.
- 🤑 Autenticación para usuarios y lead scoring por cuenta.
- 📲 Integración con WhatsApp y Telegram.
- 📢 Sistema de alertas automáticas según el score.
- 💡 Entrenamiento de modelo propio personalizado con tus propios leads.
- 👥 Soporte multiusuario y multiempresa.

## 🙌 Contribuciones bienvenidas

Estoy abierto a recibir sugerencias, mejoras y colaboraciones en el repositorio. Si quieres ayudar:

1. Haz un fork del proyecto.
2. Crea tu rama (`git checkout -b feature/nombre`)
3. Sube tus cambios (`git commit -am 'Agrega una nueva funcionalidad'`)
4. Haz un push (`git push origin feature/nombre`)
5. Abre un Pull Request

Tambien puedes escribirme directamente si quieres colaborar en nuevas funcionalidades.

## 📂 Datos de ejemplo

Puedes encontrar un archivo `leads.csv` de ejemplo dentro del repositorio para comenzar a probar.

## 🌐 Demo

- [Versión local](http://localhost:8501) (ejecuta `streamlit run app.py`)
- [Demo en Streamlit Cloud](https://pyton-lead-scoring.streamlit.app/) (si está activa)

---

Desarrollado por [Andrés Tobio](https://elsaltoweb.es) — 2025
