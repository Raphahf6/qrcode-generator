from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import requests
import os

app = FastAPI()

# Pega as mesmas variáveis que você já usa
EVO_URL = os.environ.get("EVOLUTION_URL")
EVO_KEY = os.environ.get("EVOLUTION_KEY")
INSTANCE = "Principal" # Mude para o nome da sua instância

@app.get("/", response_class=HTMLResponse)
async def view_qr():
    url = f"{EVO_URL}/instance/connect/{INSTANCE}"
    headers = {"apikey": EVO_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if "base64" in data:
            qr_base64 = data["base64"]
            return f"""
            <html>
                <body style="background:#0f172a; color:white; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; font-family:sans-serif;">
                    <h1>Escaneie o QR Code - {INSTANCE}</h1>
                    <div style="background:white; padding:20px; border-radius:10px;">
                        <img src="{qr_base64}" style="width:300px; height:300px;" />
                    </div>
                    <p style="margin-top:20px; color:grey;">Atualize a página (F5) se o código expirar.</p>
                </body>
            </html>
            """
        else:
            return f"<h1>Erro: {data.get('message', 'Instância já conectada ou erro interno')}</h1>"
    except Exception as e:
        return f"<h1>Erro de Conexão: {str(e)}</h1>"