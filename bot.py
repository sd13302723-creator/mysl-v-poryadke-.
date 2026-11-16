from flask import Flask
import os
import threading
import telebot # или ваш импорт бота

# Инициализация Flask для веб-сервера (чтобы Render не засыпал)
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Запускаем Flask в фоновом потоке
threading.Thread(target=run_flask).start()

# --- СЮДА НИЖЕ ВСТАВЬТЕ ВЕСЬ ВАШ КОД БОТА ---
TOKEN = "ваш_токен_бота"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот 'Мысли в порядке'.")

# Запуск бота (поллинг)
bot.infinity_polling()
