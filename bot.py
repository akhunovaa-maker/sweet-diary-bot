import json, os
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = "8818329273:AAHeCUTLNR-M4FdPt84P-LgCBlErLz5rNi4"
ADMIN_ID = 534720549
USERS_FILE = "users.json"
Q1, Q2, Q3, Q4, Q5, Q6 = range(6)
Q1_OTHER, Q2_OTHER, Q3_OTHER, Q4_OTHER, Q5_OTHER = range(6, 11)

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
    keyboard = [["🏠 Дома", "🏢 В офисе"], ["☕️ В кафе", "🚗 В дороге"], ["✏️ Другое"]]
    await update.message.reply_text(
        "Где ты сейчас?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return Q1

async def q1(update, context):
    if update.message.text == "✏️ Другое":
        await update.message.reply_text("Напиши где ты 👇", reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True))
        return Q1_OTHER
    context.user_data["q1"] = update.message.text
    keyboard = [["💻 Работаю", "😌 Отдыхаю"], ["🎬 Смотрю кино/сериал", "👥 Общаюсь с людьми"], ["✏️ Другое"]]
    await update.message.reply_text(
        "Что делаешь?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return Q2

async def q1_other(update, context):
    context.user_data["q1"] = update.message.text
    keyboard = [["💻 Работаю", "😌 Отдыхаю"], ["🎬 Смотрю кино/сериал", "👥 Общаюсь с людьми"], ["✏️ Другое"]]
    await update.message.reply_text(
        "Что делаешь?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return Q2

async def q2(update, context):
    if update.message.text == "✏️ Другое":
        await update.message.reply_text("Напиши что делаешь 👇", reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True))
        return Q2_OTHER
    context.user_data["q2"] = update.message.text
    keyboard = [["🧍 Один(а)", "👔 С коллегами"], ["👫 С друзьями", "👨‍👩‍👧 С семьёй"], ["✏️ Другое"]]
    await update.message.reply_text(
        "С кем ты?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return Q3

async def q2_other(update, context):
    context.user_data["q2"] = update.message.text
    keyboard = [["🧍 Один", "👔 С коллегами"], ["👫 С друзьями", "👨‍👩‍👧 С семьёй"], ["✏️ Другое"]]
    await update.message.reply_text(
        "С кем ты?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return Q3

async def q3(update, context):
    if update.message.text == "✏️ Другое":
        await update.message.reply_text("Напиши с кем ты 👇", reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True))
        return Q3_OTHER
    context.user_data["q3"] = update.message.text
    keyboard = [["🎂 Торт/пирожное", "🍫 Шоколад"], ["🍪 Печенье/конфеты", "🤷 Что-нибудь сладкое"], ["✏️ Другое"]]
    await update.message.reply_text(
        "Чего именно хочется?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return Q4

async def q3_other(update, context):
    context.user_data["q3"] = update.message.text
    keyboard = [["🎂 Торт/пирожное", "🍫 Шоколад"], ["🍪 Печенье/конфеты", "🤷 Что-нибудь сладкое"], ["✏️ Другое"]]
    await update.message.reply_text(
        "Чего именно хочется?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return Q4

async def q4(update, context):
    if update.message.text == "✏️ Другое":
        await update.message.reply_text("Напиши что именно хочется 👇", reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True))
        return Q4_OTHER
    context.user_data["q4"] = update.message.text
    keyboard = [
        ["🏪 Магазин рядом", "🛵 Самокат"],
        ["🍏 Вкусвилл", "🚕 Яндекс Доставка"],
        ["🏠 Дома есть в запасах", "⏳ Потерплю"],
        ["✏️ Другое"]
    ]
    await update.message.reply_text(
        "Где скорее всего возьмёшь?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return Q5

async def q4_other(update, context):
    context.user_data["q4"] = update.message.text
    keyboard = [
        ["🏪 Магазин рядом", "🛵 Самокат"],
        ["🍏 Вкусвилл", "🚕 Яндекс Доставка"],
        ["🏠 Дома есть в запасах", "⏳ Потерплю"],
        ["✏️ Другое"]
    ]
    await update.message.reply_text(
        "Где скорее всего возьмёшь?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return Q5

async def q5(update, context):
    if update.message.text == "✏️ Другое":
        await update.message.reply_text("Напиши куда пойдёшь 👇", reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True))
        return Q5_OTHER
    context.user_data["q5"] = update.message.text
    await update.message.reply_text(
        "Как ты себя чувствуешь? Напиши своими словами — усталость, хочу побаловать себя, просто к чаю, скучно и т.д.",
        reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True)
    )
    return Q6

async def q5_other(update, context):
    context.user_data["q5"] = update.message.text
    await update.message.reply_text(
        "Как ты себя чувствуешь? Напиши своими словами — усталость, хочу побаловать себя, просто к чаю, скучно и т.д.",
        reply_markup=ReplyKeyboardMarkup([[]], resize_keyboard=True)
    )
    return Q6

async def q6(update, context):
    context.user_data["q6"] = update.message.text
    name = update.effective_user.first_name or "Участник"
    username = f"@{update.effective_user.username}" if update.effective_user.username else f"id:{update.effective_user.id}"
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"📝 {name} ({username})\n"
            f"📍 {context.user_data.get('q1','?')}\n"
            f"🎯 {context.user_data.get('q2','?')}\n"
            f"👥 {context.user_data.get('q3','?')}\n"
            f"🍬 {context.user_data.get('q4','?')}\n"
            f"🏪 {context.user_data.get('q5','?')}\n"
            f"💬 {context.user_data.get('q6','?')}"
        )
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
            Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, q1)],
            Q1_OTHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, q1_other)],
            Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, q2)],
            Q2_OTHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, q2_other)],
            Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, q3)],
            Q3_OTHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, q3_other)],
            Q4: [MessageHandler(filters.TEXT & ~filters.COMMAND, q4)],
            Q4_OTHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, q4_other)],
            Q5: [MessageHandler(filters.TEXT & ~filters.COMMAND, q5)],
            Q5_OTHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, q5_other)],
            Q6: [MessageHandler(filters.TEXT & ~filters.COMMAND, q6)],
        },
        fallbacks=[CommandHandler("start", start)]
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_reminder, "cron", hour=9, minute=0)
    scheduler.start()

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
