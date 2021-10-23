from ast import parse
import telebot
import os
import time
import schedule
from datetime import datetime
from multiprocessing import Process

from telebot.types import Message, Venue


all1 = {'Дима': '752872267', 'Паша': '629075242', 'Полина Кочеткова': '967925905', 'Виталик': '485433810', 'Витя': '1250087021', 'Полина Ковалева': '650761348',
        'Леша': '751974761', 'Ваня': '701727602', 'Наташа': '461883085', 'Максим': '688659984', 'Антон': '1084801379', 'Егор Белявский': '1280128315', 'Никита': '1242174386'}
hostel = {'Паша': '629075242', 'Полина Кочеткова': '967925905', 'Дима': '752872267', 'Ваня': '701727602',
          'Наташа': '461883085', 'Максим': '688659984', 'Антон': '1084801379', 'Егор Белявский': '1280128315', 'Никита': '1242174386'}
minsk = {'Егор Белявский': '1280128315', 'Виталик': '485433810',
         'Леша': '751974761', 'Антон': '1084801379'}
TOKEN = '1827746031:AAGKqa_5XyWhcBYtCIZ_QxhcQdmaoIHcHWQ'
CHAT_ID = '-1001185015555'
duty = ['@againTL @Tomasttt @greedann', '@Shuhmen @NiK1TA315',
        '@kowalskivarianty ', '@natarg @Fllloyd', '@Appolinapiya ', ]
bot = telebot.TeleBot(TOKEN)


class Nahui:

    def __init__(self, file_name):
        self.file_name = file_name
        self.stat = {}
        self.line = None
        self.date = None
        self.message = None

    def _set_time(self, line):
        if line.endswith('\n'):
            self.line = line[:-1]
        else:
            self.line = line
        self.date = '{} {}'.format(self.line[-6:-4], self.line[-3:-1])
        self.message = self.line[0:-8]

    def collect(self):
        with open(self.file_name, 'r', encoding='utf-8') as file:
            for line in file:
                self._set_time(line)
                self.stat[self.date] = f'{self.message}'

    def get_people(self, date):
        return self.stat[date]


def notify():
    now = datetime.now()
    date = now.strftime("%d %m")
    try:
        students = stat.get_people(date)
        message = f"Дежурные на неделю: {students}"
        bot.send_message(CHAT_ID, message, parse_mode="Markdown")
    except:
        bot.send_message(CHAT_ID, 'Дежурных нет идите нахуй',
                         parse_mode="Markdown")


@bot.message_handler(commands=['all'])
def tag_all(message):
    tag = ""
    for key, value in all1.items():
        tag += f'[{key}](tg://user?id={value}) '
    bot.send_message(message.chat.id, tag, parse_mode="Markdown")


@bot.message_handler(commands=['hostel'])
def tag_hostel(message):
    tag = ""
    for key, value in hostel.items():
        tag += f'[{key}](tg://user?id={value}) '
    bot.send_message(message.chat.id, tag, parse_mode="Markdown")


@bot.message_handler(commands=['minsk'])
def tag_minsk(message):
    tag = ""
    for key, value in minsk.items():
        tag += f'[{key}](tg://user?id={value}) '
    bot.send_message(message.chat.id, tag, parse_mode="Markdown")


@bot.message_handler(commands=['duty'])
def duty(message):
    tag_duty = '[Полина](tg://user?id=967925905)'
    bot.send_message(message.chat.id, tag_duty, parse_mode="Markdown")


stat = Nahui('list.txt')
stat.collect()
schedule.every().sunday.at("22:00").do(notify)


def loop():
    while True:
        schedule.run_pending()
        time.sleep(1)


def polly():
    print('bot started')
    bot.polling(none_stop=True)


if __name__ == '__main__':
    Process(target=polly).start()
    Process(target=loop).start()
