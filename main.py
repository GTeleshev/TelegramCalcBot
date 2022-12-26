from telebot import TeleBot, types
import time

TOKEN = input('Введите бот TOKEN (либо получить через BotFather: https://telegram.me/BotFather): ')

bot = TeleBot(TOKEN)
dct = {}


def get_time():
    curr = time.localtime()
    strtime = f'{curr.tm_year}.{curr.tm_mon}.{curr.tm_mday} - {curr.tm_hour}:{curr.tm_min}:{curr.tm_sec}'
    return strtime


def log_write(message, string_to_write):
    curr_time = get_time()
    full_str = f'{curr_time}: {string_to_write}\n'
    dct[message.id] = full_str
    doc = open('log.txt', 'a')
    with doc as d:
        doc.write(full_str)


def greeting(msg):
    bot.send_message(chat_id=msg.from_user.id, text=f'Здравствуйте. Выберите действие:\n'
                                                    f'/start - вызвать этот диалог\n'
                                                    f'/calc - использовать калькулятор\n'
                                                    f'/log - вывести лог действий пользователя')


@bot.message_handler(commands=['start', 'help'])
def answer(msg: types.Message):
    log_write(msg, 'start called')
    greeting(msg)


@bot.message_handler(commands=['calc'])
def answer(msg: types.Message):
    log_write(msg, 'calc called')
    markup = types.ReplyKeyboardMarkup()
    itema = types.KeyboardButton('+')
    itemb = types.KeyboardButton('-')
    itemc = types.KeyboardButton('*')
    itemd = types.KeyboardButton('/')
    markup.row(itema, itemb)
    markup.row(itemc, itemd)
    bot.send_message(chat_id = msg.from_user.id, text = 'Введите арифметическую операцию', reply_markup=markup)
    bot.register_next_step_handler(msg, handle_operation)


def handle_operation(msg):
    text = msg.text
    if text == '+':
        bot.register_next_step_handler(msg, sum_)
        bot.send_message(chat_id=msg.from_user.id, text='Введите слагаемые разделённые пробелом')
    elif text == '-':
        bot.register_next_step_handler(msg, sub_)
        bot.send_message(chat_id=msg.from_user.id, text='Введите уменьшаемое и вычитаемое разделённые пробелом')
    elif text == '*':
        bot.register_next_step_handler(msg, mult_)
        bot.send_message(chat_id=msg.from_user.id, text='Введите умножаемое и множитель разделённые пробелом')
    elif text == '/':
        bot.register_next_step_handler(msg, div_)
        bot.send_message(chat_id=msg.from_user.id, text='Введите делимое и делитель разделённые пробелом')
    else:
        bot.send_message(chat_id=msg.from_user.id, text='Вы прислали: ' + msg.text +
                                                        ', а должны были арифметическое действие')
        greeting()


def is_complex(ex):
    flag = True if "j" in ex else False
    if flag:
        return complex(ex)
    return float(ex)


def sum_(msg):
    a, b = map(is_complex, msg.text.split())
    log_write(msg, f'sum for {a}, {b} called')
    bot.send_message(chat_id=msg.from_user.id, text=f'Результат сложения {a + b}')
    greeting(msg)


def sub_(msg):
    a, b = map(is_complex, msg.text.split())
    log_write(msg, f'substraction for {a}, {b} called')
    bot.send_message(chat_id=msg.from_user.id, text=f'Результат вычитания {a - b}')
    greeting(msg)


def mult_(msg):
    a, b = map(is_complex, msg.text.split())
    log_write(msg, f'multiplication for {a}, {b} called')
    bot.send_message(chat_id=msg.from_user.id, text=f'Результат умножения {a * b}')
    greeting(msg)


def div_(msg):
    a, b = map(is_complex, msg.text.split())
    log_write(msg, f'multiplication for {a}, {b} called')
    bot.send_message(chat_id=msg.from_user.id, text=f'Результат деления {a / b}')
    greeting(msg)


@bot.message_handler(commands=['log'])
def answer(msg: types.Message):
    log_write(msg, 'log called')
    bot.send_message(chat_id=msg.from_user.id, text='Вывожу лог')
    print(dct)
    text_to_return = ""
    for keys, values in dct.items():
        text_to_return += f"{values}\n"
    bot.send_message(chat_id=msg.from_user.id, text=f'{text_to_return}')
    doc = open('log.txt', 'r')
    with doc as d:
        bot.send_document(chat_id=msg.from_user.id, document=d)
    greeting(msg)


bot.polling()
