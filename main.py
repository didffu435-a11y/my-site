import os
import logging
import asyncio
import random
from datetime import datetime, timedelta
from threading import Thread
from flask import Flask, render_template, jsonify
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

BOT_TOKEN = "8997716327:AAHlY2OEIYJ_E_oisD8D7yK9LirE0Yo2e_w"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

KEYWORDS = ["важно", "срочно", "помощь", "купить", "python"]

# --- МАРШРУТЫ FLASK ---

@app.route('/')
def home():
    return render_template('my_file.html')

# Добавляем API-путь, который запрашивает ваш HTML-файл для постройки графиков
@app.route('/api/history/<username>')
def get_history(username):
    # Генерируем случайную красивую статистику для демонстрации на графике
    mock_data = []
    base_subscribers = random.randint(1000, 5000)
    now = datetime.now()
    
    for i in range(10):
        time_label = (now - timedelta(minutes=10-i)).strftime("%Y-%m-%d %H:%M:%S")
        base_subscribers += random.randint(-15, 30)
        mock_data.append({
            "date": time_label,
            "subscribers": base_subscribers
        })
    return jsonify(mock_data)

# --- ЛОГИКА TELEGRAM-БОТА ---

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("Бот-трекер запущен. Я фиксирую сообщения в доступных мне чатах.")

@dp.message()
async def track_messages(message: Message):
    text = message.text or ""
    user = message.from_user.full_name if message.from_user else "Аноним"
    username = f"@{message.from_user.username}" if message.from_user.username else "нет юзернейма"
    chat_name = message.chat.title if message.chat.title else "Личный чат"
    
    log_entry = f"[{chat_name}] {user} ({username}): {text}\n"
    print(log_entry, end="")
    
    with open("messages_log.txt", "a", encoding="utf-8") as file:
        file.write(log_entry)
        
    for word in KEYWORDS:
        if word in text.lower():
            await message.reply(f"🔔 Обнаружено ключевое слово: {word}", parse_mode="Markdown")
            break

async def run_bot():
    print("Бот начал отслеживание сообщений...")
    await dp.start_polling(bot)

def start_bot_in_background():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

bot_thread = Thread(target=start_bot_in_background, daemon=True)
bot_thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
