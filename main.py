from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo


bot = Bot('6324404412:AAE6meqtZe9jTwu9SZAs6dxAvQcwu7M2wX0')
dp = Dispatcher(bot)

@dp.message_handler(commands = ['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Открыть веб-страницу', web_app=WebAppInfo(url='https://kapeku.github.io/web-tg/')))
    await message.answer('Привет, мой друг!', reply_markup = markup)

executor.start_polling(dp)