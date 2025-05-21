import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
openai.api_key = os.getenv("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")

# Configuração do logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Função para o comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f'Olá {update.effective_user.first_name}! Sou seu novo bot. Use /help para ver meus comandos.'
    )

# Função para o comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Comandos disponíveis:
    /start - Inicia o bot
    /help - Mostra esta mensagem de ajuda
    /echo [mensagem] - Repete sua mensagem
    /info - Mostra informações sobre você
    /gpt [mensagem] - Fala com a IA do ChatGPT
    """
    await update.message.reply_text(help_text)

# Função para o comando /echo
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        await update.message.reply_text(' '.join(context.args))
    else:
        await update.message.reply_text("Use /echo seguido da mensagem que deseja que eu repita.")

# Função para o comando /info
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Suas informações:\n"
        f"ID: {user.id}\n"
        f"Nome: {user.first_name}\n"
        f"Username: @{user.username if user.username else 'Não definido'}"
    )

# Novo comando /gpt usando OpenAI
async def gpt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = " ".join(context.args)
    if not user_input:
        await update.message.reply_text("Use assim: /gpt sua pergunta")
        return

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente simpático e útil."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response['choices'][0]['message']['content']
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("Erro ao conectar com a IA.")

# Função para responder a comandos desconhecidos
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Desculpe, não entendi esse comando. Use /help para ver a lista de comandos disponíveis."
    )

def main():
    # Token do bot (obtém da variável de ambiente ou usa o valor direto)
    TOKEN = os.environ.get("7842704675:AAEf6lsuRYUOs0T29FXZSJ-Syck4dDhC7ps")

    # Cria a aplicação
    application = Application.builder().token(TOKEN).build()

    # Adiciona os handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("gpt", gpt_command))

    # Handler para comandos desconhecidos
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    # Imprime mensagem indicando que o bot está rodando
    print("Bot iniciado!")

    # Inicia o bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
