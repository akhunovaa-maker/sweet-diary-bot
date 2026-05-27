import json, os
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = "8818329273:AAHeCUTLNR-M4FdPt84P-LgCBlErLz5rNi4"
ADMIN_ID = 534720549
USERS_FILE = "users.json"
Q1, Q2, Q3, Q4 = range(4)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE) as f:
            return json.load(f)
    return []

def save_user(chat_id):
    users = load_users()
    if chat_id not in users:
        users.append(chat_id)
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

app = Application.builder().token(TOKEN).build()

async def send_reminder(context=None):
    keyboard = [["🍰 Хочу сладкого!"]]
    for chat_id in load_users():
        try:
            await app.bot.send_message(
                chat_id=chat_id,
                text="Привет! 🍰 Было сегодня что-нибудь сладкое? Если захочется — нажми кнопку!",
                reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            )
        except:
            pass

async def start(update, context):
    save_user(update.effective_chat.id)
    keyboard = [["🍰 Хочу сладкого!"]]
    await update.message.reply_text(
        "Привет! Когда захочется сладкого — нажми кнопку ниже 🍫",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    name = update.effective_user.first_name or "Участник"
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"🟢 Новый участник: {name}")

async def want(update, context):
    keyboard = [["🏠 Дома", "💼 На работе"], ["🚗 В дороге", "👥 С коллегами/друзьями"]]
    await update.message.reply_text(
        "Что сейчас происходит?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return Q1

async def q1(update, context):
    context.user_data["q1"] = update.message.text
    keyboard = [["🎂 Торт/пирожное", "🍫 Шоколад"], ["🍪 Печенье/конфеты", "🤷 Что-нибудь сладкое"]]
    await update.message.reply_text(
        "Чего именно хочется?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return Q2

async def q2(update, context):
    context.user_data["q2"] = update.message.text
    keyboard = [
        ["🏪 Магазин рядом", "🛵 Самокат"],
        ["🍏 Вкусвилл", "🚕 Яндекс Доставка"],
        ["⏳ Потерплю", "✏️ Другое"]
    ]
    await update.message.reply_text(
        "Где скорее всего возьмёшь?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return Q3

async def q3(update, context):
    choice = update.message.text
    if choice == "✏️ Другое":
        await update.message.reply_text(
            "Напиши куда пойдёшь 👇",
            reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True)
        )
        return Q3
    context.user_data["q3"] = choice
    await update.message.reply_text(
        "Как ты себя чувствуешь? Напиши своими словами — устал(а), хочу побаловать себя, просто к чаю, скучно и т.д.",
        reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True)
    )
    return Q4

async def q4(update, context):
    context.user_data["q4"] = update.message.text
    name = update.effective_user.first_name or "Участник"
    username = f"@{update.effective_user.username}" if update.effective_user.username else f"id:{update.effective_user.id}"
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📝 {name} ({username})\n📍 {context.user_data.get('q1','?')}\n🍬 {context.user_data.get('q2','?')}\n🏪 {context.user_data.get('q3','?')}\n💬 {context.user_data.get('q4','?')}"
    )
    keyboard = [["🍰 Хочу сладкого!"]]
    await update.message.reply_text(
        "Записала, спасибо! 🙂\nНажми кнопку снова когда захочется.",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    return ConversationHandler.END

def main():
    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("🍰 Хочу сладкого!"), want)],
        states={
