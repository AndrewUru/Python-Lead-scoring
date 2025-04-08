# scoring_utils.py

def obtener_score(client, mensaje, empresa, tamaño_empresa):
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
    except Exception:
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

def obtener_recomendacion(categoria):
    if "Caliente" in categoria:
        return "¡Contactar de inmediato!"
    elif "Tibio" in categoria:
        return "Dar seguimiento pronto."
    elif "Frío" in categoria:
        return "Baja prioridad."
    else:
        return "Revisar manualmente."
