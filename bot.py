import asyncio
import datetime
import logging

from config import TOKEN

from aiogram import Bot, Dispatcher, types, executor
from sqlighter import SQLighter
from datetime import datetime

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)

dp = Dispatcher(bot)
db = SQLighter('database.db')


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    text = 'Приветствую тебя ,\nподпишись на меня если ещё не подписан , для этого пропиши команду \subscribe'
    await bot.send_message(message.chat.id, text)


@dp.message_handler(commands=['help'])
async def bot_help(message: types.Message):
    await bot.send_message(message.chat.id, "Помощь")


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.subscribers_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscriber(message.from_user.id, True)

    await message.answer("Вы успешно подписались!")


@dp.message_handler(command=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscribers_exists(message.from_user.id):
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы и так не подписаны!")
    else:
        db.update_subscriber(message.from_user, False)
        await message.answer("Вы успешно отписались!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
