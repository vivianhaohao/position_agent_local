import logging
from telegram.ext import (
    CommandHandler,
    ContextTypes
)
from telegram import Update
from users_state.user_state import set_user_state,get_wallet_address
from tools.add_user_logs import add_user_logs



logger=logging.getLogger(__name__)
async def input_strategy(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_id=update.effective_user.id
    set_user_state(user_id,"waiting_user_strategy")
    wallet = get_wallet_address(user_id)

    if wallet:
        add_user_logs(wallet, "strategy", "writing_strategy")


    await update.message.reply_text(
        "name:\n"
        "side:\n"
        "type:\n"
        "amount:\n"
        "range:\n"
        "depth:\n"
        "tp:\n"
        "sl:\n\n"
    )

def register_strategy(app):
    app.add_handler(CommandHandler("strategy", input_strategy))

