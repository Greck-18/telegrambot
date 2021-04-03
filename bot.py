import asyncio
import datetime
import logging

from config import TOKEN

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters import Text
from sqlighter import SQLighter
from datetime import datetime
from news_by import page_of_news, title_of_news
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold, italic, code, pre
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove

logging.basicConfig(level=logging.INFO)

# инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# создание бд
db = SQLighter('database.bd')
db.create_db()

# кнопки для новостей
repeat_btn = KeyboardButton('Да')
repeat_btn2 = KeyboardButton('Нет')
news_btn1 = InlineKeyboardButton('1', callback_data='btn1')
news_btn2 = InlineKeyboardButton('2', callback_data='btn2')
news_btn3 = InlineKeyboardButton('3', callback_data='btn3')
news_btn4 = InlineKeyboardButton('4', callback_data='btn4')
news_btn5 = InlineKeyboardButton('5', callback_data='btn5')
news_btn6 = InlineKeyboardButton('6', callback_data='btn6')
news_keyboard = InlineKeyboardMarkup().add(news_btn1, news_btn2, news_btn3, news_btn4, news_btn5, news_btn6)
repeat_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(repeat_btn, repeat_btn2)


# колбек функции кнопок с последующим выводом на экран текста
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('btn'))
async def news_process(callback_query: types.CallbackQuery):
    num = callback_query.data[-1]
    if num.isdigit():
        num = int(num)
    count = num
    text = page_of_news(count)
    if num == 1:
        await bot.send_message(callback_query.from_user.id, text, parse_mode="html")
    elif num == 2:
        await bot.send_message(callback_query.from_user.id, text, parse_mode="html")
    elif num == 3:
        await bot.send_message(callback_query.from_user.id, text, parse_mode="html")
    elif num == 4:
        await bot.send_message(callback_query.from_user.id, text, parse_mode="html")
    elif num == 5:
        await bot.send_message(callback_query.from_user.id, text, parse_mode="html")
    elif num == 6:
        await bot.send_message(callback_query.from_user.id, text, parse_mode="html")
    await asyncio.sleep(2)
    await bot.send_message(callback_query.from_user.id, "Хотите ещё почитать новости?", reply_markup=repeat_keyboard)


@dp.message_handler(Text(equals='Да'))
async def repeat_news(message: types.Message):
    await news_by(message)


@dp.message_handler(Text(equals='Нет'))
async def no_repeat(message: types.Message):
    await bot_help(message)


# функция страрт
@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    text = 'Приветствую тебя ,\nодпишись на меня если ещё не подписан , для этого пропиши команду /subscribe'
    await bot.send_message(message.from_user.id, message.text)


# меню бота
@dp.message_handler(commands=['help'])
async def bot_help(message: types.Message):
    await bot.send_message(message.chat.id, "Помощь")


# подписка на бота
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.subscribers_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id)
        await message.answer("Вы успешно <b>подписались</b>!", parse_mode="html")
    elif db.check_status(message.chat.id) == 0:
        db.update_subscriber(message.from_user.id, True)
        await message.answer("Вы опять <b>подписались</b>!", parse_mode="html")
    else:
        db.update_subscriber(message.from_user.id, True)
        await message.answer("Вы уже и так <b>подписаны</b>!", parse_mode="html")


# отписка от бота
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscribers_exists(message.from_user.id):
        await message.answer("Вы и так не <b>подписаны</b>!", parse_mode="html")
    elif db.check_status(message.chat.id) == 0:
        await message.answer("Вы уже итак <b>отписались</b>", parse_mode="html")
    else:
        db.update_subscriber(message.from_user.id, False)
        await message.answer("Вы успешно <b>отписались</b>!", parse_mode='html')


# функция вывода новостей (белорусских)
@dp.message_handler(commands=["news"])
async def news_by(message: types.Message):
    text = title_of_news()
    await message.answer(text)
    await asyncio.sleep(2)
    await message.answer("Какую <strong>новость</strong> хотите прочитать подробнее?", reply_markup=news_keyboard,
                         parse_mode='html')


# @dp.message_handler()
# async def echo(message: types.Message):
#      await bot.send_message(message.from_user.id, message.text)


# функция для непонятного текста
@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(message: types.Message):
    text = "Я не знаю , этой команды , но зато я знаю эту команду /help !)"
    await message.reply(text, parse_mode=ParseMode.MARKDOWN)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
