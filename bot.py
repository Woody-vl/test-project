import os
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Set up OpenAI and Telegram credentials from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not OPENAI_API_KEY or not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("OPENAI_API_KEY and TELEGRAM_BOT_TOKEN must be set as environment variables")

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def handle_message(message: types.Message):
    """Forward the user's message to OpenAI and return the response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}],
        )
        reply_text = response["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        reply_text = f"Error communicating with OpenAI API: {exc}"
    await message.reply(reply_text)

if __name__ == "__main__":
    executor.start_polling(dp)
