import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_TELEGRAM = os.getenv("TOKEN_TELEGRAM")
CHAT_ID = os.getenv("CHAT_ID")

def enviar_aviso(mensagem):
    url_bot = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    dados = {"chat_id": CHAT_ID, "text": mensagem}
    requests.post(url_bot, data=dados)

# --- CONFIGURAÇÕES DO PRODUTO ---
url = 'https://www.amazon.com.br/Crime-castigo-Fiódor-Dostoiévski/dp/8573266465/'
preco_alvo = 100.00 # Deixei o alvo em 100.00 para forçar o código a mandar a mensagem agora!

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
}

# --- O MOTOR DO CÓDIGO ---
resposta = requests.get(url, headers=headers)
site = BeautifulSoup(resposta.text, 'html.parser')

preco_elemento = site.find('span', class_='a-offscreen')

if preco_elemento:
    preco_texto = preco_elemento.get_text()
    # Limpeza do texto para transformar em número
    preco_limpo = preco_texto.replace('R$', '').replace('\xa0', '').replace(' ', '').replace('.', '').replace(',', '.')
    preco_numero = float(preco_limpo)
    
    print(f"Preço na loja: R$ {preco_numero} | Seu alvo: R$ {preco_alvo}")
    
    if preco_numero <= preco_alvo:
        aviso = f"🚨 O PREÇO CAIU!\nO livro Crime e Castigo está por R$ {preco_numero}.\nCompre aqui: {url}"
        print("Enviando aviso para o seu Telegram...")
        enviar_aviso(aviso)
        print("Aviso enviado com sucesso!")
    else:
        print("❌ Ainda está caro. Nenhuma mensagem foi enviada.")

else:
    print("Não consegui encontrar o preço. A Amazon bloqueou o acesso.")