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
        bot.send_message(message.from_user.id, "Чтобы перезапустить работу бота, введите /start")
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
        keyboard.add(key_add)  # Добавляем кнопку в клавиатуру
        key_equation = types.InlineKeyboardButton(text='Обычные уравнения', callback_data='usurav')
        keyboard.add(key_equation)  # Добавляем кнопку в клавиатуру

        # Отправляем сообщение с выбором операций
        bot.send_message(call.from_user.id, msg, reply_markup=keyboard)

    # Если выбрали "Обычные математические выражения"
    elif call.data == "usuall":
        bot.send_message(call.from_user.id, "Здесь вводите выражение любой длины. Можно использовать: сложение (n + n), вычитание (n - n), умножение (n * n), деление (n / n), степени (n ** n), корни (sqrt(n), дроби (n / n). После получения ответа снова выберите 'Обычные математические выражение' либо что-то другое. Если этого не сделать и снова вписать выражение, бот выдаст ошибку.)")
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
