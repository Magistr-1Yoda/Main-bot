import telebot
from telebot import *
import database


def keyboards_create(ListNameBTN, NumberColumns=2):
    keyboards = types.ReplyKeyboardMarkup(
    row_width=NumberColumns, resize_keyboard=True)
    btn_names = [types.KeyboardButton(text=x) for x in ListNameBTN]
    keyboards.add(*btn_names)
    return keyboards


bot = telebot.TeleBot('6279309417:AAE88A0P3Pc8F-dw9BLiMYXqsj5pprTyP6w')

def welcome_message(message):
    id = message.chat.id
    score = db.check_profile(id)
    data = db.get_table()
    if score[2] == 0:
        msg = bot.send_message(message.from_user.id,f'Приветствуем вас в нашем чат-боте!\nМы приготовили для вас увлекательные викторины по физике, программированию, математике и естественным наукам. Давайте начнем наше путешествие в мир знаний!🚀🔭', reply_markup=keyboards_create([data[0] , data[1], data[2], 'Естественные науки🌳🦠🪲' ,'Личная информация📋']))
        bot.register_next_step_handler(msg, choice, data)
    else:
        msg = bot.send_message(message.chat.id, "Вы вернулись в главное меню, здесь вы можете попробовать другие викторины!🔎🧠", reply_markup=keyboards_create([ data[0] , data[1], data[2], 'Естественные науки🌳🦠🪲' , 'Личная информация📋']))
        bot.register_next_step_handler(msg, choice, data)

def choice(message, data):
    enter = message.text
    if enter in data:
        msg = bot.send_message(message.chat.id, "В викторине будет 10 вопросов, время не ограничено, вы готовы?🏁✨", reply_markup=keyboards_create(['Главное меню🔙', 'Начать▶']))
        bot.register_next_step_handler(msg, start_choice, enter)
    elif enter == 'Естественные науки🌳🦠🪲':
        msg = bot.send_message(message.chat.id, "Выберите определенную тему🌏🧬🧪", reply_markup=keyboards_create([ data[3], data[4], data[5], 'Главное меню🔙']))
        bot.register_next_step_handler(msg, choice_Natural)
    elif enter == 'Личная информация📋':
        info(message, data)



def start_choice(message, enter):
    list_nub = [1,2,3,4,5,6,7,8,9,10]
    if message.text == 'Начать▶':
        if enter:
            send_question(message, list_nub, enter)
    elif message.text == 'Главное меню🔙':
        welcome_message(message)


def choice_Natural(message):
    enter = message.text
    if enter:
        choice(message)
    else:
        welcome_message(message)

@bot.message_handler(func = lambda m : m.text == 'Личная информация📋')
def info(message, data):
    id = message.chat.id
    score = db.check_profile(id)
    msg = bot.send_message(id, f"Вас зовут: {score[0]} {score[1]}. \nВаше количество баллов: {score[2]}🌟")
    bot.register_next_step_handler(msg, choice, data)

@bot.message_handler(commands=['start'])
def start(message):
    nic =  message.from_user.username
    id = message.chat.id
    new = db.check_human(id)
    if new is not None:
        welcome_message(message)
    elif new is None:
        list_names_surnames = []
        list_names_surnames.append(nic)
        bot.send_message(message.from_user.id, "Вы начали регестрацию💭 \nВведите своё имя:")
        bot.register_next_step_handler(message, names, list_names_surnames)


def names(message, list_names_surnames):
    names = message.text.strip()
    list_names_surnames.append(names)
    bot.send_message(message.from_user.id, "Введите свою фамилию:")
    bot.register_next_step_handler(message, surnames, list_names_surnames)

def surnames(message, list_names_surnames):
    surnames = message.text.strip()
    list_names_surnames.append(surnames)
    db.new_human(message.chat.id, list_names_surnames)
    welcome_message(message)


def send_question(message, list_nub, enter):
    if len(list_nub) != 0:
        random_number = random.choice(list_nub)
        if random_number in list_nub:
            id = message.chat.id
            data = db._test(id, random_number, enter)
            question = data[1]

            keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [types.KeyboardButton(str(i)) for i in range(1, 5)]
            keyboards.add(*buttons)

            bot.send_message(
                id,
                f'{question[1]}\n1. {question[2]}\n2. {question[3]}\n3. {question[4]}\n4. {question[5]}'
                ,reply_markup=keyboards
            )
        
            bot.register_next_step_handler(message, check_answer, id, data, list_nub, random_number, enter)
    elif len(list_nub) == 0:
        bot.send_message(message.chat.id,f'Вопросы кончились☹️ ')
        welcome_message(message)

def check_answer(message, id, data, list_nub, random_number, enter):
    try:
        answer = int(message.text)
        current_question = data[0]

        correct_option = current_question[id]['otvet']
        if answer == correct_option:
            bot.send_message(id, 'Верно, вы получили 10 баллов за этот вопрос!🥳')
            list_nub.remove(random_number)
            send_question(message, list_nub, enter)
            db.score(id)
            
        else:
            bot.send_message(id, 'Неверно🔥')
            list_nub.remove(random_number)
            send_question(message, list_nub, enter)
            
    except ValueError:
        bot.send_message(id, 'Пожалуйста, введите номер ответа')
        send_question(message, list_nub, enter)



if __name__ == '__main__':
    db = database.Database()
    bot.infinity_polling()