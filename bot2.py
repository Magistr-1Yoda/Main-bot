import telebot
from telebot import *
import database


def keyboards_create(MN, NumberColumns=1):
    keyboards = types.ReplyKeyboardMarkup(
        row_width=NumberColumns, resize_keyboard=True)
    btn_names = [types.KeyboardButton(text=x) for x in MN]
    keyboards.add(*btn_names)
    return keyboards


bot = telebot.TeleBot('6279309417:AAEs9jKOp18I_RYxc41EI2uI31zIV0ZxZcQ')

def welcome_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Программирование🤖')
    btn2 = types.KeyboardButton('Математика🔢')
    btn3 = types.KeyboardButton('Физика🔬')
    btn4 = types.KeyboardButton("Естественные науки🌳🦠🪲")
    btn5 = types.KeyboardButton('Космос🚀')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.from_user.id,f'Приветствуем вас в нашем чат-боте!\nМы приготовили для вас увлекательные викторины по физике, программирование, математике и естественным наукам. Давайте начнем наше путешествие в мир знаний! 🚀🔭', reply_markup=markup)


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
def send_question(chat_id, question, current_question):
    db.programming(chat_id, question, current_question)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(str(i)) for i in range(1, 5)]
    keyboard.add(*buttons)

    bot.send_message(
        chat_id,
        f'{question[1]}\n1. {question[2]}\n2. {question[3]}\n3. {question[4]}\n4. {question[5]}'
        ,reply_markup=keyboard
    )
    bot.register_next_step_handler(message, check_answer, question, current_question)
@bot.message_handler(func=lambda message: True)
def check_answer(message, question, current_question):
    try:
        answer = int(message.text)
        chat_id = message.chat.id

        correct_option = current_question[chat_id]['otvet']
        if answer == correct_option:
            bot.send_message(chat_id, 'Верно! Следующий вопрос:')
            send_question(chat_id)
        else:
            bot.send_message(chat_id, 'Неверно. Попробуйте еще раз:')
            send_question(chat_id )
    except ValueError:
        bot.send_message(chat_id, 'Пожалуйста, введите номер ответа.')
        send_question(chat_id )




if __name__ == '__main__':
    db = database.Database()
    bot.polling()