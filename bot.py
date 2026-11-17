import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import os
import threading

# Токен нового бота Игорь | Комфорт-авто
TOKEN = "9276621575:AAHXOXyMmEczwE96mMXGA1WOysHzm38jGq4"
bot = telebot.TeleBot(TOKEN)

# Инициализация Flask-сервера для работы 24/7 на Render
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()

# Приветствие при старте /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    
    text = (
        f"Здравствуйте, {user_name}! 🚗\n\n"
        f"Добро пожаловать в личный бот водителя **Игоря**.\n"
        f"⭐ **Стаж за рулем — 15 лет.** Безопасные и комфортные поездки.\n\n"
        f"Маршруты:\n"
        f"• Кара-Балта ⇄ Бишкек\n"
        f"• Каинда, Беловодские, Петровка ⇄ Бишкек\n\n"
        f"Никаких диспетчеров и очередей. Выберите нужное действие или напишите сообщение:"
    )
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("📅 Забронировать поездку (Маршруты)", callback_data="routes"),
        InlineKeyboardButton("💬 Написать в WhatsApp Игорю", url="https://wa.me/996505910613"),
        InlineKeyboardButton("📞 Позвонить (+996 505 910 613)", callback_data="call"),
        InlineKeyboardButton("ℹ️ О водителе и условиях", callback_data="about")
    )
    
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

# Обработка нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "routes":
        bot.answer_callback_query(call.id)
        
        markup_routes = InlineKeyboardMarkup()
        markup_routes.row_width = 1
        markup_routes.add(
            InlineKeyboardButton("🚗 Кара-Балта ⇄ Бишкек", callback_data="order_kb_bish"),
            InlineKeyboardButton("🚗 Бишкек ⇄ Кара-Балта", callback_data="order_bish_kb"),
            InlineKeyboardButton("🚗 Каинда / Беловодское ⇄ Бишкек", callback_data="order_other"),
            InlineKeyboardButton("↩️ Другой маршрут / Свой вопрос", callback_data="custom_order")
        )
        
        bot.send_message(
            call.message.chat.id,
            "Выберите ваше направление:",
            reply_markup=markup_routes
        )
        
    elif call.data.startswith("order_") or call.data == "custom_order":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "✍️ **Отправьте детали поездки сообщением:**\n"
            "• Дата и точное время\n"
            "• Сколько человек / есть ли багаж\n"
            "• Откуда и куда нужно забрать\n\n"
            "Игорь увидит ваше сообщение и сразу свяжется с вами!",
            parse_mode="Markdown"
        )
        
    elif call.data == "call":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "📞 Телефон для прямой связи и срочных заказов:\n**+996 505 910 613** (Игорь)",
            parse_mode="Markdown"
        )
        
    elif call.data == "about":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "⭐ **Информация о сервисе:**\n\n"
            "• Водитель: Игорь\n"
            "
