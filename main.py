import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from ai_handler import query_ai

API_TOKEN = '7752843434:AAEBQX2wx9tC2wO6cIuOr5e2ZtyyaFPdoM4'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    website_button = InlineKeyboardButton(text="Перейти на сайт", url="https://vladtichonenko.github.io/safe1/")
    chat_button = InlineKeyboardButton(text="Начать чат с ИИ", callback_data="start_chat")
    keyboard.add(website_button, chat_button)

    welcome_text = (
        "👋 Привет! Я ваш виртуальный финансовый помощник, готовый помочь вам "
        "в вопросах управления финансами и бухгалтерией. 🏦\n\n"
        "Наш проект предназначен для того, чтобы сделать финансовое планирование "
        "и управление более простым и доступным. Мы понимаем, что финансовые решения "
        "могут быть сложными и требовательными, поэтому мы здесь, чтобы поддержать вас "
        "на каждом этапе пути. 📈💡\n\n"
        "От повседневного бухгалтерского учета до стратегического финансового планирования, "
        "наш ИИ готов предоставить вам советы, ответить на ваши вопросы и предложить решения, "
        "основанные на лучших практиках отрасли. 🌟\n\n"
        "Отправьте мне сообщение, и давайте начнем улучшать ваше финансовое будущее вместе!"
    )

    await message.reply(welcome_text, reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'start_chat')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Начнем чат! Отправь мне сообщение.")

@dp.message_handler(content_types=['text'])
async def handle_message(message: types.Message):
    user_message = message.text
    progress_message = await message.reply("Обрабатываю ваш запрос...")

    # Отправка прогресс-бара
    for i in range(1, 11):
        await asyncio.sleep(2)
        await progress_message.edit_text(f"Обрабатываю ваш запрос... {i * 10}%")

    ai_response = query_ai(user_message)

    if 'Ошибка' in ai_response:
        await message.reply("Извините, я очень устал, мне надо отдохнуть 😓")
    else:
        await message.reply(ai_response)

@dp.message_handler(content_types=['document'])
async def handle_file(message: types.Message):
    file_info = await bot.get_file(message.document.file_id)
    file_path = file_info.file_path
    file = await bot.download_file(file_path)
    progress_message = await message.reply("Обрабатываю ваш файл...")

    # Отправка прогресс-бара
    for i in range(1, 11):
        await asyncio.sleep(2)
        await progress_message.edit_text(f"Обрабатываю ваш файл... {i * 10}%")

    ai_response = query_ai('Обработай этот файл')
    if 'Ошибка' in ai_response:
        await message.reply("Извините, я очень устал, мне надо отдохнуть 😓")
    else:
        await message.reply(ai_response)

if __name__ == '__main__':
    from aiogram.utils.executor import start_polling
    start_polling(dp, skip_updates=True)
