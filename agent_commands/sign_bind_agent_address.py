from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes
)
from tools.add_user_logs import add_user_logs
from users_state.user_state import set_user_state,get_user_state,clear_user_state,get_wallet_address
from backend_functions.encrypt_store import get_agent_address




async def sign_user_to_bind_agent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    wallet = get_wallet_address(user_id)
    if not wallet:
        await update.message.reply_text("⚠️ Use /connect connect wallet.")
        return

    try:
        agent_address = get_agent_address(wallet)
        user_state = get_user_state(user_id)

        if user_state != "sign_pending":
            await update.message.reply_text(
                f"🔐 Go to HyperLiquid website bind agent: \n\n"
                f"👛 Main wallet: {wallet}\n"
                f"🤖 Agent wallet: {agent_address}\n\n"
                f"👉 Open website: https://app.hyperliquid.xyz\n"
                f"➡️ Click “more” > API > paste agent address > sign\n"
                f"⚠️ Click /sign again to confirm."
            )
            set_user_state(user_id, "sign_pending")
            add_user_logs(wallet, "sign_pending", f"Bind agent wallet: {agent_address}")
        else:
            clear_user_state(user_id)
            await update.message.reply_text("🟢Bind successfully, click /strategy to input strategies.")
            add_user_logs(wallet, "..", f"...")

    except Exception as e:
        add_user_logs(wallet, "..", f"{e}")
        await update.message.reply_text("❌ Can not read agent address, use /connect to connect main wallet.")

def register_sign(app):
    app.add_handler(CommandHandler("sign", sign_user_to_bind_agent))
