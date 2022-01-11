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

reply_keyboard = ReplyKeyboardMarkup()
reply_keyboard.add(start_timer_button)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")

if __name__ == '__main__':
    print(PORT)
    executor.start_webhook(
        dp,
        skip_updates=True,
        webhook_path='',
        port=PORT,
        host='localhost'
    )
