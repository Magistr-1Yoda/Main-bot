import telebot
import sqlite3
from telebot import types

# Инициализация бота
token = '6279309417:AAEs9jKOp18I_RYxc41EI2uI31zIV0ZxZcQ'
bot = telebot.TeleBot(token)

# Подключение к базе данных SQLite
conn = sqlite3.connect('viktorina.db')
cursor = conn.cursor()

# Словарь для хранения текущего вопроса и правильного ответа
current_question = {}


# Функция начала викторины
@bot.message_handler(commands=['start', 'quiz'])
def start_quiz(message):
    send_question(message.chat.id)


# Функция отправки вопроса
def send_question(chat_id):
    conn = sqlite3.connect('viktorina.db')
    cursor = conn.cursor()

    # Получение случайного вопроса
    cursor.execute('SELECT * FROM coding ORDER BY RANDOM() LIMIT 1')
    question = cursor.fetchone()

    # Сохранение текущего вопроса и правильного ответа
    current_question[chat_id] = {
        'question': question[1],
        'otvet': question[6]
    }

    # Формирование клавиатуры с вариантами ответов
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(str(i)) for i in range(1, 5)]
    keyboard.add(*buttons)

    # Отправка вопроса с вариантами ответов
    bot.send_message(
        chat_id,
        f'{question[1]}\n1. {question[2]}\n2. {question[3]}\n3. {question[4]}\n4. {question[5]}',
        reply_markup=keyboard
    )


# Функция проверки ответа
@bot.message_handler(func=lambda message: True)
def check_answer(message):
    try:
        answer = int(message.text)
        chat_id = message.chat.id

        # Получение правильного ответа из сохраненных данных
        correct_option = current_question[chat_id]['otvet']

        # Проверка ответа
        if answer == correct_option:
            bot.send_message(chat_id, 'Верно! Следующий вопрос:')
            send_question(chat_id)
        else:
            bot.send_message(chat_id, 'Неверно. Попробуйте еще раз:')
            send_question(chat_id)
    except ValueError:
        bot.send_message(chat_id, 'Пожалуйста, введите номер ответа.')
        send_question(chat_id)


# Запуск бота
if __name__ == '__main__':
    bot.polling()
