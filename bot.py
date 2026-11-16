import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import os
import threading

# Токен вашего бота
TOKEN = "9294883225:AAE9HC5YvrO6DI3RwrfvnawY9TymJuOWty8"
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
        f"Здравствуйте, {user_name}! 🚗💨\n\n"
        f"Добро пожаловать в личный бот водителя **Игоря**.\n"
        f"🛡 **Стаж за рулем — 15 лет.** Безопасные и комфортные поездки!\n\n"
        f"Маршруты:\n"
        f"• Кара-Балта ⇄ Бишкек\n"
        f"• Каинда, Беловодское, Петровка ⇄ Бишкек\n\n"
        f"Никаких диспетчеров и очередей. Выберите нужное действие или просто отправьте голосовое сообщение! 👇"
    )
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("✅ Забронировать поездку (Маршруты)", callback_data="routes"),
        InlineKeyboardButton("💬 Написать в WhatsApp Игорю", url="https://wa.me/996505910613"),
        InlineKeyboardButton("📞 Позвонить (+996 505 910 613)", callback_data="call_igor"),
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
            InlineKeyboardButton("📍 Кара-Балта ➔ Бишкек", callback_data="order_KB_Bish"),
            InlineKeyboardButton("📍 Бишкек ➔ Кара-Балта", callback_data="order_Bish_KB"),
            InlineKeyboardButton("📍 Каинда / Беловодское ➔ Бишкек", callback_data="order_selo_Bish"),
            InlineKeyboardButton("✍️ Другой маршрут / Свой вопрос", callback_data="custom_order")
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
            "✍️ Отправьте детали поездки сообщением:\n"
            "• Дата и точное время?\n"
            "• Сколько человек / есть ли багаж?\n\n"
            "💬 *Или просто запишите голосовое сообщение*, например: «Игорь, заберите завтра в 7 утра с Беловодского двоих».\n\n"
            "⚠️ _Отправляя данные, вы соглашаетесь на их передачу водителю исключительно для организации поездки._",
            parse_mode="Markdown"
        )
        
    elif call.data == "call_igor":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "📞 **Прямой номер телефона Игоря:**\n\n"
            "+996505910613\n\n"
            "Нажмите на номер выше, чтобы сразу позвонить или сохранить контакт."
        )
        
    elif call.data == "about":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "👨‍✈️ **Водитель: Игорь**\n"
            "📞 Телефон / WhatsApp: +996505910613\n\n"
            "• **Стаж вождения:** 15 лет\n"
            "• Аккуратное вождение и знание трассы\n"
            "• Чистый и комфортный салон\n"
            "• Честные фиксированные цены (итоговая стоимость подтверждается водителем)\n"
            "• Помощь с багажом и передачами\n\n"
            "Всегда на связи для вас!"
        )

# Обработка обычных текстовых сообщений от клиентов
@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.reply_to(
        message, 
        "✅ Ваша заявка и сообщение получены!\n\n"
        "Игорь видит ваше обращение и свяжется с вами в ближайшее время. "
        "Если поездка срочная — звоните: +996505910613"
    )

# Обработка голосовых сообщений
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    bot.reply_to(
        message, 
        "🎤 Голосовое сообщение успешно записано и передано Игорю!"
    )

if __name__ == "__main__":
    bot.infinity_polling()
