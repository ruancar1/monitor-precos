import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import uvicorn

load_dotenv()

app = FastAPI()

# --- CONFIGURAÇÕES DO TELEGRAM ---
TOKEN_TELEGRAM = os.getenv("TOKEN_TELEGRAM")
CHAT_ID = os.getenv("CHAT_ID")


def enviar_aviso(mensagem):
    url_bot = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    requests.post(url_bot, data={"chat_id": CHAT_ID, "text": mensagem}, timeout=10)


# Modelo de dados que o frontend vai enviar
class DadosProduto(BaseModel):
    link: str
    preco_alvo: float


def converter_preco(texto):
    limpo = texto.replace('R$', '').replace('\xa0', '').replace(' ', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(limpo)
    except ValueError:
        return None


def extrair_preco(site):
    seletores = [
        '#corePriceDisplay_desktop_feature_div span.a-price:not(.a-text-price) span.a-offscreen',
        '#corePrice_feature_div span.a-price:not(.a-text-price) span.a-offscreen',
        '#corePrice_desktop span.a-price:not(.a-text-price) span.a-offscreen',
        '#apex_desktop span.a-price:not(.a-text-price) span.a-offscreen',
        '#price_inside_buybox',
        '#newBuyBoxPrice',
        '#kindle-price',
    ]
    for seletor in seletores:
        for elemento in site.select(seletor):
            preco = converter_preco(elemento.get_text())
            if preco is not None:
                return preco
    return None


# Rota 1: Entrega a página HTML quando acedemos ao site
@app.get("/")
def ler_index():
    return FileResponse("index.html")


# Rota 2: Recebe os dados do HTML, verifica o preço e responde
@app.post("/api/monitorar")
def monitorar_preco(dados: DadosProduto):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    try:
        resposta = requests.get(dados.link, headers=headers, timeout=10)
        site = BeautifulSoup(resposta.text, 'html.parser')

        preco_numero = extrair_preco(site)

        if preco_numero is None:
            return {"status": "erro", "mensagem": "Não foi possível encontrar o preço. A Amazon pode ter bloqueado a leitura."}

        if preco_numero <= dados.preco_alvo:
            aviso = f"🚨 O PREÇO CAIU!\nO produto está por R$ {preco_numero}.\nCompre aqui: {dados.link}"
            enviar_aviso(aviso)
            return {"status": "sucesso", "mensagem": f"Preço alvo atingido (R$ {preco_numero})! Aviso enviado no Telegram."}
        else:
            return {"status": "info", "mensagem": f"Monitorizando... Preço atual: R$ {preco_numero}. (Alvo: R$ {dados.preco_alvo})"}

    except Exception as e:
        return {"status": "erro", "mensagem": f"Erro de conexão: {str(e)}"}


# Inicia o servidor
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)