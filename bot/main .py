from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = "8100477393:AAGO6wTC2zd0cJM6Rc4Xyd3WoFczC21y3b0"
ADMIN_ID = 6791111414

reply_targets = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Xabaringizni yozing, men uni adminga yetkazaman 📩")

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Sizning Telegram ID: {update.message.chat_id}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    username = update.message.from_user.username or "username yo‘q"
    text = update.message.text

    if user_id == ADMIN_ID:
        if ADMIN_ID in reply_targets:
            target_id = reply_targets[ADMIN_ID]
            await context.bot.send_message(chat_id=target_id, text=f"📩 Admin javobi:\n{text}")
            await update.message.reply_text("✅ Javob foydalanuvchiga yuborildi.")
            del reply_targets[ADMIN_ID]
        else:
            await update.message.reply_text("ℹ️ Javob berish uchun tugmani bosing.")
    else:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✏️ Javob berish", callback_data=f"reply_{user_id}")]
        ])
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📢 Yangi xabar:\n👤 Username: @{username}\n🆔 ID: {user_id}\n💬 Xabar: {text}",
            reply_markup=keyboard
        )
        await update.message.reply_text("✅ Xabaringiz adminga yuborildi!")

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        await query.edit_message_text("❌ Bu tugma faqat admin uchun.")
        return

    data = query.data
    if data.startswith("reply_"):
        user_id = int(data.split("_")[1])
        reply_targets[ADMIN_ID] = user_id
        await query.message.reply_text("✏️ Javob matnini yozing:")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_click))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
