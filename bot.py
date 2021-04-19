import asyncio
import logging
import aioschedule

from config import TOKEN

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.message import ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove, ParseMode
from news import NewsBy, FootBallNews
from sqlighter import SQLighter
from states import Test
from weather import Weather

logging.basicConfig(level=logging.INFO)

# инициализация бота
news_by = NewsBy()
football_news = FootBallNews()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
football_news.get_data()
football_news.process_data()
news_by.get_data()
news_by.process_data()
# создание бд
db = SQLighter('database.bd')
db.create_db()

# кнопки для новостей
news_btn1 = InlineKeyboardButton('1', callback_data='btn1')
news_btn2 = InlineKeyboardButton('2', callback_data='btn2')
news_btn3 = InlineKeyboardButton('3', callback_data='btn3')
news_btn4 = InlineKeyboardButton('4', callback_data='btn4')
news_btn5 = InlineKeyboardButton('5', callback_data='btn5')
news_btn6 = InlineKeyboardButton('6', callback_data='btn6')
news_keyboard = InlineKeyboardMarkup().add(news_btn1, news_btn2, news_btn3, news_btn4, news_btn5, news_btn6)

# кнопки для новостей про футбол
sport_btn1 = InlineKeyboardButton('🇫🇷', callback_data='sport1')
sport_btn2 = InlineKeyboardButton('🇩🇪', callback_data='sport2')
sport_btn3 = InlineKeyboardButton('🇵🇹', callback_data='sport3')
sport_btn4 = InlineKeyboardButton('🇳🇱', callback_data='sport4')
sport_btn5 = InlineKeyboardButton('🇧🇪', callback_data='sport5')
sport_btn6 = InlineKeyboardButton('🇦🇹', callback_data='sport6')
sport_btn7 = InlineKeyboardButton('🏴󠁧󠁢󠁳󠁣󠁴󠁿', callback_data='sport7')
sport_btn8 = InlineKeyboardButton('🇺🇦', callback_data='sport8')
sport_btn9 = InlineKeyboardButton('🏴󠁧󠁢󠁥󠁮󠁧󠁿', callback_data='sport9')
sport_btn10 = InlineKeyboardButton('🇪🇸', callback_data='sport10')
sport_btn11 = InlineKeyboardButton('🇷🇺', callback_data='sport11')
sport_btn12 = InlineKeyboardButton('🇮🇹', callback_data='sport12')
sport_keyboard = InlineKeyboardMarkup().add(sport_btn1, sport_btn2, sport_btn3, sport_btn4, sport_btn5, sport_btn6,
                                            sport_btn7,
                                            sport_btn8, sport_btn9, sport_btn10, sport_btn11, sport_btn12)


# колбек функции кнопок с последующим выводом на экран текста
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('btn'))
async def news_process(callback_query: types.CallbackQuery, state=None):
    num = callback_query.data[-1]
    if num.isdigit():
        num = int(num)
    count = num
    if num == 1:
        await bot.send_message(callback_query.from_user.id, news_by.get_news(count), parse_mode="html")
    elif num == 2:
        await bot.send_message(callback_query.from_user.id, news_by.get_news(count), parse_mode="html")
    elif num == 3:
        await bot.send_message(callback_query.from_user.id, news_by.get_news(count), parse_mode="html")
    elif num == 4:
        await bot.send_message(callback_query.from_user.id, news_by.get_news(count), parse_mode="html")
    elif num == 5:
        await bot.send_message(callback_query.from_user.id, news_by.get_news(count), parse_mode="html")
    elif num == 6:
        await bot.send_message(callback_query.from_user.id, news_by.get_news(count), parse_mode="html")
    await asyncio.sleep(2)
    repeat_btn = KeyboardButton("Да", callback_data="Yes")
    repeat_btn2 = KeyboardButton('Нет', callback_data="No")
    repeat_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(repeat_btn, repeat_btn2)
    await bot.send_message(callback_query.from_user.id, "Хотите ещё почитать новости?", reply_markup=repeat_keyboard)
    await Test.Q2.set()


# функция страрт
@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    text = 'Приветствую тебя ,\nодпишись на меня если ещё не подписан , для этого пропиши команду /subscribe'
    await bot.send_message(message.from_user.id, text)


# меню бота
@dp.message_handler(commands=['help'])
async def bot_help(message: types.Message):
    await bot.send_message(message.chat.id, f"Помощь, твой id {message.from_user.id}")


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


# получение города для погоды
@dp.message_handler(Command("weather"), state=None)
async def give_weather(message: types.Message):
    await message.answer("Введите город в котром хотитите узнать погоду: ")
    """Какой-то код"""
    await Test.Q1.set()


# машина состояний для белорусских новостей
@dp.message_handler(state=Test.Q1)
async def answer_weather(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data({"answer1": answer})
    data = await state.get_data()
    city = data.get("answer1")
    weather = Weather(city)
    await message.answer(weather.get_weather(), parse_mode="html")
    await state.finish()


# функция вывода новостей (белорусских)
@dp.message_handler(commands=["news"], state=None)
async def bel_news(message: types.Message):
    await message.answer(news_by.get_title())
    await asyncio.sleep(2)
    await message.answer("Какую <strong>новость</strong> хотите прочитать подробнее?", reply_markup=news_keyboard,
                         parse_mode='html')


# машина состояния для погоды
@dp.message_handler(state=Test.Q2)
async def answer_weather(message: types.Message, state: FSMContext):
    answer1 = message.text
    await state.update_data({"answer2": answer1})
    data = await state.get_data()
    repeat = data.get("answer2")
    if repeat.lower() in "да":
        await bel_news(message)
    elif repeat.lower() in 'нет':
        await bot_help(message)
    else:
        await unknown_message(message)
    await state.finish()


@dp.message_handler(commands=['football'], state=None)
async def sport_news(message: types.Message):
    await bot.send_message(message.chat.id,
                           "Здесь новости про мировой футбол , нажмите на лигу, новости которой хотите прочитать",
                           reply_markup=sport_keyboard)
    await message.answer(football_news.get_news(12))


# функция для непонятного текста
@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(message: types.Message):
    text = "Я не знаю , этой команды , но зато я знаю эту команду /help !)"
    await message.reply(text, parse_mode=ParseMode.MARKDOWN)


# функция , отправляющая админу приветствующее сообщение
async def clock_for_admin():
    text = "Доброе утро ,<strong> мой господин</strong> . Желаю вам хорошего дня!"
    await bot.send_message(800847160, text, parse_mode='html')
    await asyncio.sleep(1)
    text = "<strong>Погода:</strong>\n"
    weather = Weather("Минск")
    await bot.send_message(800847160, text + weather.get_weather(), parse_mode='html')


# дополнение к приветсвию админа
async def scheduled():
    aioschedule.every().day.at("09:30").do(clock_for_admin)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


# дополнение к приветствию админа
async def on_startup(x):
    asyncio.create_task(scheduled())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
