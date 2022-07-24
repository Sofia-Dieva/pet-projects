import telebot
from telebot import types
import random as r

goodboy = ['Молодец', 'Ты же знаешь,что ты особенный)', 'У тебя обязательно все получится', 'Я в тебя верю!']
bot = telebot.TeleBot(TOKEN)
zadachi = []


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Список задач')
    item2 = types.KeyboardButton('Получить похвалу')
    item3 = types.KeyboardButton('Посмотреть записанные дела')
    markup.add(item1, item2, item3)
    bot.send_message(message.from_user.id, f"Йоу,{message.from_user.first_name},я бот, который изначально создавался для записи дел ю ноу, но сейчас функционал расширили, дальше ты все увидишь, если запутаешься напиши '/help'", reply_markup=markup)


@bot.message_handler(commands=['help'])
def helper(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Список задач')
    item2 = types.KeyboardButton('Получить похвалу')
    item3 = types.KeyboardButton('Посмотреть записанные дела')
    markup.add(item1, item2, item3)
    bot.send_message(message.from_user.id, 'Все достаточно просто- нажимаешь на кнопочку и,если это связано с задачами, пишешь задачи,если хочешь сделать что-то другое, то просто нажми нужное на клавиатуре, но! если бот спрашивает тебя "Что-то еще?", следует ответить "нет", потому что иначе он запишет следующее сообщение в список задач', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Список задач":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Дополнить список задач')
        item2 = types.KeyboardButton('Удалить сделанные задачи')
        item3 = types.KeyboardButton('Назад')
        markup.add(item1, item2, item3)
        bot.send_message(message.from_user.id, "Давай посмотрим, что сегодня делаем с нашим списком задач", reply_markup=markup)
    elif message.text == 'Дополнить список задач':
        msg = bot.send_message(message.from_user.id, 'Напиши новые задачи')
        bot.register_next_step_handler(msg, adddel)
    elif message.text == 'Удалить сделанные задачи':
        msg = bot.send_message(message.from_user.id, 'Напиши задачи, которые нужно удалить')
        bot.register_next_step_handler(msg, deldela)
    elif message.text == "Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Список задач')
        item2 = types.KeyboardButton('Получить похвалу')
        item3 = types.KeyboardButton('Посмотреть записанные дела')
        markup.add(item1, item2, item3)
        bot.send_message(message.from_user.id, "Оки", reply_markup=markup)
    elif message.text == "Получить похвалу":
        bot.send_message(message.from_user.id, r.choice(goodboy))
    elif message.text == 'Посмотреть записанные дела':
        if len(zadachi) == 0:
            bot.send_message(message.from_user.id, 'Пока нет никаких задач)')
        else:
            bot.send_message(message.from_user.id, ''.join(zadachi))
    else:
        bot.send_message(message.from_user.id, "Малыш, ни черта не понимаю, либо ты тоже и мы два незнайки, либо ты требуешь от меня слишком многого")


def adddel(message):
    if message.text.lower() != 'нет':
        z = message.text
        zadachi.append(z.title().strip() + '\n')
        msg = bot.send_message(message.from_user.id, 'Что-нибудь еще?')
        bot.register_next_step_handler(msg, adddel)
        return
    msg= bot.send_message(message.from_user.id, 'Ну и славно')


def deldela(message):
    p = message.text + '\n'
    if p not in zadachi:
        bot.send_message(message.from_user.id, 'Этой задачи нет в списке')
    else:
        zadachi.remove(p)
        bot.send_message(message.from_user.id, 'Задача удалена из списка')


bot.polling(none_stop=True)
