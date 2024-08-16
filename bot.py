import json
import os
import logging
from os.path import join, dirname
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler,MessageHandler, filters, ContextTypes
import asyncio

# Carregar o nosso TOKEN - boa prática
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.environ.get("TOKEN")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	name = update.message.from_user.first_name
	await update.message.reply_text(f"Olá, eu sou um bot! Como posso te ajudar, {name}?")

async def teste(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	await update.message.reply_text("Comando recebido com sucesso!")
	
application = None

async def initialize_application():
	global application
	
	if application is None:
		application = ApplicationBuilder().token(TOKEN).build()
		application.add_handler(CommandHandler("start", start))
		application.add_handler(MessageHandler(filters.COMMAND, teste))
		await application.initialize()

async def handle_request(event):
	try:
		logging.info("Processing request")
		update = Update.de_json(json.loads(event['body']), application.bot)
		await application.process_update(update)

		logging.info("Request processed successfully")

	except Exception as e:
		logging.error(f"Error processing update: {e}")
		raise
        
def lambda_handler(event, context):
	asyncio.run(initialize_application())
	asyncio.run(handle_request(event))

	return {
	'statusCode': 200,
	'body': json.dumps('Request processed successfully!')
	}