import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Get token from environment (SAFE)
TOKEN = os.getenv("7515671011:AAG-ZcjpUrvQamploYprjciYxj5bW47esgc")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    domains = ["1secmail.com", "1secmail.org", "1secmail.net"]
    name = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz123456789') for _ in range(10))
    domain = random.choice(domains)

    email = f"{name}@{domain}"

    await update.message.reply_text(f"📧 Your Fake Mail:\n{email}")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start to generate fake mail")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))

print("Bot running...")

app.run_polling()
