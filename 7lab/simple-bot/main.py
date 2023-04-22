import telebot
from telebot import types
import datetime
from math import ceil
import psycopg2

def day_timetable(day, week):
    cursor.execute("""
                       SELECT subject.title, subject.type, teacher.full_name,
                        timetable.room_numb, timetable.num
                        FROM subject
                        JOIN teacher ON (subject.id = teacher.subject_id)
                        JOIN timetable ON (subject.id = timetable.subject_id)
                        WHERE timetable.week = %s AND timetable.day = %s
                        ORDER BY timetable.num
                       """, (week, day))
    data = list(cursor.fetchall())
    days = ['понедельник','вторник','среда','четверг','пятница','суббота']
    time = ['09.30 - 11.05', '11.20 - 12.55', '13.10 - 14.45', '15.25 - 17.00', '17.15 - 18.50']
    if not data:
            return('____________\nВ такой день недели как ' + days[day-1] + ' занятий нет\n____________\n\n')
    msg = days[day-1] + '\n'
    msg += '____________\n'
    for lesson in range(1, 6):
        flag = 0
        for elem in data: 
            if lesson == elem[-1]:
                flag = 1
                temp = elem
        if flag == 0:
            msg += '<' + str(lesson) + '> ' + 'занятий нет\n'
        else:
            msg += '<' + str(lesson) + '> ' + time[lesson-1] + '\n' + temp[0] + " " + temp[1]
            msg += '\n' + temp[3] +' ' + temp[2] + '\n' 
    msg += '____________\n\n'
    return msg

def week_timetable(week):
    msg = ''
    for i in range(1, 7):
        msg += day_timetable(i, week)
    return msg

conn = psycopg2.connect(database = 'timetable',
                        user = 'postgres', password = 'k30042004',
                        host = 'localhost', port ='5432')
cursor = conn.cursor()

token = "6220917164:AAHfI-mnFXmyejCgMnl0NeZr8ISuRCI2ZeA"

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Понедельник", "Вторник")
    keyboard.row("Среда", "Четверг")
    keyboard.row("Пятница", "Суббота")
    keyboard.row("Расписание на текущую неделю")
    keyboard.row("Расписание на следующую неделю")
    bot.send_message(message.chat.id, 'Здравствуйте! Хотите узнать свежую информацию о МТУСИ?',
                      reply_markup=keyboard)
#Класс ReplyKeyboardMarkup создает пользовательскую клавиатуру с текстовыми кнопками    
#на месте стандартной клавиатуры.
#Метод row() заполняет клавиатуру кнопками.
#Метод send_massage отправляет пользователю сообщение.
#Аргумент message.chat.id используется для того, чтобы бот отправил сообщение тому
#пользователю, которые отправил сообщение, на которое бот в данный момент времени отвечает.
#Аргумент reply_markup=keyboard используется для отправки пользовательской клавиатуры,
#для её дальнейшего отображения.

@bot.message_handler(commands=['help'])
def start_message(message):
    msg = ''
    msg += 'Здравствуйте. С помощью данного бота вы можете узнать'
    msg += ' расписание группы БВТ2203 за 2 семестр этого года. Для того, '
    msg += 'чтобы бот выдал вам расписание, необходимо нажать на одну из кнопок\n\n'
    msg += 'Бот имеет следующие команды\n'
    msg += '/week - расписание на эту неделю\n'
    msg += '/mtuci - сайт университета.\n\n'
    msg += 'Приятного использования.'
    bot.send_message(message.chat.id, msg)
#В сообщение можно указать что умеет бот, включая команды, на которые он умеет реагировать

@bot.message_handler(commands=['week'])
def what_week(message):
    num_of_week = ceil((datetime.datetime.now() - datetime.datetime(2023,1,29)).days/7)
    s = "Сейчас " + str(num_of_week) + "-ая неделя"
    if num_of_week % 2 == 0:
        s += "(чётная)"
    else:
        s+= "(нечётная)"
    bot.send_message(message.chat.id, s)

@bot.message_handler(commands = ['mtuci'])
def link_mtuci(message):
    bot.send_message(message.chat.id, 'Сайт университета https://mtuci.ru/')

@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "понедельник":
        if ceil((datetime.datetime.now() - datetime.datetime(2023,1,29)).days/7) % 2 == 0:
            week = 2
        else:
            week = 1
        day = 1
        bot.send_message(message.chat.id, day_timetable(day, week))
    elif message.text.lower() == 'вторник':
        if ceil((datetime.datetime.now() - datetime.datetime(2023,1,29)).days/7) % 2 == 0:
            week = 2
        else:
            week = 1
        day = 2
        bot.send_message(message.chat.id, day_timetable(day, week))
    elif message.text.lower() == 'среда':
        if ceil((datetime.datetime.now() - datetime.datetime(2023,1,29)).days/7) % 2 == 0:
            week = 2
        else:
            week = 1
        day = 3
        bot.send_message(message.chat.id, day_timetable(day, week))
    elif message.text.lower() == 'четверг':
        if ceil((datetime.datetime.now() - datetime.datetime(2023,1,29)).days/7) % 2 == 0:
            week = 2
        else:
            week = 1
        day = 4
        bot.send_message(message.chat.id, day_timetable(day, week))
    elif message.text.lower() == 'пятница':
        if ceil((datetime.datetime.now() - datetime.datetime(2023,1,29)).days/7) % 2 == 0:
            week = 2
        else:
            week = 1
        day = 5
        bot.send_message(message.chat.id, day_timetable(day, week))
    elif message.text.lower() == 'суббота':
        if ceil((datetime.datetime.now() - datetime.datetime(2023,1,29)).days/7) % 2 == 0:
            week = 2
        else:
            week = 1
        day = 6
        bot.send_message(message.chat.id, day_timetable(day, week))
    elif message.text.lower() == "расписание на текущую неделю":
        if ceil((datetime.datetime.now() - datetime.datetime(2023,1,29)).days/7) % 2 == 0:
            week = 2
        else:
            week = 1
        bot.send_message(message.chat.id, week_timetable(week))
    elif message.text.lower() == "расписание на следующую неделю":
        if ceil((datetime.datetime.now() - datetime.datetime(2023,1,29)).days/7) % 2 == 0:
            week = 1
        else:
            week = 2
        bot.send_message(message.chat.id, week_timetable(week))
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял.")
#Данные декоратор должен стоять ниже, чем декораторы команд, так как в противном случае
#декораторы команд обрабатываться не будут, потому что команды в своем роде
#тоже текстовые сообщения.
#В этом декораторе аргумент content_type=['text'] отвечает за реакцию на текстовый тип контента
#сообщения.
#Для проверки конкретного текста используется условная конструкция с условием
#message.text.lower()=='<text>'
#Причем функция lower() отвезает за перевод текста в нижний регистр для удобства
#использования, и может применяться не только для библиотеки telebot, но и для 
#любых строковых операций и переменных
bot.infinity_polling()