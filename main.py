import os, requests, time
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
EVO_URL = os.environ.get("EVOLUTION_URL", "").rstrip("/")
EVO_KEY = os.environ.get("EVOLUTION_KEY")
INSTANCE = "Principal"

@app.get("/", response_class=HTMLResponse)
async def home():
    url = f"{EVO_URL}/instance/connect/{INSTANCE}"
    headers = {"apikey": EVO_KEY}
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Se o loop acabar e o QR nascer
        if data.get("base64"):
            return f"""<html><body style="background:#0f172a;color:white;text-align:center;padding-top:50px;font-family:sans-serif;">
                <h1>QR CODE GERADO!</h1>
                <img src="{data['base64']}" style="width:300px;border:10px solid white;border-radius:10px;" />
                <p>Escaneie rápido antes do próximo reinício.</p>
                <script>setTimeout(()=>{{location.reload()}}, 10000)</script>
            </body></html>"""
        
        # Interface de espera com diagnóstico
        return f"""<html><body style="background:#0f172a;color:white;text-align:center;padding-top:100px;font-family:sans-serif;">
            <h1>Aguardando Estabilização...</h1>
            <p>A API está em loop de boot. Tentando pescar o código...</p>
            <p style="background:#1e293b;padding:10px;display:inline-block;">Status Atual: {data}</p>
            <br><br>
            <a href="/reset" style="background:red;color:white;padding:15px;text-decoration:none;border-radius:5px;">EXECUTAR RESET NUCLEAR</a>
            <script>setTimeout(()=>{{location.reload()}}, 3000)</script>
        </body></html>"""
    except:
        return "<h1>Servidor Offline ou Reiniciando...</h1>"

@app.get("/reset")
async def nuclear_reset():
    headers = {"apikey": EVO_KEY}
    
    # 1. Limpeza total
    requests.delete(f"{EVO_URL}/instance/delete/{INSTANCE}", headers=headers)
    time.sleep(3) # Tempo para o banco Neon respirar
    
    # 2. Criação seguindo as Soluções Comuns que você encontrou
    payload = {
        "instanceName": INSTANCE,
        "token": EVO_KEY,
        "integration": "WHATSAPP-BAILEYS", # Integração correta
        "qrcode": True,                    # Força a geração do QR
        "browser": "Chrome"                # Garante compatibilidade
    }
    
    response = requests.post(f"{EVO_URL}/instance/create", headers=headers, json=payload)
    
    if response.status_code == 201:
        return HTMLResponse("<h1>Versão Sincronizada! <a href='/'>Volte para a Home</a> e o QR Code deve aparecer em 10s.</h1>")
    else:
        return HTMLResponse(f"<h1>Erro na Criação: {response.text}</h1>")