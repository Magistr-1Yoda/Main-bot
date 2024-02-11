import telebot
from telebot import types
import sqlite3
import random
db = sqlite3.connect('viktorina.db', check_same_thread = False)
import telebot
from telebot import types
import sqlite3
import MN



db = sqlite3.connect('viktorina.db', check_same_thread = False)
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS viktorina(
    chatid TEXT,
    username TEXT,
    score INT,
    name TEXT,
    surname TEXT
)""")
db.commit()


bot = telebot.TeleBot('6279309417:AAEs9jKOp18I_RYxc41EI2uI31zIV0ZxZcQ')
name = None
surname = None

def keyboards_create(MN, NumberColumns=1):
    keyboards = types.ReplyKeyboardMarkup(
        row_width=NumberColumns, resize_keyboard=True)
    btn_names = [types.KeyboardButton(text=x) for x in MN]
    keyboards.add(*btn_names)
    return keyboards

@bot.message_handler(commands=['start'])
def start(message):
    sql.execute(f"SELECT chatid FROM viktorina WHERE chatid = '{message.chat.id}'")
    if sql.fetchone() is None:
        db.commit()
    bot.send_message(message.from_user.id, MN.welcome_message,)
    bot.register_next_step_handler(message, user_name)
def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите свою фамилию')
    bot.register_next_step_handler(message, user_surname)
def user_surname(message):
    global surname
    people_id = message.chat.id
    sql.execute(f"SELECT chatid FROM viktorina WHERE chatid = {people_id}")
    data = sql.fetchone()
    if data is None:    
        surname = message.text.strip()
        sql.execute("INSERT INTO viktorina VALUES(?,?,?,?,?)", (message.chat.id, message.from_user.username, 0, name, surname))
        db.commit()
        bot.send_message(message.from_user.id, 'Пользователь успешно зарегестрирован')
    else: 
        bot.send_message(message.from_user.id, 'Вы успешно вошли в свой аккаунт')
    bot.send_message(message.from_user.id, 'Выберите интересующий раздел', reply_markup=keyboards_create(MN.welcome_keyboard)) 
@bot.message_handler(func = lambda m : m.text == '🛡️Викторина по цифровой безопастности')
def bes(message):
    bot.send_message(message.from_user.id, MN.message_bezopasno, reply_markup=keyboards_create (MN.otvet_keyboard))
@bot.message_handler(func = lambda m : m.text == 'Да👍🏻')
def bes(message):
    bot.send_message(message.from_user.id, MN.message_vopros1, reply_markup=keyboards_create(MN.bezopas1_keyboard)) 
@bot.message_handler(func = lambda m : m.text == '4-Все вышеперечисленное')
def bes(message):
    bot.send_message(message.from_user.id, 'Вы ответили совершенно верно🥳' , parse_mode='Markdown')
    sql.execute(f"UPDATE viktorina SET score = score + 10 WHERE chatid = {message.chat.id}")
    db.commit()
    for value in sql.execute(f"SELECT score FROM viktorina WHERE chatid = {message.chat.id}"):
        bot.send_message(message.chat.id, f"Отлично\nЯ выдал вам 10 очков за это задание\n \n Ваш баланс: {value[0]}", parse_mode='html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.from_user.id, 'Следущие вопросы вас ждут', reply_markup=keyboards_create(MN.sledushiy1_keyboard))
@bot.message_handler(func = lambda m : m.text == '3-Посадочные талоны')
def bes(message):
    bot.send_message(message.from_user.id, 'Вы ответили не верно, но в переди еще много вопросов!', reply_markup=keyboards_create(MN.sledushiy1_keyboard))
@bot.message_handler(func = lambda m : m.text == '2-Билеты на транспорт')
def bes(message):
    bot.send_message(message.from_user.id, 'Вы ответили не верно, но в переди еще много вопросов!', reply_markup=keyboards_create(MN.sledushiy1_keyboard))
@bot.message_handler(func = lambda m : m.text == '1-Фото паспорта и других документов')
def bes(message):
    bot.send_message(message.from_user.id, 'Вы ответили не верно, но в переди еще много вопросов!', reply_markup=keyboards_create(MN.sledushiy1_keyboard))


@bot.message_handler(func = lambda m : m.text == 'Следущий вопрос!')
def bes(message):
    bot.send_message(message.from_user.id, MN.message_vopros2, reply_markup=keyboards_create(MN.bezopas2_keyboard))
@bot.message_handler(func = lambda m : m.text == '2-Если нужно отправить сообщение в позднее время, не используй отложенные сообщения.')
def bes(message):
    bot.send_message(message.from_user.id, 'Вы ответили совершенно верно🥳' , parse_mode='Markdown')
    sql.execute(f"UPDATE viktorina SET score = score + 10 WHERE chatid = {message.chat.id}")
    db.commit()
    for value in sql.execute(f"SELECT score FROM viktorina WHERE chatid = {message.chat.id}"):
        bot.send_message(message.chat.id, f"Отлично\nЯ выдал вам 10 очков за это задание\n \n Ваш баланс: {value[0]}", parse_mode='html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.from_user.id, 'Следущие вопросы вас ждут', reply_markup=keyboards_create(MN.sledushiy2_keyboard))
@bot.message_handler(func = lambda m : m.text == '1-Обращайся в сети к незнакомым людям на «вы». Обязательно приветствуй собеседника в начале общения.')
def bes(message):
    bot.send_message(message.from_user.id, 'Вы ответили не верно, но в переди еще много вопросов!', reply_markup=keyboards_create(MN.sledushiy2_keyboard))
@bot.message_handler(func = lambda m : m.text == '3-Не записывай голосовые сообщения без согласия собеседника.')
def bes(message):
    bot.send_message(message.from_user.id, 'Вы ответили не верно, но в переди еще много вопросов!', reply_markup=keyboards_create(MN.sledushiy2_keyboard))
@bot.message_handler(func = lambda m : m.text == '4-Старайся формулировать мысль в одном сообщении и не отправляй множество коротких')
def bes(message):
    bot.send_message(message.from_user.id, 'Вы ответили не верно, но в переди еще много вопросов!', reply_markup=keyboards_create(MN.sledushiy2_keyboard))




@bot.message_handler(func = lambda m : m.text == 'Следущий вопрос!')
def bes(message):
    bot.send_message(message.from_user.id, MN.message_vopros3, reply_markup=keyboards_create(MN.bezopas3_keyboard))
@bot.message_handler(func = lambda m : m.text == '3-Все вышеперечисленное')
def bes(message):
    bot.send_message(message.from_user.id, 'Вы ответили совершенно верно🥳' , parse_mode='Markdown')
    sql.execute(f"UPDATE viktorina SET score = score + 10 WHERE chatid = {message.chat.id}")
    db.commit()
    for value in sql.execute(f"SELECT score FROM viktorina WHERE chatid = {message.chat.id}"):
        bot.send_message(message.chat.id, f"Отлично\nЯ выдал вам 10 очков за это задание\n \n Ваш баланс: {value[0]}", parse_mode='html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.from_user.id, 'Следущие вопросы вас ждут', reply_markup=keyboards_create(MN.sledushiy3_keyboard))
@bot.message_handler(func = lambda m : m.text == '1-Золотая середина между онлайн- и офлайн-миром.')
def bes(message):
    bot.send_message(message.from_user.id, 'Вы ответили не верно, но в переди еще много вопросов!', reply_markup=keyboards_create(MN.sledushiy3_keyboard))
@bot.message_handler(func = lambda m : m.text == '2-Специальная опция, предусмотренная на смартфонах для контроля онлайн пребывания в приложениях, сети.')
def bes(message):
    bot.send_message(message.from_user.id, 'Вы ответили не верно, но в переди еще много вопросов!', reply_markup=keyboards_create(MN.sledushiy3_keyboard))

bot.infinity_polling()