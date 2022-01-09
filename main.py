import asyncio
import json
import os

from aiotg import Bot, Chat

bot = Bot(api_token=os.getenv('ROSH_TIMER_BOT_API_TOKEN'))

inline_keyboard_markup = {
    'type': 'InlineKeyboardMarkup',
    'inline_keyboard': [
        [{'type': 'InlineKeyboardButton',
          'text': 'Start timer',
          'callback_data': 'start-timer'}]
    ]
}

@bot.callback(r"start-timer")
async def echo(chat, cq, match):
    await chat.send_text('Timer started')
    await chat.send_text('8-11 min left')
    await asyncio.sleep(300)
    await chat.send_text('3-6 min left')
    await asyncio.sleep(60)
    await chat.send_text('2-5 min left')
    await asyncio.sleep(60)
    await chat.send_text('1-4 min left')
    await asyncio.sleep(60)
    await chat.send_text('Rosh can be up. 3 min left.')
    await asyncio.sleep(60)
    await chat.send_text('Rosh can be up. 2 min left.')
    await asyncio.sleep(60)
    await chat.send_text('Rosh can be up. 1 min left.')
    await asyncio.sleep(60)

    await chat.send_text('Rosh is up!', reply_markup=json.dumps(inline_keyboard_markup))


@bot.default
async def echo(chat, message):
    await chat.send_text(text='Ready to track rosh timer!', reply_markup=json.dumps(inline_keyboard_markup))


if __name__ == '__main__':
    bot.run()
