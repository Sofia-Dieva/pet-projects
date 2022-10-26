import telebot
from telebot import types
bot = telebot.TeleBot('token')
admin = 'admin id'
users = []
black_list = []
user_dict = {}
jaloba_dict = {}

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id not in users:
        chat_id = message.chat.id
        user_dict[chat_id] = []
        msg = bot.send_message(message.from_user.id, 'send name name')
        bot.register_next_step_handler(msg, name)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('/mainpage')
        markup.add(item1)


def name(message):
    if len(message.text.split()) == 2:
        user_dict[message.chat.id].append(message.text)
        msg = bot.send_message(message.from_user.id, 'send phone')
        bot.register_next_step_handler(msg, number)
    else:
        msg = bot.send_message(message.from_user.id, 'Neverno try again')
        bot.register_next_step_handler(msg, name)

def number(message):
    if len(message.text) == 12 and message.text.startswith('+7'):
        user_dict[message.chat.id].append(message.text)
        users.append(message.chat.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('/mainpage')
        markup.add(item1)
        bot.send_message(message.from_user.id, 'Done', reply_markup=markup)
    else:
        msg = bot.send_message(message.from_user.id, 'Neverno try again')
        bot.register_next_step_handler(msg, number)

@bot.message_handler(func=lambda message: message.chat.id not in users or message.chat.id in black_list)
def some(message):
   bot.send_message(message.chat.id, "Sorry, you don`t have access")

@bot.message_handler(commands=['sendmessage'])
def msg_from_bot(message):
    if message.from_user.id == admin:
        send = bot.send_message(message.from_user.id, 'Введите сообщение')
        bot.register_next_step_handler(send, msg_from_bot1)
    else:
        bot.send_message(message.chat.id, 'you can`t do that')

def msg_from_bot1(message):
    for i in users:
        bot.send_message(i, message.text)
    bot.send_message(message.chat.id, 'Well done')

@bot.message_handler(commands=['viewallusers'])
def viewall(message):
    if message.from_user.id == admin:
        for i, l in user_dict.items():
            bot.send_message(message.from_user.id, f'{i}:{",".join(l)}')
    else:
        bot.send_message(message.from_user.id, 'you can`t do that')

@bot.message_handler(commands=['addtoblacklist'])
def addtobl(message):
    if message.from_user.id == admin:
        send = bot.send_message(message.from_user, 'Введите user id')
        bot.register_next_step_handler(send, addtobl1)
    else:
        bot.send_message(message.chat.id, 'you can`t do that')


def addtobl1(message):
    black_list.append(message.text)
    bot.send_message(message.chat.id, 'Done')

@bot.message_handler(commands=['removefromblacklist'])
def rembl(message):
    if message.from_user.id == admin:
        send = bot.send_message(message.from_user.id, 'Введите user id')
        bot.register_next_step_handler(send, rembl1)
    else:
        bot.send_message(message.from_user.id, 'you can`t do that')


def rembl1(message):
    black_list.remove(message.text)
    bot.send_message(message.from_user.id, 'Done')

@bot.message_handler(commands=['mainpage'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Оставить заявку')
    item2 = types.KeyboardButton('Связаться')
    item3 = types.KeyboardButton('Настройки')
    item4 = types.KeyboardButton('Полезные контакты')
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.from_user.id,'Добро пожаловать в главное меню чат-бота Управляющей компании "УЭР-ЮГ". Здесь'
        , reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def skipitem(call):
    if call.data == 'skip':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        menu3 = telebot.types.InlineKeyboardMarkup()
        menu3.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back2'))
        menu3.add(telebot.types.InlineKeyboardButton(text='Пропустить', callback_data='skip2'))
        msg = bot.send_message(call.message.chat.id, 'Хотите добавить фото?',reply_markup=menu3)
        bot.register_next_step_handler(msg, step3)
    elif call.data == 'skip2':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        final = ' '.join([i for i in jaloba_dict[call.message.chat.id]])
        bot.send_message(admin, f'user{user_dict[call.message.chat.id][0]} write:{final}')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Оставить заявку')
        item2 = types.KeyboardButton('Связаться')
        item3 = types.KeyboardButton('Настройки')
        item4 = types.KeyboardButton('Полезные контакты')
        markup.add(item1, item2, item3, item4)
        msg = bot.send_message(call.message.chat.id, 'Good we ychtem', reply_markup=markup)
        bot.register_next_step_handler(msg, get_text_messages)
    elif call.data == 'back':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Оставить заявение')
        item2 = types.KeyboardButton('Поделиться предложением')
        item3 = types.KeyboardButton('Назад')
        markup.add(item1, item2, item3)
        msg = bot.send_message(call.message.chat.id, "Выберите категорию", reply_markup=markup)
        bot.register_next_step_handler(msg, get_text_messages)
    elif call.data == 'back2':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        menu1 = telebot.types.InlineKeyboardMarkup()
        menu1.add(telebot.types.InlineKeyboardButton(text='Пропустить', callback_data='skip'))
        menu1.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back'))
        msg = bot.send_message(call.message.chat.id, 'step 1', reply_markup=menu1)
        bot.register_next_step_handler(msg, zayavca)
    elif call.data == 'photo':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        msg = bot.send_message(call.message.chat.id, 'Send photo')
        bot.register_next_step_handler(msg, step3)
    elif call.data == 'endup':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, 'Диалог завершен')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Полезные контакты":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Назад')
        markup.add(item1)
        bot.send_message(message.from_user.id, "Текст про контакты компании", reply_markup=markup)
    elif message.text == 'Связаться':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Перезвоните мне')
        item2 = types.KeyboardButton('Свяжитесь со мной в чат-боте')
        item3 = types.KeyboardButton('Назад')
        markup.add(item1, item2, item3)
        bot.send_message(message.from_user.id, "Выберите способ", reply_markup=markup)
    elif message.text == 'Перезвоните мне':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Да')
        item2 = types.KeyboardButton('Оставить номер телефона')
        markup.add(item1, item2)
        msg = bot.send_message(message.from_user.id, f"{user_dict[message.chat.id][1]} this is ur number?", reply_markup=markup)
        bot.register_next_step_handler(msg, done_zayavka)
    elif message.text == 'Да':
        msg = bot.send_message(message.from_user.id, 'we will call you as soon as possible')
        bot.register_next_step_handler(msg, done_zayavka)
    elif message.text == 'Оставить номер телефона':
        msg = bot.send_message(message.from_user.id, 'write new number')
        bot.register_next_step_handler(msg, done_zayavka)
    elif message.text == 'Свяжитесь со мной в чат-боте':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Да')
        item2 = types.KeyboardButton('Оставить номер телефона')
        markup.add(item1, item2)
        msg = bot.send_message(message.from_user.id, 'Добрый день, напишите вопрос и ожидайте ответа', reply_markup=markup)
        bot.register_next_step_handler(msg, talktoadmin)
    elif message.text == 'Настройки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Поменять имя')
        item2 = types.KeyboardButton('Сменить номер')
        item3 = types.KeyboardButton('Назад')
        markup.add(item1, item2, item3)
        bot.send_message(message.from_user.id, "Тут можете поменять имя и телефон", reply_markup=markup)
    elif message.text == 'Оставить заявку':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Оставить заявление')
        item2 = types.KeyboardButton('Поделиться предложением')
        item3 = types.KeyboardButton('Назад')
        markup.add(item1, item2, item3)
        bot.send_message(message.from_user.id, "Выберите категорию", reply_markup=markup)
    elif message.text == 'Оставить заявление':
        menu1 = telebot.types.InlineKeyboardMarkup()
        menu1.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back'))
        msg = bot.send_message(message.from_user.id, 'Опишите проблему', reply_markup=menu1)
        jaloba_dict[message.chat.id] = []
        bot.register_next_step_handler(msg, zayavca)
    elif message.text == 'Поменять имя':
        msg = bot.send_message(message.from_user.id, 'send new name')
        bot.register_next_step_handler(msg, new_name)
    elif message.text == 'Поделиться предложением':
        msg = bot.send_message(message.from_user.id, 'send предложение')
        bot.register_next_step_handler(msg, predlozenie)
    elif message.text == 'Сменить номер':
        msg = bot.send_message(message.from_user.id, 'send new number')
        bot.register_next_step_handler(msg, new_number)
    elif message.text == "Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Оставить заявку')
        item2 = types.KeyboardButton('Связаться')
        item3 = types.KeyboardButton('Настройки')
        item4 = types.KeyboardButton('Полезные контакты')
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.from_user.id,'return to main page', reply_markup=markup)

def zayavca(message):
    jaloba_dict[message.chat.id].append(message.text)
    menu2 = telebot.types.InlineKeyboardMarkup()
    menu2.add(telebot.types.InlineKeyboardButton(text='Пропустить', callback_data='skip'))
    menu2.add(telebot.types.InlineKeyboardButton(text='Назад', callback_data='back2'))
    msg = bot.send_message(message.from_user.id, 'Напишите адрес или пропустите этот пункт', reply_markup=menu2)
    bot.register_next_step_handler(msg, step2)


def step2(message):
    jaloba_dict[message.chat.id].append(message.text)
    menu5 = telebot.types.InlineKeyboardMarkup()
    menu5.add(telebot.types.InlineKeyboardButton(text='Пропустить', callback_data='skip2'))
    menu5.add(telebot.types.InlineKeyboardButton(text='Да', callback_data='photo'))
    msg = bot.send_message(message.chat.id, 'Хотите добавить фото?', reply_markup=menu5)
    bot.register_next_step_handler(msg, step3)

def step3(message):
    if message.content_type == 'photo':
        final = ' '.join([i for i in jaloba_dict[message.chat.id]])
        bot.send_message(admin, f'user{message.from_user.id} write:{final}')
        bot.forward_message(admin, message.chat.id, message.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Оставить заявку')
        item2 = types.KeyboardButton('Связаться')
        item3 = types.KeyboardButton('Настройки')
        item4 = types.KeyboardButton('Полезные контакты')
        markup.add(item1, item2, item3, item4)
        msg = bot.send_message(message.from_user.id, 'Good we ychtem', reply_markup=markup)
        bot.register_next_step_handler(msg, get_text_messages)
    elif message.text == 'Нет':
        final = ' '.join([i for i in jaloba_dict[message.chat.id]])
        bot.send_message(admin, f'user{user_dict[message.chat.id][0]} write:{final}')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Оставить заявку')
        item2 = types.KeyboardButton('Связаться')
        item3 = types.KeyboardButton('Настройки')
        item4 = types.KeyboardButton('Полезные контакты')
        markup.add(item1, item2, item3, item4)
        msg = bot.send_message(message.from_user.id, 'Good we ychtem', reply_markup=markup)
        bot.register_next_step_handler(msg, get_text_messages)
    else:
        msg = bot.send_message(message.from_user.id, 'try only img or write "Нет"')
        bot.register_next_step_handler(msg, step3)

def talktoadmin(message):
    menu5 = telebot.types.InlineKeyboardMarkup()
    menu5.add(telebot.types.InlineKeyboardButton(text='Завершить диалог', callback_data='endup'))
    msg = bot.send_message(admin, f'только что поступило сообщение от {user_dict[message.chat.id][0]}:{message.text}',reply_markup=menu5)
    bot.register_next_step_handler(msg, otvet, m=message.chat.id)

def otvet(message, m):
    menu5 = telebot.types.InlineKeyboardMarkup()
    menu5.add(telebot.types.InlineKeyboardButton(text='Завершить диалог', callback_data='endup'))
    msg = bot.send_message(m, message.text,reply_markup=menu5)
    bot.register_next_step_handler(msg, talktoadmin)


def predlozenie(message):
    if message.content_type == 'text':
        bot.send_message(admin, f'this user{user_dict[message.chat.id][0]} предлагает {message.text}')
        bot.send_message(message.from_user.id, 'Thanks')
    else:
        msg = bot.send_message(message.from_user.id, 'try only text')
        bot.register_next_step_handler(msg, predlozenie)

def new_name(message):
    if len(message.text.split())==2:
        user_dict[message.chat.id][0] = message.text
        bot.send_message(message.from_user.id, 'Done')
    else:
        msg = bot.send_message(message.from_user.id, 'Neverno try again')
        bot.register_next_step_handler(msg, new_name)

def new_number(message):
    if len(message.text)==12 and message.text.startswith('+7'):
        user_dict[message.chat.id][1] = message.text
        bot.send_message(message.from_user.id, 'Done')
    else:
        msg = bot.send_message(message.from_user.id, 'Neverno try again')
        bot.register_next_step_handler(msg, new_number)

def done_zayavka(message):
    if message.text == 'Да':
        bot.send_message(admin, f'this user {user_dict[message.chat.id][0]} want to call. Number {user_dict[message.chat.id][1]}')
        bot.send_message(message.from_user.id, 'we will call you as soon as possible')
    elif message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Оставить заявку')
        item2 = types.KeyboardButton('Связаться')
        item3 = types.KeyboardButton('Настройки')
        item4 = types.KeyboardButton('Полезные контакты')
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.from_user.id, 'return to main page', reply_markup=markup)
    else:
        bot.send_message(admin, f'this user {user_dict[message.chat.id][0]} want to call on this number {message.text}')
        bot.send_message(message.from_user.id, 'we will call you as soon as possible')

bot.polling(none_stop=True)
