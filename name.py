import telebot
from tokeeen import mytokeen
import sympy as sp  # Импортируем библиотеку sympy для вычисления математических выражений

# Подключаем модуль для Телеграма
bot = telebot.TeleBot(mytokeen)

# Импортируем типы из модуля, чтобы создавать кнопки
from telebot import types

# Метод, который получает сообщения и обрабатывает их
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # Если написали «Привет»
    if message.text == "/start":
        # Пишем приветствие
        bot.send_message(message.from_user.id,
                         "Приветствую вас в моём первом, не самом стандартном калькуляторе, написанном на Python!")
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()
        # Кнопка для математических операций
        key_math = types.InlineKeyboardButton(text='Математические операции', callback_data='math')
        keyboard.add(key_math)
        # Кнопка для построения графиков
        key_geo = types.InlineKeyboardButton(text='Построение графиков', callback_data='geo')
        keyboard.add(key_geo)

        # Показываем все кнопки сразу и пишем сообщение о выборе
        bot.send_message(message.from_user.id, text='Выберите, что вы хотите делать:', reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Введите /start")
    else:
        bot.send_message(message.from_user.id, "Некорректное сообщение. Напишите /help.")

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # Если нажали на кнопку "математические операции"
    if call.data == "math":
        msg = "Выберите математическую операцию:"
        keyboard = types.InlineKeyboardMarkup()
        key_add = types.InlineKeyboardButton(text='Обычные математические выражения', callback_data='usuall')
        key_equation = types.InlineKeyboardButton(text='Уравнения', callback_data='urav')
        key_vieta = types.InlineKeyboardButton(text='Квадратные уравнения (т. Виета)', callback_data='kv_urav')
        key_system = types.InlineKeyboardButton(text='Система уравнений', callback_data='sys_urav')
        keyboard.add(key_add)
        keyboard.add(key_equation)
        keyboard.add(key_vieta)
        keyboard.add(key_system)

        # Отправляем сообщение с выбором операций
        bot.send_message(call.from_user.id, msg, reply_markup=keyboard)

    # Если выбрали "Обычные математические выражения"
    elif call.data == "usuall":
        bot.send_message(call.from_user.id, "Введите математическое выражение (например, 2 + 2):")
        bot.register_next_step_handler(call.message, process_expression)

# Обработка введенного математического выражения
def process_expression(message):
    try:
        # Используем sympy для вычисления выражения
        result = sp.sympify(message.text)
        bot.send_message(message.from_user.id, f"Результат: {result}")
    except Exception as e:
        bot.send_message(message.from_user.id, "Ошибка в выражении. Пожалуйста, попробуйте еще раз.")

# Запускаем постоянный опрос бота в Телеграме
bot.polling(none_stop=True, interval=0)
