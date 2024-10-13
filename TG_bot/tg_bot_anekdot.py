import random
import requests
from bs4 import BeautifulSoup
import asyncio
import logging
from _key import TOKEN
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Звичайна клавіатура (без callback_data)
# kb = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text='Новий анекдот')],
#     # [KeyboardButton(text='Ліво'), KeyboardButton(text='Кинути кості 🎲')]
#     [KeyboardButton(text='Ліво'), KeyboardButton(text='Кинути')]
# ],
# resize_keyboard=True,
# input_field_placeholder='Натисніть на кнопку')

kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Анекдот'),
    KeyboardButton(text='Dice 🎲')]
],
resize_keyboard=True,
input_field_placeholder='Натисніть на кнопки')

url = 'https://etnosvit.com/uk/anekdoty_uk.html'
def parser(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    anekdots = soup.find_all('div', class_='sue-panel-content sue-content-wrap')
    return [c.text for c in anekdots]
list_jokes = parser(url)
# print(list_jokes)

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Привіт {message.from_user.first_name}!\n',
                        reply_markup=kb)

@dp.message(F.text == 'Анекдот')
async def send_joke(message: Message):
    joke = random.choice(list_jokes)
    await message.answer(joke)

@dp.message(F.text == 'Dice 🎲')
async def dice(message: Message):
    await bot.send_dice(message.chat.id)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')
