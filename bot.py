import requests
import random
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

domains = ["1secmail.com", "1secmail.org", "1secmail.net"]

def generate_email():
    name = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz123456789') for _ in range(10))
    domain = random.choice(domains)
    return name, domain

def get_messages(login, domain):
    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
    return requests.get(url).json()

def read_message(login, domain, msg_id):
    url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}"
    return requests.get(url).json()

def extract_otp(text):
    otp = re.findall(r'\b\d{4,8}\b', text)
    return otp[0] if otp else "Not found"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    login, domain = generate_email()
    context.user_data['login'] = login
    context.user_data['domain'] = domain

    email = f"{login}@{domain}"

    keyboard = [
        [InlineKeyboardButton("📥 Check Inbox", callback_data="check")],
        [InlineKeyboardButton("🔄 New Email", callback_data="new")]
    ]

    await update.message.reply_text(
        f"📧 Your Temp Mail:\n{email}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    login = context.user_data.get('login')
    domain = context.user_data.get('domain')

    if query.data == "new":
        await start(query, context)
        return

    if query.data == "check":
        msgs = get_messages(login, domain)

        if not msgs:
            await query.edit_message_text("📭 No messages yet")
            return

        text = ""
        for m in msgs:
            msg = read_message(login, domain, m['id'])
            otp = extract_otp(msg['textBody'])

            text += f"📩 From: {m['from']}\n"
            text += f"Subject: {m['subject']}\n"
            text += f"OTP: {otp}\n\n"

        await query.edit_message_text(text)

app = ApplicationBuilder().token("7515671011:AAG-ZcjpUrvQamploYprjciYxj5bW47esgc").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
