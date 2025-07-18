# 💬 Extract My Chat

Una app en Streamlit que te permite extraer conversaciones específicas de tu historial exportado de ChatGPT (`conversations.json`) y descargarlas como texto plano o JSON.

## 🚀 Cómo usar

1. Exporta tu historial desde [chat.openai.com](https://chat.openai.com)
2. Sube el archivo `conversations.json` a la app
3. Selecciona una conversación
4. Elige el formato de salida: `.json` o `.txt`
5. Descarga el resultado

## 🛡️ Privacidad

- El archivo no se guarda en ningún servidor.
- Solo se registra el título de la conversación y formato usado (sin contenido), junto con la IP, para estadísticas de uso.

## 📊 Métricas

Los datos se envían a un webhook privado gestionado con Make.com y almacenados en Google Sheets para seguimiento del uso (no incluye texto del chat).
