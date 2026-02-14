from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
import os

app = FastAPI()

EVO_URL = os.environ.get("EVOLUTION_URL")
EVO_KEY = os.environ.get("EVOLUTION_KEY")
INSTANCE = "Principal"

@app.get("/", response_class=HTMLResponse)
async def view_qr():
    # Rota de conexão da Evolution
    url = f"{EVO_URL}/instance/connect/{INSTANCE}"
    headers = {"apikey": EVO_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Se retornar o QR Code, exibe
        if "base64" in data:
            qr_base64 = data["base64"]
            return f"""
            <html>
                <body style="background:#0f172a; color:white; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; font-family:sans-serif;">
                    <h1>Escaneie o QR Code - {INSTANCE}</h1>
                    <div style="background:white; padding:20px; border-radius:10px;">
                        <img src="{qr_base64}" style="width:300px; height:300px;" />
                    </div>
                    <p style="margin-top:20px;"><a href="/reset" style="color:#ef4444; text-decoration:none; font-weight:bold;">NÃO APARECEU? CLIQUE AQUI PARA RESETAR INSTÂNCIA</a></p>
                </body>
            </html>
            """
        # Se cair aqui, a instância está em "limbo"
        else:
            status = data.get('instance', {}).get('state', 'unknown')
            return f"""
            <body style="background:#0f172a; color:white; text-align:center; padding-top:50px; font-family:sans-serif;">
                <h1>Estado: {status}</h1>
                <p>A API diz que já está conectada ou em erro.</p>
                <a href="/reset" style="background:#ef4444; color:white; padding:15px 30px; text-decoration:none; border-radius:5px; font-weight:bold;">FORÇAR RESET DA INSTÂNCIA</a>
                <p style="margin-top:20px; color:grey;">(Isso vai apagar a instância e criar de novo para gerar o QR Code)</p>
            </body>
            """
    except Exception as e:
        return f"<h1>Erro de Conexão: {str(e)}</h1>"

@app.get("/reset")
async def reset_instance():
    headers = {"apikey": EVO_KEY}
    # 1. Tenta deletar a instância atual para limpar o banco Neon
    requests.delete(f"{EVO_URL}/instance/delete/{INSTANCE}", headers=headers)
    
    # 2. Cria a instância do zero (Tipo Baileys)
    payload = {
        "instanceName": INSTANCE,
        "token": EVO_KEY,
        "qrcode": True
    }
    requests.post(f"{EVO_URL}/instance/create", headers=headers, json=payload)
    
    return HTMLResponse("<h1>Instância Resetada! <a href='/'>Volte para a Home</a> para ver o QR Code.</h1>")