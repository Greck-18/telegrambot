import asyncio
import datetime
import logging

from config import TOKEN

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.message import ContentType
from sqlighter import SQLighter
from datetime import datetime

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)

dp = Dispatcher(bot)
db = SQLighter('database.bd')

db.create_db()


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    text = 'Приветствую тебя ,\nподпишись на меня если ещё не подписан , для этого пропиши команду /subscribe'
    await bot.send_message(message.chat.id, text)


@dp.message_handler(commands=['help'])
async def bot_help(message: types.Message):
    await bot.send_message(message.chat.id, "Помощь")


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.subscribers_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id)
        await message.answer("Вы успешно подписались!")
    elif db.check_status(message.chat.id) == 0:
        db.update_subscriber(message.from_user.id, True)
        await message.answer("Вы опять подписались!")
    else:
        db.update_subscriber(message.from_user.id, True)
        await message.answer("Вы уже и так подписаны!")


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscribers_exists(message.from_user.id):
        await message.answer("Вы и так не подписаны!")
    elif db.check_status(message.chat.id) == 0:
        await message.answer("Вы уже итак отписались")
    else:
        db.update_subscriber(message.from_user.id, False)
        await message.answer("Вы успешно отписались!")


@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(message: types.Message):
    text = "Я не знаю , этой команды , но зато я знаю эту команду /help !)"
    await message.reply(text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
