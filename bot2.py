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
    bot.send_message(message.from_user.id,f'Приветствуем вас в нашем чат-боте!\nМы приготовили для вас увлекательные викторины по физике, программированию, математике и естественным наукам. Давайте начнем наше путешествие в мир знаний!🚀🔭', reply_markup=keyboards_create(['Программирование🤖' , 'Математика🔢', 'Физика🔬', 'Естественные науки🌳🦠🪲', 'Космос🚀']))

@bot.message_handler(func = lambda m : m.text == 'Главное меню🔙')
def back(message):
    bot.send_message(message.chat.id, "Вы вернулись в главное меню, здесь вы можете попробовать другие викторины!🔎🧠", reply_markup=keyboards_create(['Программирование🤖' , 'Математика🔢', 'Физика🔬', 'Естественные науки🌳🦠🪲', 'Космос🚀']))

@bot.message_handler(commands=['start'])
def start(message):
    nic =  message.from_user.username
    id = message.chat.id
    new = db.check_human(id)
    if new is not None:
        bot.send_message(message.from_user.id, f"Такой пользователь уже есть в базе данных!")
        welcome_message(message)
    elif new is None:
        list_names_surnames = []
        list_names_surnames.append(nic)
        bot.send_message(message.from_user.id, "Вы начали регестрацию, введите своё имя:")
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


@bot.message_handler(func = lambda m : m.text == 'Программирование🤖')
def start1_programming(message):
    bot.send_message(message.chat.id, "Это викторина по программированию в ней будет 10 вопросов, время не ограничено, вы готовы?🏁✨", reply_markup=keyboards_create(['Главное меню🔙', 'Начать ▶']))


@bot.message_handler(func = lambda m : m.text == 'Начать ▶')
def start2_programming(message):
    list_nub = [1,2,3,4,5,6,7,8,9,10]
    send_question_programming(message, list_nub)

def send_question_programming(message, list_nub):
    if len(list_nub) != 0:
        random_number = random.choice(list_nub)
        if random_number in list_nub:
            id = message.chat.id
            data = db.programming(id, random_number)
            question = data[1]

            keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [types.KeyboardButton(str(i)) for i in range(1, 5)]
            keyboards.add(*buttons)

            bot.send_message(
                id,
                f'{question[1]}\n1. {question[2]}\n2. {question[3]}\n3. {question[4]}\n4. {question[5]}'
                ,reply_markup=keyboards
            )
        
            bot.register_next_step_handler(message, check_answer_programming, id, data, list_nub, random_number)
    elif len(list_nub) == 0:
        bot.send_message(message.chat.id,f'Вопросы кончились☹️ ')
        back(message)

@bot.message_handler(func=lambda message: True)
def check_answer_programming(message, id, data, list_nub, random_number):
    try:
        answer = int(message.text)
        current_question = data[0]

        correct_option = current_question[id]['otvet']
        if answer == correct_option:
            bot.send_message(id, 'Верно, вы получили 10 баллов за этот вопрос!🥳')
            list_nub.remove(random_number)
            send_question_programming(message, list_nub)
            db.score(id)
            print(list_nub)
        else:
            bot.send_message(id, 'Неверно🔥')
            list_nub.remove(random_number)
            send_question_programming(message, list_nub)
            print(list_nub)
    except ValueError:
        bot.send_message(id, 'Пожалуйста, введите номер ответа')
        send_question_programming(message, list_nub)


@bot.message_handler(func = lambda m : m.text == 'Физика🔬')
def start1_physics(message):
    bot.send_message(message.chat.id, "Это викторина по физике в ней будет 10 вопросов, время не ограничено, вы готовы?⭐", reply_markup=keyboards_create(['Главное меню🔙', 'Начать ▶']))


@bot.message_handler(func = lambda m : m.text == 'Начать ▶')
def start2_physics(message):
    list_nub = [1,2,3,4,5,6,7,8,9,10]
    send_question_physics(message, list_nub)

def send_question_physics(message, list_nub):
    if len(list_nub) != 0:
        random_number = random.choice(list_nub)
        if random_number in list_nub:
            id = message.chat.id
            data = db.physics(id, random_number)
            question = data[1]

            keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [types.KeyboardButton(str(i)) for i in range(1, 5)]
            keyboards.add(*buttons)

            bot.send_message(
                id,
                f'{question[1]}\n1. {question[2]}\n2. {question[3]}\n3. {question[4]}\n4. {question[5]}'
                ,reply_markup=keyboards
            )
        
            bot.register_next_step_handler(message, check_answer_physics, id, data, list_nub, random_number)
    elif len(list_nub) == 0:
        bot.send_message(message.chat.id,f'Вопросы кончились☹️ ')
        back(message)

@bot.message_handler(func=lambda message: True)
def check_answer_physics(message, id, data, list_nub, random_number):
    try:
        answer = int(message.text)
        current_question = data[0]

        correct_option = current_question[id]['otvet']
        if answer == correct_option:
            bot.send_message(id, 'Верно, вы получили 10 баллов за этот вопрос!🥳')
            list_nub.remove(random_number)
            send_question_physics(message, list_nub)
            db.score(id)
            print(list_nub)
        else:
            bot.send_message(id, 'Неверно🔥')
            list_nub.remove(random_number)
            send_question_physics(message, list_nub)
            print(list_nub)
    except ValueError:
        bot.send_message(id, 'Пожалуйста, введите номер ответа')
        send_question_physics(message, list_nub)
    
if __name__ == '__main__':
    db = database.Database()
    bot.infinity_polling()