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
    if message.text == "/start":
        bot.send_message(message.from_user.id,
                         "Приветствую вас в моём первом, не самом стандартном калькуляторе, написанном на Python!")
        keyboard = types.InlineKeyboardMarkup()
        key_math = types.InlineKeyboardButton(text='Математические операции', callback_data='math')
        keyboard.add(key_math)
        key_geo = types.InlineKeyboardButton(text='Построение графиков', callback_data='geo')
        keyboard.add(key_geo)

        bot.send_message(message.from_user.id, text='Выберите, что вы хотите делать:', reply_markup=keyboard)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Введите /start")
    else:
        bot.send_message(message.from_user.id, "Некорректное сообщение. Напишите /help.")


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "math":
        msg = "Запишите своё выражение привычным образом с помощью знаков, все операции, которые бот сможет обработать вы увидете далее: сложение: + вычитание: - умножение: * деление: / степени: ** "
        bot.send_message(call.from_user.id, msg)

    # Если выбрали "Обычные математические выражения"
    elif call.data == "usuall":
        bot.send_message(call.from_user.id, "Введите математическое выражение, например 2 + 2 - 2 * 2 / 2 ** 2:")
        bot.register_next_step_handler(call.message, process_expression)


# Обработка введенного математического выражения
def process_expression(message):
    try:
        # Заменяем символ корня на соответствующий формат для sympy
        expression = message.text.replace('√', 'sqrt')

        # Используем sympy для вычисления выражения
        result = sp.sympify(expression)
        bot.send_message(message.from_user.id, f"Результат: {result}")
    except Exception as e:
        bot.send_message(message.from_user.id, "Ошибка в выражении. Пожалуйста, попробуйте еще раз.")


# Запускаем постоянный опрос бота в Телеграме
bot.polling(none_stop=True, interval=0)
