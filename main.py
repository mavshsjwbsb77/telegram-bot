from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import Message
import asyncio
from flask import Flask
from threading import Thread
import os

API_TOKEN = '8470735691:AAEXDGQ6Fi_abvRxpp52Plld38Gshc15GSw'
ADMIN_ID = 7078757412  # ضع معرفك الصحيح

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def handle_message(message: Message):
    await bot.send_message(ADMIN_ID, f"📩 رسالة من {message.from_user.full_name}:\n{message.text}")
    reply = await message.reply("✅ تم إرسال رسالتك إلى المدير. سيتم حذفها بعد دقيقتين.")
    await asyncio.sleep(120)
    try:
        await message.delete()
        await reply.delete()
    except:
        pass

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ البوت يعمل الآن"

def run_web():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

def start_web():
    thread = Thread(target=run_web)
    thread.start()

if __name__ == '__main__':
    start_web()
    executor.start_polling(dp, skip_updates=True)
