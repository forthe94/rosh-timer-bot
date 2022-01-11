import asyncio
import dataclasses
import time
import datetime
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
    ('3-6 min left', 360),
    ('2-5 min left', 420),
    ('1-4 min left', 480),
    ('Rosh can be up. 3 min left', 540),
    ('Rosh can be up. 2 min left', 600),
    ('Rosh can be up. 1 min left', 660),
    ('Rosh up!', 700)
]


@dataclasses.dataclass
class RoshTimer:
    time_started: time.time
    next_time: time.time
    chat_id: int
    cur_step: int = 0

    async def process_cur_step(self):
        await bot.send_message(chat_id=self.chat_id, text=phrases_delays[self.cur_step][0])
        self.next_time = self.time_started + phrases_delays[self.cur_step][1]
        self.cur_step += 1

    def time_left(self):
        time_in_sec = time.time() - self.time_started
        if time_in_sec < 480:
            tdelta = int(480 - time_in_sec)
            return str(datetime.timedelta(seconds=tdelta)) + ' to ' + str(datetime.timedelta(seconds=tdelta + 180))
        else:
            tdelta = int(660 - time_in_sec)
            return str(datetime.timedelta(seconds=tdelta))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer('Ready to track rosh timer!', reply_markup=reply_keyboard)


@dp.message_handler(regexp="Stop timer")
async def stop_timer(message: types.Message):
    timer = timers_running.get(message.chat.id)
    if timer:
        del timers_running[message.chat.id]
        await message.answer('Timer stopped', reply_markup=reply_keyboard)
        return
    await message.answer('Timer not running', reply_markup=reply_keyboard)


@dp.message_handler(regexp="Start timer")
async def run_timer(message: types.Message):
    if timers_running.get(message.chat.id):
        await message.answer(f'Time left {timers_running[message.chat.id].time_left()}')
        return
    rosh_timer = RoshTimer(
        time_started=time.time(),
        next_time=time.time(),
        chat_id=message.chat.id,
    )
    timers_running[rosh_timer.chat_id] = rosh_timer
    await message.answer('Timer started')


@dp.message_handler()
async def default_message(message: types.Message):
    await message.answer('Ready to track rosh timer!', reply_markup=reply_keyboard)


async def timers_checker():
    while True:
        to_delete = []
        for chat_id, rosh_timer in timers_running.items():
            if time.time() >= rosh_timer.next_time:
                await rosh_timer.process_cur_step()
                if rosh_timer.cur_step == len(phrases_delays):
                    to_delete.append(rosh_timer.chat_id)
        for chat_id in to_delete:
            del timers_running[chat_id]
        await asyncio.sleep(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(timers_checker())
    # executor.start_polling(dispatcher=dp, loop=loop)

    executor.start_webhook(
        dispatcher=dp,
        skip_updates=True,
        webhook_path='',
        port=PORT,
        host='0.0.0.0'
    )
