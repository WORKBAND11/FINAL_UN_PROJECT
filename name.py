import telebot
from tokeeen import mytokeen
import sympy as sp
import matplotlib

matplotlib.use('Agg')  # Устанавливаем бэкенд для работы без GUI
import matplotlib.pyplot as plt
import numpy as np

bot = telebot.TeleBot(mytokeen)
from telebot import types


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
        bot.send_message(message.from_user.id,
                         "Чтобы перезапустить работу бота, введите /start. Пишите всё строго по инструкции.")
    else:
        bot.send_message(message.from_user.id, "Некорректное сообщение. Напишите /help.")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "math":
        msg = "Выберите математическую операцию:"
        keyboard = types.InlineKeyboardMarkup()
        key_add = types.InlineKeyboardButton(text='Обычные математические выражения', callback_data='usuall')
        keyboard.add(key_add)
        key_equation = types.InlineKeyboardButton(text='Обычные уравнения', callback_data='usurav')
        keyboard.add(key_equation)
        bot.send_message(call.from_user.id, msg, reply_markup=keyboard)

    elif call.data == "geo":
        msg = "📊 Выберите тип графика:"
        keyboard = types.InlineKeyboardMarkup()
        key_linear = types.InlineKeyboardButton(text='Линейный (y = kx + b)', callback_data='linear_graph')
        keyboard.add(key_linear)
        key_quadratic = types.InlineKeyboardButton(text='Квадратичный (y = ax² + bx + c)',
                                                   callback_data='quadratic_graph')
        keyboard.add(key_quadratic)
        bot.send_message(call.from_user.id, msg, reply_markup=keyboard)

    elif call.data == "usuall":
        bot.send_message(call.from_user.id, "Введите математическое выражение...")
        bot.register_next_step_handler(call.message, process_expression)

    elif call.data == "usurav":
        bot.send_message(call.from_user.id, "Введите уравнение в формате '2*x + 2 = 4'...")
        bot.register_next_step_handler(call.message, process_equation)

    elif call.data == "linear_graph":
        bot.send_message(call.from_user.id, "Введите коэффициенты k и b через пробел (пример: '2 3'):")
        bot.register_next_step_handler(call.message, process_linear_graph)

    elif call.data == "quadratic_graph":
        bot.send_message(call.from_user.id, "Введите коэффициенты a, b, c через пробел (пример: '1 -2 1'):")
        bot.register_next_step_handler(call.message, process_quadratic_graph)


def process_expression(message):
    try:
        result = sp.sympify(message.text)
        bot.send_message(message.from_user.id, f"Результат: {result}")
    except Exception as e:
        bot.send_message(message.from_user.id, "Ошибка в вводе выражения.")


def process_equation(message):
    try:
        equation_text = message.text.replace(" ", "")
        if '=' not in equation_text:
            raise ValueError("Отсутствует знак '='.")
        left, right = equation_text.split('=')
        equation = sp.Eq(sp.sympify(left), sp.sympify(right))
        solution = sp.solve(equation)
        bot.send_message(message.from_user.id, f"Решение: x = {solution}")
    except Exception as e:
        bot.send_message(message.from_user.id, "Ошибка в вводе уравнения.")
def process_linear_graph(message):
    try:
        k, b = map(float, message.text.split())
        x = np.linspace(-10, 10, 400)
        y = k * x + b

        plt.figure()
        plt.plot(x, y, label=f'y = {k}x + {b}')
        plt.title("Линейный график")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.legend()

        plt.savefig('graph.png')
        plt.close()

        with open('graph.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка: Убедитесь, что вы ввели два числа через пробел.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}. Попробуйте снова.")


def process_quadratic_graph(message):
    try:
        # Разделяем входное сообщение на коэффициенты a, b и c
        a, b, c = map(float, message.text.split())
        x = np.linspace(-10, 10, 400)
        y = a * x ** 2 + b * x + c

        plt.figure()
        plt.plot(x, y, label=f'y = {a}x² + {b}x + {c}')
        plt.title("Квадратичный график")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.legend()

        plt.savefig('graph.png')
        plt.close()

        with open('graph.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка: Убедитесь, что вы ввели три числа через пробел.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}. Попробуйте снова.")


bot.polling(none_stop=True, interval=0)
