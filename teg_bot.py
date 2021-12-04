from ast import parse
import telebot
import time
import schedule
from datetime import datetime
from multiprocessing import Process


all = {
    'Ceвa': '1021465762',
    'Антон': '1084801379',
    'Артём': '985490261',
    'Ваня': '701727602',
    'Виталик': '485433810',
    'Дима Борейко': '752872267',
    'Егор Белявский': '1280128315',
    'Егор Дробушевич': '1147728466',
    'Егор Крылов': '1986086510',
    'Егор Панковец': '790220005',
    'Леша': '751974761',
    'Максим': '688659984',
    'Негр': '1250087021',
    'Никита Белостоцкий': '1242174386',
    'Паша': '629075242',
    'Полина Ковалева': '650761348',
    'Полина Кочеткова': '967925905',
    'Помело': '461883085',
    'Саша Бренчанинов': '1318315130',
    'Серёжа': '994027544',
    'Дима Василевич': '1836814972',
    'Женя': '1010820388',
    'Саша Габриневский': '503086754',
    'Дед': '927086053',
    'Денис': '1123009924'
}

hostel = [
    'Ceвa',
    'Артём',
    'Ваня',
    'Дима Борейко',
    'Максим',
    'Негр',
    'Никита Белостоцкий',
    'Паша',
    'Полина Ковалева',
    'Полина Кочеткова',
    'Помело',
    'Саша Бренчанинов',
    'Серёжа',
]

minsk = [
    'Дед',
    'Саша Габриневский',
    'Женя',
    'Дима Василевич',
    'Егор Панковец',
    'Егор Крылов',
    'Егор Дробушевич',
    'Антон',
    'Виталик',
    'Егор Белявский',
    'Леша',
    'Денис',
]

TOKEN = '1827746031:AAGKqa_5XyWhcBYtCIZ_QxhcQdmaoIHcHWQ'
CHAT_ID = '-1001185015555'
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

    def notify(a=None):
        now = datetime.now()
        date = now.strftime("%d %m")
        try:
            students = stat.get_people(date)
        except:
            bot.send_message(
                CHAT_ID, 'Дежурных нет идите нахуй', parse_mode="Markdown")
        students = list(students.split(', '))
        tag = 'Дежурные на неделю: '
        for piple in students:
            tag += f'[{piple}](tg://user?id={all[piple]}), '
        tag = tag[:-2]
        bot.send_message(CHAT_ID, tag, parse_mode="Markdown")

    def collect(self):
        with open(self.file_name, 'r', encoding='utf-8') as file:
            for line in file:
                self._set_time(line)
                self.stat[self.date] = f'{self.message}'

    def get_people(self, date):
        return self.stat[date]


@bot.message_handler(commands=['all'])
def tag_all(message):
    tag = ""
    for key, value in all.items():
        tag += f'[{key}](tg://user?id={value}), '
    bot.send_message(message.chat.id, tag, parse_mode="Markdown")


@bot.message_handler(commands=['hostel'])
def tag_hostel(message):
    tag = ""
    for key in hostel:
        tag += f'[{key}](tg://user?id={all[key]}) '
    bot.send_message(message.chat.id, tag, parse_mode="Markdown")


@bot.message_handler(commands=['minsk'])
def tag_minsk(message):
    tag = ""
    for key in minsk:
        tag += f'[{key}](tg://user?id={all[key]}) '
    bot.send_message(message.chat.id, tag, parse_mode="Markdown")


@bot.message_handler(commands=['duty'])
def duty(message):
    stat.notify()


stat = Nahui('./list.txt')
stat.collect()
schedule.every().sunday.at("22:00").do(stat.notify)


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
