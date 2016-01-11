import telebot
import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.exams.third

TOKEN = '162083216:AAEIgURtX5BKFTaBL7x9nEg74mKGElWjskA'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hola, este bot te recuerda\
 cuando son tus examenes, escribe /help para mas info.")

@bot.message_handler(commands=['help'])
def show_help(message):
    bot.reply_to(message, "escribe /exams para ver todas las fechas,\
 escribe la abreviatura de la asignatura para verla en detalle.")

@bot.message_handler(commands=['exams'])
def show_exams(message):

	result = ""

	for post in db.find():
		result = result + "\n" + str(post['details']['date']['day']) + " de "\
+ post['details']['date']['month'] + ", "  + post['initials']

	bot.reply_to(message,result)

@bot.message_handler(func=lambda message: True)
def echo_message(message):




	number = db.count({"initials": message.text.upper()})

	if number == 1:
		query = db.find_one({"initials": message.text.upper()})

		result = query['name'] + ", " + str(query['details']['date']['day']) + " de "\
+ query['details']['date']['month'] + "\nAula/s: " + query['details']['classroom']\
+ "\nTurno: " + query['details']['turn']

		bot.reply_to(message,result)

	else:
		bot.reply_to(message,"Asignatura no encontrada")

bot.polling()