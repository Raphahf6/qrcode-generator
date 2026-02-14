from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
import os

app = FastAPI()

EVO_URL = os.environ.get("EVOLUTION_URL")
EVO_KEY = os.environ.get("EVOLUTION_KEY")
INSTANCE = "Principal"

async def view_qr():
    # Adicionamos um parâmetro de força para garantir que ele tente pegar o QR
    url = f"{EVO_URL}/instance/connect/{INSTANCE}"
    headers = {"apikey": EVO_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # LOGICA TURBINADA: Se houver base64, MOSTRA. Independente de qualquer erro.
        if data.get("base64"):
            qr_base64 = data["base64"]
            return f"""
            <html>
                <body style="background:#0f172a; color:white; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; font-family:sans-serif;">
                    <h1>Escaneie o QR Code - {INSTANCE}</h1>
                    <div style="background:white; padding:20px; border-radius:10px; box-shadow: 0 0 20px rgba(34, 197, 94, 0.5);">
                        <img src="{qr_base64}" style="width:300px; height:300px;" />
                    </div>
                    <p style="margin-top:20px; color:#22c55e; font-weight:bold;">SINAL VERDE: API respondendo!</p>
                    <a href="/reset" style="color:grey; text-decoration:none; font-size:12px; margin-top:10px;">Resetar Instância</a>
                </body>
            </html>
            """
        
        # Se estiver conectado de verdade
        elif data.get("instance", {}).get("state") == "open":
            return """
            <body style="background:#0f172a; color:white; text-align:center; padding-top:100px; font-family:sans-serif;">
                <h1 style="color:#22c55e;">✅ STATUS: CONECTADO!</h1>
                <p>Seu WhatsApp já está autenticado.</p>
                <p>Você já pode rodar o Robô de Disparos.</p>
                <br>
                <a href="/reset" style="color:red;">Desconectar e Gerar Novo QR</a>
            </body>
            """
            
        else:
            # Caso caia no limbo, mostramos o erro real que a API está cuspindo
            return f"""
            <body style="background:#0f172a; color:white; text-align:center; padding-top:100px; font-family:sans-serif;">
                <h1>Aguardando QR Code...</h1>
                <p>Resposta da API: {data}</p>
                <script>setTimeout(() => {{ window.location.reload(); }}, 3000);</script>
            </body>
            """
    except Exception as e:
        return f"<h1>Erro de Conexão: {str(e)}</h1>"

@app.get("/reset")
async def reset_instance():
    headers = {"apikey": EVO_KEY}
    
    # 1. Deleta a instância zumbi
    requests.delete(f"{EVO_URL}/instance/delete/{INSTANCE}", headers=headers)
    
    # 2. Cria do zero FORÇANDO a integração correta (Baileys)
    payload = {
        "instanceName": INSTANCE,
        "token": EVO_KEY,
        "integration": "WHATSAPP-BAILEYS", # O SEGREDO ESTÁ AQUI
        "qrcode": True
    }
    
    response = requests.post(f"{EVO_URL}/instance/create", headers=headers, json=payload)
    
    if response.status_code == 201:
        return HTMLResponse("<h1>Resetado com Sucesso! <a href='/'>Volte para a Home</a> e o QR Code aparecerá agora.</h1>")
    else:
        return HTMLResponse(f"<h1>Erro no Reset: {response.text}</h1>")