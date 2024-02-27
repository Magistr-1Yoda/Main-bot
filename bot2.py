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
    bot.send_message(message.from_user.id,f'Приветствуем вас в нашем чат-боте!\nМы приготовили для вас увлекательные викторины по физике, программирование, математике и естественным наукам. Давайте начнем наше путешествие в мир знаний! 🚀🔭', reply_markup=keyboards_create(['Программирование🤖' , 'Математика🔢', 'Физика🔬', 'Естественные науки🌳🦠🪲', 'Космос🚀']))


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

list_nub = [1,2,3,4,5,6,7,8,9,10]
@bot.message_handler(func = lambda m : m.text == 'Программирование🤖')
def send_question_programming(message):
    if len(list_nub) != 0:
        random_number = random.choice(list_nub)
        if random_number in list_nub:
            chat_id = message.chat.id
            data = db.programming(chat_id, random_number)
            question = data[1]

            keyboards = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = [types.KeyboardButton(str(i)) for i in range(1, 5)]
            keyboards.add(*buttons)

            bot.send_message(
                chat_id,
                f'{question[1]}\n1. {question[2]}\n2. {question[3]}\n3. {question[4]}\n4. {question[5]}'
                ,reply_markup=keyboards
            )
        
            bot.register_next_step_handler(message, check_answer_programming, chat_id, data, list_nub, random_number)
    elif len(list_nub) == 0:
        bot.send_message(message.chat.id,f'Вопросы кончились☹️', reply_markup=keyboards_create(['Главное меню🔙']))
@bot.message_handler(func=lambda message: True)
def check_answer_programming(message, chat_id, data, list_nub, random_number):
    try:
        answer = int(message.text)
        current_question = data[0]

        correct_option = current_question[chat_id]['otvet']
        if answer == correct_option:
            bot.send_message(chat_id, 'Верно, вы получили 10 баллов за этот вопрос! Следующий вопрос:')
            list_nub.remove(random_number)
            send_question_programming(message)
            db.score(chat_id)
            print(list_nub)
        else:
            bot.send_message(chat_id, 'Неверно. Следующий вопрос:')
            list_nub.remove(random_number)
            send_question_programming(message)
            print(list_nub)
    except ValueError:
        bot.send_message(chat_id, 'Пожалуйста, введите номер ответа')
        send_question_programming(message)
    

@bot.message_handler(func = lambda m : m.text == 'Главное меню🔙')
def back(message):
    welcome_message(message)

if __name__ == '__main__':
    db = database.Database()
    bot.polling()