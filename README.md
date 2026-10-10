# Monitor de Preços

Aplicação web que verifica o preço de um produto da Amazon Brasil e avisa no Telegram quando ele chega ao valor que você quer pagar.

## Como funciona

1. Você cola o link do produto e informa o preço alvo em R$ na interface.
2. O servidor (FastAPI) busca a página da Amazon e extrai o preço atual com BeautifulSoup.
3. Se o preço atual for menor ou igual ao alvo, um bot do Telegram envia uma mensagem com o valor e o link de compra.
4. Se ainda estiver acima do alvo, a interface mostra o preço atual e o alvo.

Cada clique em **Iniciar Monitoramento** faz uma verificação.

## Tecnologias

- Python 3
- FastAPI e Uvicorn
- Requests e BeautifulSoup4
- python-dotenv
- HTML, CSS e JavaScript puros no front-end
- API de bots do Telegram

## Como rodar

### 1. Clone o repositório

```bash
git clone https://github.com/ruancar1/monitor-precos.git
cd monitor-precos
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

No Windows, se o `pip` não for reconhecido, use `py -m pip install -r requirements.txt`.

### 3. Crie o bot do Telegram

1. No Telegram, converse com o [@BotFather](https://t.me/BotFather), envie `/newbot` e siga as instruções. Ele vai te entregar o **token** do bot.
2. Envie qualquer mensagem para o seu bot recém-criado.
3. Descubra seu **chat ID**, por exemplo conversando com o [@userinfobot](https://t.me/userinfobot).

### 4. Configure o `.env`

Copie o modelo e preencha com seus valores:

```bash
cp .env.example .env
```

No Windows, basta copiar e renomear o arquivo `.env.example` para `.env`.

```
TOKEN_TELEGRAM=seu_token_aqui
CHAT_ID=seu_chat_id_aqui
```

> O `.env` está no `.gitignore` e nunca deve ser enviado ao GitHub. Se o seu token vazar, revogue-o no @BotFather.

### 5. Inicie o servidor

```bash
python main.py
```

Abra [http://127.0.0.1:8000](http://127.0.0.1:8000) no navegador.

## Estrutura

```
monitor-precos/
├── main.py           # servidor FastAPI (rota da página e rota /api/monitorar)
├── index.html        # interface
├── monitor.py        # script avulso de teste, com um produto fixo no código
├── .env.example      # modelo das variáveis de ambiente
├── requirements.txt
└── .gitignore
```

## Limitações

- **A Amazon pode bloquear a leitura.** Ela detecta acessos automáticos e às vezes devolve uma página de verificação (captcha). Nesse caso o app avisa que não encontrou o preço.
- **O scraping depende do HTML da Amazon**, que muda com frequência. Se o preço deixar de ser encontrado, os seletores da função `extrair_preco` em `main.py` podem precisar de ajuste.
- A verificação acontece quando você clica no botão. Não há agendamento automático em segundo plano.

## Ideias para evoluir

- Verificar o preço automaticamente em intervalos de tempo
- Monitorar vários produtos ao mesmo tempo
- Guardar o histórico de preços
- Usar a API oficial de afiliados da Amazon em vez de scraping

## Autor

Feito por Ruan ([@ruancar1](https://github.com/ruancar1)).
