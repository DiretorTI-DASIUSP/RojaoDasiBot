import json
import os
import logging
from os.path import join, dirname
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler,MessageHandler, filters, ContextTypes
import asyncio
import datetime
import boto3
from typing import Dict
from dotenv import load_dotenv

# Carregar o nosso TOKEN - boa prática
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
TOKEN = os.environ.get("TOKEN")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#Init S3
s3 = boto3.client(
	's3',
	aws_access_key_id = AWS_ACCESS_KEY_ID,
	aws_secret_access_key = AWS_SECRET_ACCESS_KEY
)

# s3 = boto3.client('s3') | IF IN LAMBDA FUNCTION

BUCKET_NAME = "contagem-rojao"
KEY = "contagem_rojao.json"

def _getContagem() -> Dict:
	response = s3.get_object(Bucket=BUCKET_NAME, Key=KEY)
	content = response['Body'].read().decode('utf-8')
	return json.loads(content)

def _putContagem() -> bool:
	cont = _getContagem()
	s3.put_object(Bucket = BUCKET_NAME, Key = KEY, Body = json.dumps({'contagem': cont['contagem'] + 1}))
	return True

#s3.put_object(Bucket = BUCKET_NAME, Key = KEY, Body = json.dumps({'contagem': 4033}))

async def acende(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	# COLOCAR A RANDOMIZAÇÃO DE PRA PRA PRA

	await asyncio.to_thread(_putContagem)
	mensagem = ["PRA PRA PRA  PRA POW POW", # Randomizar aqui <------
				"pra",
				"pra pra",
				"pra pra pra",
				"pow",
				"pow pow"]
	
	
	for texto in mensagem:
		await update.message.reply_text(texto, quote = False)
	
async def vemai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	month = datetime.datetime.now().month
	msg = ""

	if 4 <= month <= 5:
		msg = "TOC TOC, É O PANCADASI BATENDO NA TUA PORTA!!! TEM QUE SER MALUCO PRA PERDER!!!"

	elif 8 <= month <= 9:
		msg = "EU OUVI MELHOR FESTA DO ANO? ISSO MESMO, VEM AÍ A GLOW CARALHO!"

	else:
		msg = "SEM PREVISÃO PRA NADA, VAMO TRABALHAAAAAAAAAAR DASI"

	await update.message.reply_text(msg)

async def cagaram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	# Atualizar contagem aqui
	# await asyncio.to_thread(_putContagem)
	
	# Pode habilitar só quando for época de inter
	# Ou deixar sempre funcionando
	mensagem = ""
	
	# Se for pra deixar só quando for inter
	month = datetime.datetime.now().month
	if 4 <= month <= 5:
		mensagem = ["Pode fumar",
			"Pode beber",
			"Só não pode CAGAR NA PIAAAA"]
	else:
		mensagem = ["Cagar?",
			"COMO ASSIM??"]

	for texto in mensagem:
		await update.message.reply_text(texto, quote = False)

async def contagem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
	cont = await asyncio.to_thread(_getContagem)
	await update.message.reply_text(f"O DASI Já usou o Rojão DASIANO {cont['contagem']} vezes")


application = None

async def initialize_application():
	global application
	
	if application is None:
		application = ApplicationBuilder().token(TOKEN).build()
		application.add_handler(CommandHandler("acende", acende))
		application.add_handler(CommandHandler("vemai", vemai))
		application.add_handler(CommandHandler("contagem", contagem))
		application.add_handler(CommandHandler("cagaram", cagaram))
		await application.initialize()
		await application.start()
async def handle_request(event):
	try:
		logging.info("Processing request")
		update = Update.de_json(json.loads(event['body']), application.bot)
		await application.process_update(update)

		logging.info("Request processed successfully")

	except Exception as e:
		logging.error(f"Error processing update: {e}")
		raise
        
def lambda_handler(event, context) -> dict:
    # Inicializar nossa aplicação caso não tenha
	loop = asyncio.get_event_loop()
	if loop.is_closed():
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)

	loop.run_until_complete(initialize_application())
	loop.run_until_complete(handle_request(event))

    # Retornar uma mensagem de sucesso.
	return {
		'statusCode': 200,
		'body': json.dumps('Request processed successfully')
		
	}
