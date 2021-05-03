# coding: utf-8
"""
    Telegram API wrapper doing all the Telegram stuff
"""

import configparser
import logging

import requests
import telebot

from ysk import speech_to_text

logging.basicConfig(level=logging.DEBUG)

parser = configparser.ConfigParser()
parser.read("config.ini")
ACCESS_KEY = parser["telegram"]["key"]
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

    try:
        file_id = message.voice.file_id
        file_info = bot.get_file(file_id)
        fbytes = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(ACCESS_KEY, file_info.file_path)).content

        with open("data/%d-%s.ogg" % (message.date, fromname), "wb") as wb:
            wb.write(fbytes)

        try:
            # обращение к нашему новому модулю
            text = speech_to_text(bytes=fbytes, key=YANDEX_KEY)
            logging.debug(f"This is what I heard: [%s]" % text)
            bot.reply_to(message, "Я распознал это так: [" + str(text) + "]")
        except Exception as se:
            logging.error("STT failed: %s" % str(se), exc_info=True)
            raise se

    except Exception as e:
        logging.error("Can't save voice", exc_info=True)
        bot.reply_to(message, "Не получилось ответить по этой причине: [%s]" % str(e))


@bot.message_handler(content_types=["text"])
def handle_text(message: telebot.types.Message):
    logging.debug(message)
    bot.reply_to(message, "Увы, бот воспринимает только голос и команды, начинающиеся на \"/\".")


bot.polling()
