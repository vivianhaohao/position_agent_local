import logging
from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes
)
from backend_functions.create_hyper_agent import create_hyper_agent
from backend_functions.encrypt_store import encrypt_store
from users_state.user_state import set_user_state,get_user_state,clear_user_state,set_wallet_address
from tools.add_user_logs import add_user_logs





logger=logging.getLogger(__name__)

async def connect_user_wallet(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_id=update.effective_user.id
    await update.message.reply_text('🔗 Send wallet address.')
    set_user_state(user_id,"waiting_user_wallet")


async def bind_agent_to_wallet(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_id=update.effective_user.id
    message=update.message.text.strip().lower()

    if get_user_state(user_id)!="waiting_user_wallet":
        return

    if not message.startswith("0x") or len(message)!=42:
        await update.message.reply_text('❌Wrong format.')
        return

    wallet=message
    agent=create_hyper_agent()
    set_wallet_address(user_id, wallet)
    try:
        encrypt_store(agent.key, wallet, agent.address)
    except FileExistsError:
        await update.message.reply_text("⚠️ Wallet already binded, if you want to reset agent of your wallet, use /reset"
                                        "\nor use other commands like /sign ")
        clear_user_state(user_id)
        return



    add_user_logs(wallet,"connect",f"...")

    await update.message.reply_text(f'👛Wallet address-{wallet}\n'
                                    f'🤖Agent address-{agent.address}\n'
                                    f'🔐Agent already protected.\n'
                                    f'🟢 Use /sign to connect agent.')

    clear_user_state(user_id)

def register_connect(app):
    app.add_handler(CommandHandler('connect', connect_user_wallet))



