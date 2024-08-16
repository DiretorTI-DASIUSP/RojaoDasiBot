import json
import os
import logging
from os.path import join, dirname
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler,MessageHandler, filters, ContextTypes
import asyncio
import datetime

# Carregar o nosso TOKEN - boa prática
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.environ.get("TOKEN")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def acende(update: Update, context: ContextTypes.DEFAULT_TYPE):
	# COLOCAR A RANDOMIZAÇÃO DE PRA PRA PRA
	name = update.message.from_user.first_name
	await update.message.reply_text(f"Olá, eu sou um bot! Como posso te ajudar, {name}?")

async def vemai(update: Update, context: ContextTypes.DEFAULT_TYPE):
	month = datetime.datetime.now().month
	msg = ""

	if 1 < month <= 5:
		msg = "TOC TOC, É O PANCADASI BATENDO NA TUA PORTA!!! TEM QUE SER MALUCO PRA PERDER!!!"

	if 5 < month <= 9:
		msg = "EU OUVI MELHOR FESTA DO ANO? ISSO MESMO, VEM AÍ A GLOW CARALHO!"

	await update.message.reply_text(msg)

application = None

async def initialize_application():
	global application
	
	if application is None:
		application = ApplicationBuilder().token(TOKEN).build()
		application.add_handler(CommandHandler("acende", acende))
		application.add_handler(CommandHandler("vemai", vemai))
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