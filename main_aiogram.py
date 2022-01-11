import asyncio
import json
import os

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.getenv('ROSH_TIMER_BOT_API_TOKEN')
PORT = int(os.environ.get('PORT', 80))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

start_timer_button = KeyboardButton('Start timer')
stop_timer_button = KeyboardButton('Stop timer')

reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
reply_keyboard.add(start_timer_button)
reply_keyboard.add(stop_timer_button)

timers_running = {}

phrases_delays = [
    ('8-11 min left', 300),
    ('3-6 min left', 60),
    ('2-5 min left', 60),
    ('1-4 min left', 60),
    ('Rosh can be up. 3 min left', 60),
    ('Rosh can be up. 2 min left', 60),
    ('Rosh can be up. 1 min left', 60),
]


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer('Ready to track rosh timer!', reply_markup=reply_keyboard)


@dp.message_handler(regexp="Stop timer")
async def stop_timer(message: types.Message):
    task = timers_running.get(message.chat.id)
    if task:
        task.cancel()
        await message.answer('Timer stopped', reply_markup=reply_keyboard)
        timers_running[message.chat.id] = None
        return
    await message.answer('Timer not running', reply_markup=reply_keyboard)


async def timer_task(message):
    await message.answer('Timer started')
    for phraze, delay in phrases_delays:
        if timers_running[message.chat.id]:
            await message.answer(phraze)
            await asyncio.sleep(delay)
        else:
            return
    await message.answer('Rosh is up!', reply_markup=reply_keyboard)


@dp.message_handler(regexp="Start timer")
async def run_timer(message: types.Message):
    if timers_running.get(message.chat.id):
        # await message.answer('Timer already running')
        return
    task = asyncio.create_task(timer_task(message))
    timers_running[message.chat.id] = task

    await task
    timers_running[message.chat.id] = None


@dp.message_handler()
async def default_message(message: types.Message):
    await message.answer('Ready to track rosh timer!', reply_markup=reply_keyboard)

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)

    # executor.start_webhook(
    #     dispatcher=dp,
    #     skip_updates=True,
    #     webhook_path='',
    #     port=PORT,
    #     host='0.0.0.0'
    # )
