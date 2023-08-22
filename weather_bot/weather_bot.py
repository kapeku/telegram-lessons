import telebot
import requests
import json
bot = telebot.TeleBot('6324404412:AAE6meqtZe9jTwu9SZAs6dxAvQcwu7M2wX0')
API = '4d9554dc6bc9cf6358285b63843ef81d'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, рад тебя видеть! Напиши название своего города")

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        msg = '\U00002600' if temp > 20.0 else '\u26C5'
        bot.reply_to(message, f'Сейчас погода: {data["main"]["temp"]}, {msg}')
        image = 'sun.webp' if temp > 20.0 else 'sun_in_cloud.jpg'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, 'Город указан не верно :(')


bot.polling(none_stop=True)