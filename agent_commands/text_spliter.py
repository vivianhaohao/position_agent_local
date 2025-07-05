from telegram import Update
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    filters)
from users_state.user_state import get_user_state
from agent_commands.connect_wallet import bind_agent_to_wallet
from backend_functions.analyze_user_strategy import analyze_user_strategy


async def handle_text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    user_state = get_user_state(user_id)

    print(f"📨 Receive text: {text}")
    print(f"🔍 User state: {user_state}")

    if user_state == "waiting_user_wallet":
        await bind_agent_to_wallet(update, context)
    elif user_state == "waiting_user_strategy":
        await analyze_user_strategy(update, context)
    else:
        await update.message.reply_text("🤖 Use commands first.")

def register_text_router(app):
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_router))
