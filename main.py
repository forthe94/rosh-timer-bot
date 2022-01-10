import asyncio
import json
import os

from aiotg import Bot, Chat

bot = Bot(api_token=os.getenv('ROSH_TIMER_BOT_API_TOKEN'))
timers_running = {}
inline_keyboard_markup = {
    'type': 'InlineKeyboardMarkup',
    'inline_keyboard': [
        [{'type': 'InlineKeyboardButton',
          'text': 'Start timer',
          'callback_data': 'start-timer'}],
        [{'type': 'InlineKeyboardButton',
          'text': 'Stop timer',
          'callback_data': 'stop-timer'}]
    ]
}
phrases_delays = [
    ('8-11 min left', 300),
    ('3-6 min left', 60),
    ('2-5 min left', 60),
    ('1-4 min left', 60),
    ('Rosh can be up. 3 min left', 60),
    ('Rosh can be up. 2 min left', 60),
    ('Rosh can be up. 1 min left', 60),
]


@bot.callback(r"stop-timer")
async def stop_timer(chat, cq, match):
    task = timers_running.get(chat.id)
    if task:
        task.cancel()
        await chat.send_text('Timer stopped', reply_markup=json.dumps(inline_keyboard_markup))
        timers_running[chat.id] = None
        return 
    await chat.send_text('Timer not running', reply_markup=json.dumps(inline_keyboard_markup))


async def timer_task(chat):
    await chat.send_text('Timer started')
    for phraze, delay in phrases_delays:
        if timers_running[chat.id]:
            await chat.send_text(phraze)
            await asyncio.sleep(delay)
        else:
            return
    await chat.send_text('Rosh is up!', reply_markup=json.dumps(inline_keyboard_markup))


@bot.callback(r"start-timer")
async def run_timer(chat, cq, match):
    if timers_running.get(chat.id):
        chat.send_text('Timer already running')
        return
    task = asyncio.create_task(timer_task(chat))
    timers_running[chat.id] = task

    await task
    timers_running[chat.id] = None

@bot.default
async def echo(chat, message):
    await chat.send_text(text='Ready to track rosh timer!', reply_markup=json.dumps(inline_keyboard_markup))


if __name__ == '__main__':
    bot.run()
