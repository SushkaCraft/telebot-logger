import telebot
from telebot import types
from datetime import datetime

# Токен вашего бота (замените на ваш реальный токен)
TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)

def log(message):
    # Открываем файл для записи логов с добавлением, параметром 'a' (не удаляет предыдущее содержимое) и кодировкой utf-8
    with open('log.txt', 'a', encoding="utf-8") as log_file:
        # Обрабатываем системные сообщения в виде строк
        if isinstance(message, str):
            msg = f"{datetime.now()}\n{message}\n"
        else:
            # Формируем строку с информацией о пользователе и сообщении
            msg = f"{datetime.now()}\nСообщение от {message.from_user.first_name} {message.from_user.last_name} - {message.from_user.username} (id = {message.from_user.id})\n{message.text}\n"
        # Печатаем сообщение в консоль для отладки
        print(msg)
        # Записываем сообщение в файл
        log_file.write(msg)

# Обработчик команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Нажми меня", callback_data="btn1")
    markup.add(btn1)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку ниже.", reply_markup=markup)
    log(message)
    log("Пользователь авторизовался.")

# Эхо-реакция на любое текстовое сообщение
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    log(message)

# Обработчик нажатий на инлайн-кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "btn1":
        bot.answer_callback_query(call.id, "Кнопка нажата!")
        bot.send_message(call.message.chat.id, "Вы нажали кнопку!")
        log(f"Обработано нажатие кнопки пользователем {call.from_user.first_name} {call.from_user.last_name} - {call.from_user.username} (id = {call.from_user.id})")

# Запуск бота
bot.polling()
