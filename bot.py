from flask import Flask
import os
import threading
import telebot

# Токен вашего бота «Мысли в порядке»
TOKEN = "9294883225:AAE9HC5YvrO6DI3RwrfvnawY9TymJuOWty8"
bot = telebot.TeleBot(TOKEN)

# Инициализация Flask-сервера, чтобы Render держал порт открытым 24/7
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Запускаем Flask в отдельном фоновом потоке
threading.Thread(target=run_flask).start()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Бот «Мысли в порядке» успешно запущен и работает в облаке 24/7! 🌿")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Ваши мысли приняты: {message.text}")

# Запуск бота (поллинг)
if __name__ == "__main__":
    bot.infinity_polling()
