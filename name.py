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
    if message.text == "ОЛЕГ":
        # Пишем приветствие
        bot.send_message(message.from_user.id, "Привет, сейчас я покажу тебе мой католог.")
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()
        # По очереди готовим текст и обработчик для каждого знака зодиака
        key_oven = types.InlineKeyboardButton(text='ТРЕУГОЛЬНИК', callback_data='zodiac')
        # И добавляем кнопку на экран
        keyboard.add(key_oven)
        key_telec = types.InlineKeyboardButton(text='ПРЯМОУГОЛЬНИК И КВАДРАТ', callback_data='zodiac')
        keyboard.add(key_telec)
        key_bliznecy = types.InlineKeyboardButton(text='ОКРУЖНОСТЬ', callback_data='zodiac')
        keyboard.add(key_bliznecy)
        key_rak = types.InlineKeyboardButton(text='ПРЯМАЯ', callback_data='zodiac')
        keyboard.add(key_rak)
        key_lev = types.InlineKeyboardButton(text='УГОЛ', callback_data='zodiac')
        keyboard.add(key_lev)

        # Показываем все кнопки сразу и пишем сообщение о выборе
        bot.send_message(message.from_user.id, text='Выбери свой знак зодиака', reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши ОЛЕГ")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # Если нажали на одну из 12 кнопок — выводим гороскоп
    if call.data == "zodiac":
        msg = "ОЛЕГеометрия"
        bot.send_message(call.message.chat.id, msg)
    # Запускаем постоянный опрос бота в Телеграме


bot.polling(none_stop=True, interval=0)