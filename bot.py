# coding: utf-8

import configparser
import logging

import requests
import telebot

from ysk_access import speech_to_text, SpeechException

logging.basicConfig(level=logging.DEBUG)

parser = configparser.ConfigParser()
parser.read("config.ini")
ACCESS_KEY = parser["access"]["key"]
YANDEX_KEY = parser["yandex"]["key"]

bot = telebot.TeleBot(ACCESS_KEY, num_threads=4)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    logging.debug(message)
    bot.reply_to(message, "Здравствуйте, поговорите что-нибудь, а я попробую это превратить в текст.")


@bot.message_handler(content_types=['voice'])
def handle_voice(message: telebot.types.Message):

    logging.debug(message)
    fromname = message.from_user.username
    bot.reply_to(message, "Спасибо.")

    try:
        file_id = message.voice.file_id
        file_info = bot.get_file(file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(ACCESS_KEY, file_info.file_path)).content

        with open("data/%d-%s.ogg" % (message.date, fromname), "wb") as wb:
            wb.write(file)

        try:
            # обращение к нашему новому модулю
            text = speech_to_text(bytes=file, key=YANDEX_KEY)
            print(text)
            bot.reply_to(message, "This? " + str(text))
        except SpeechException as se:
            print(se, "NOT OKAY")
        else:
            print("OKAY")

        bot.reply_to(message, "Принято Спасибо.")
        # bot.reply_to(message, "Едем дальше.")
    except Exception as e:
        logging.error("Can't save voice", exc_info=True)
        bot.reply_to(message, "Problems saving your response: " + str(e))


@bot.message_handler(content_types=["text"])
def handle_text(message: telebot.types.Message):
    logging.debug(message)
    bot.reply_to(message, "Бот воспринимает только голос и команды.")


bot.polling()
