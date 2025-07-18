import streamlit as st
import json
import requests
from datetime import datetime, timezone

# === CONFIGURACIÓN GENERAL ===
st.set_page_config(page_title="Extract My Chat", layout="wide")

# === FUNCIONES AUXILIARES ===
def get_ip():
    try:
        return requests.get("https://api64.ipify.org").text.strip()
    except:
        return "desconocida"

def registrar_uso_make(titulo, formato, idioma):
    try:
        ip = get_ip()
        url = "MAKE_WEBHOOK_URL"
        data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "titulo": titulo,
            "formato": formato,
            "idioma": idioma,
            "ip": ip,
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 200:
            print(f"⚠️ Make respondió con código {response.status_code}: {response.text}")

    except Exception as e:
        print("❌ Error al registrar en Make:", e)

# === IDIOMA / TRADUCCIÓN ===
lang = st.sidebar.selectbox("🌐 Language / Idioma", ["Español", "English"])

T = {
    "Español": {
        "title": "💬 Extract My Chat",
        "description": (
        "Extrae conversaciones específicas de tu historial de ChatGPT exportado. "
        "Sube tu archivo `conversations.json`, selecciona el chat que quieres y descárgalo en formato texto o JSON.\n\n"
        "🔒 Tus chats no se guardan en ningún servidor. Son totalmente privados."
    ),
        "upload_label": "📁 Sube tu archivo `conversations.json`",
        "select_chat": "🗂️ Elige la conversación",
        "format_label": "📤 Formato de salida",
        "extract_btn": "📦 Extraer conversación",
        "json_download": "⬇️ Descargar JSON",
        "txt_download": "⬇️ Descargar TXT",
        "preview": "📝 Vista previa",
        "no_messages": "No se encontraron mensajes válidos.",
        "not_found": "No se encontró la conversación.",
    },
    "English": {
        "title": "💬 Extract My Chat",
        "description": (
        "Extract specific conversations from your exported ChatGPT history. "
        "Upload your `conversations.json`, pick a chat, and download it as plain text or JSON.\n\n"
        "🔒 Your chats are not stored on any server. They remain fully private."
    ),
        "upload_label": "📁 Upload your `conversations.json` file",
        "select_chat": "🗂️ Select a conversation",
        "format_label": "📤 Output format",
        "extract_btn": "📦 Extract conversation",
        "json_download": "⬇️ Download JSON",
        "txt_download": "⬇️ Download TXT",
        "preview": "📝 Preview",
        "no_messages": "No valid messages found.",
        "not_found": "Conversation not found.",
    }
}[lang]

# === INTERFAZ PRINCIPAL ===
st.title(T["title"])
st.markdown(T["description"])

archivo = st.file_uploader(T["upload_label"], type="json")

if archivo:
    datos = json.load(archivo)
    conversaciones = [conv for conv in datos if isinstance(conv, dict) and conv.get("title")]
    titulos = [conv["title"] for conv in conversaciones]
    titulo_seleccionado = st.selectbox(T["select_chat"], titulos)
    formato = st.radio(T["format_label"], options=["Texto", "JSON"] if lang == "Español" else ["Text", "JSON"])

    if st.button(T["extract_btn"]):
        seleccionada = next((c for c in conversaciones if c["title"] == titulo_seleccionado), None)
        if not seleccionada:
            st.error(T["not_found"])
        else:
            registrar_uso_make(titulo_seleccionado, formato, lang)

            if formato.lower() == "json":
                json_str = json.dumps(seleccionada, ensure_ascii=False, indent=2)
                st.download_button(T["json_download"], data=json_str, file_name="conversacion.json", mime="application/json")

            else:
                mapping = seleccionada.get("mapping", {})
                mensajes = []

                def recorrer(nodo_id):
                    nodo = mapping.get(nodo_id)
                    if not nodo:
                        return
                    msg = nodo.get("message")
                    if msg:
                        autor = msg.get("author", {}).get("role", "")
                        partes = msg.get("content", {}).get("parts", [])
                        tipo_contenido = msg.get("content", {}).get("content_type", "")
                        texto = "\n".join(partes).strip()
                        if autor in ["user", "assistant"] and texto and tipo_contenido == "text":
                            mensajes.append(f"{autor.upper()}:\n{texto}\n")
                    for hijo_id in nodo.get("children", []):
                        recorrer(hijo_id)

                if "client-created-root" in mapping:
                    recorrer("client-created-root")
                else:
                    for nodo_id in mapping:
                        recorrer(nodo_id)

                if mensajes:
                    texto_final = "\n".join(mensajes)
                    st.text_area(T["preview"], value=texto_final, height=400)
                    st.download_button(T["txt_download"], data=texto_final, file_name="conversacion.txt", mime="text/plain")
                else:
                    st.warning(T["no_messages"])

