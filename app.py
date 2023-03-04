import requests
import json
from flask import Flask, request, jsonify

# Configuración de las claves de las APIs
REI_REPLY_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2NhdGlvbl9pZCI6Imp3cnBDZ0tOaW90b0w1WWx1TDJDIiwiY29tcGFueV9pZCI6Im0waXo0YktRT1NkbmJmdzVmcHJCIiwidmVyc2lvbiI6MSwiaWF0IjoxNjY5MzkyNzEyMjAzLCJzdWIiOiJ6YXBpZXIifQ.Hpj13PRwe0_yQs70-0rOBvpLeokHPSlSNNzMog2jHNM"
CHAT_GPT_API_KEY = "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"

# Función para enviar mensajes a Chat GPT
def send_message_to_chat_gpt(message):
    url = f"https://api.openai.com/v1/messages"
    headers = {
        "Authorization": f"Bearer {CHAT_GPT_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": message,
        "chat_id": "080094c1-832f-4925-8fb3-d79f7e0fe108"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

# Función para recibir mensajes de REI Reply y enviarlos a Chat GPT
def handle_incoming_message(message):
    message_text = message["content"]
    chat_gpt_response = send_message_to_chat_gpt(message_text)
    return chat_gpt_response["data"][0]["text"]

# Ruta para recibir los mensajes entrantes de REI Reply
app = Flask(__name__)
@app.route('/webhook/reireply', methods=['POST'])
def receive_rei_reply_messages():
    message = request.json
    response_text = handle_incoming_message(message)
    # Enviar la respuesta de Chat GPT de vuelta a REI Reply
    response = {
        "content": response_text
    }
    return jsonify(response)

# Configuración de la API de REI Reply para recibir los mensajes entrantes
def configure_rei_reply_webhook():
    url = "https://api.reireply.ai/webhooks"
    headers = {
        "Authorization": f"Bearer {REI_REPLY_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "url": "tu_url_de_webhook",
        "event": "incoming_message"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

# Configuración del webhook y ejecución de la aplicación
if __name__ == '__main__':
    configure_rei_reply_webhook()
    app.run()
