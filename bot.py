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

app = Application.builder().token(TOK
