import os
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# AJUSTE CRÍTICO: Removendo qualquer barra extra da URL
EVO_URL = os.environ.get("EVOLUTION_URL", "").rstrip("/")
EVO_KEY = os.environ.get("EVOLUTION_KEY")
INSTANCE = "Principal"

@app.get("/", response_class=HTMLResponse)
async def home():
    # Rota direta para pegar o QR Code
    url = f"{EVO_URL}/instance/connect/{INSTANCE}"
    headers = {"apikey": EVO_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Se vier o Base64, o problema acabou!
        if data.get("base64"):
            return f"""
            <html><body style="background:#0f172a;color:white;text-align:center;padding-top:50px;font-family:sans-serif;">
                <h1>Escaneie agora!</h1>
                <div style="background:white;padding:20px;display:inline-block;border-radius:10px;">
                    <img src="{data['base64']}" style="width:300px;" />
                </div>
                <p>O QR Code expira rápido. <a href="/reset" style="color:red;">Resetar se sumir</a></p>
                <script>setTimeout(()=>{{location.reload()}}, 15000)</script>
            </body></html>
            """
        
        # Se vier o maldito {"count": 0}, forçamos um reload automático curto
        return f"""
            <html><body style="background:#0f172a;color:white;text-align:center;padding-top:100px;font-family:sans-serif;">
                <h1>Aguardando geração do QR...</h1>
                <p>Status da API: <b>{data}</b></p>
                <p><i>O motor Baileys está aquecendo, não feche esta página.</i></p>
                <script>setTimeout(()=>{{location.reload()}}, 5000)</script>
                <br><a href="/reset" style="color:red;">Forçar Novo Reset</a>
            </body></html>
            """
    except Exception as e:
        return f"<h1>Erro de Conexão: {str(e)}</h1>"

@app.get("/reset")
async def reset():
    headers = {"apikey": EVO_KEY}
    # Deleta com força
    requests.delete(f"{EVO_URL}/instance/delete/{INSTANCE}", headers=headers)
    
    # Criação Completa para v2.2.3
    payload = {
        "instanceName": INSTANCE,
        "token": EVO_KEY,
        "integration": "WHATSAPP-BAILEYS",
        "qrcode": True # GARANTE QUE O QR SEJA GERADO
    }
    requests.post(f"{EVO_URL}/instance/create", headers=headers, json=payload)
    return HTMLResponse("<h1>Reiniciando instância... <a href='/'>Clique aqui para ver o QR</a></h1>")