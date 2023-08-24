import telebot
from currency_converter import CurrencyConverter
from telebot import types

currency = CurrencyConverter()
bot = telebot.TeleBot('6324404412:AAE6meqtZe9jTwu9SZAs6dxAvQcwu7M2wX0')
amount=0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат, впишите сумму')
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data= 'usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть больше 0, впишите сумму заново')
        bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call: call.data == 'да' or call.data == 'нет' )
def another_summ(call):
    if call.data == 'да':
        bot.send_message(call.message.chat.id, 'Введите новую сумму')
        bot.register_next_step_handler(call.message, summa)
    if call.data == 'нет':
        bot.send_message(call.message.chat.id, 'Хорошо. Если захотите продолжить, нажмите да')

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        markup2 = types.InlineKeyboardMarkup(row_width=2)
        btn5 = types.InlineKeyboardButton('ДА', callback_data='да')
        btn6 = types.InlineKeyboardButton('НЕТ', callback_data='нет')
        markup2.add(btn5, btn6)
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Хотите конвертировать еще одно значение?', reply_markup=markup2)

    else:
        bot.send_message(call.message.chat.id, 'Введите пару значение через "/"')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('ДА', callback_data='да')
        btn2 = types.InlineKeyboardButton('НЕТ', callback_data='нет')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}. Хотите конвертировать еще одно значение?', reply_markup=markup)
    except Exception:
        bot.send_message(message.chat.id, f'Что-то не так. Впишите значение заново')
        bot.register_next_step_handler(message, my_currency)

bot.polling(none_stop=True)