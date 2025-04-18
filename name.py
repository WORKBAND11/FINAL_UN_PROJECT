import telebot
from tokeeen import mytokeen
# Подключаем модуль для Телеграма
# Указываем токен
bot = telebot.TeleBot(mytokeen)
# Импортируем типы из модуля, чтобы создавать кнопки
from telebot import types
# Заготовки для трёх предложений

# Метод, который получает сообщения и обрабатывает их
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # Если написали «Привет»
    if message.text == "/start":
        # Пишем приветствие
        bot.send_message(message.from_user.id, "Приветствую вас в моём первом, не самом стандартном калькуляторе, написанном на Python!")
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()
        # По очереди готовим текст и обработчик для каждого знака зодиака
        key_oven = types.InlineKeyboardButton(text='Математические операции', callback_data='zodiac')
        # И добавляем кнопку на экран
        keyboard.add(key_oven)
        key_telec = types.InlineKeyboardButton(text='Построение графиков', callback_data='zodiac')
        keyboard.add(key_telec)

        # Показываем все кнопки сразу и пишем сообщение о выборе
        bot.send_message(message.from_user.id, text='Выберите, что вы хотите делать:', reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Введите /start")
    else:
        bot.send_message(message.from_user.id, "Некоректное сообщение. Напишите /help.")
# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # Если нажали на одну из 12 кнопок — выводим гороскоп
    if call.data == "zodiac":
        msg = "ОЛЕГеометрия"
        bot.send_message(call.message.chat.id, msg)
    # Запускаем постоянный опрос бота в Телеграме


bot.polling(none_stop=True, interval=0)
