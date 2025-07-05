from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes
)
from users_state.user_state import get_wallet_address
from backend_functions.save_user_strategy import load_all_strategy


async def check_strategy_status(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_id=update.effective_user.id
    wallet=get_wallet_address(user_id)
    if not wallet:
        await update.message.reply_text("❌Bind wallet first.")
        return

    all_strategy=load_all_strategy(wallet)
    if not all_strategy:
        await update.message.reply_text("❌Input strategies first.")
        return

    message=f'There are {len(all_strategy)} strategies.\n\n'
    for strategy in all_strategy:
        name=strategy.get('name','NA')
        side=strategy.get('side','NA')
        type=strategy.get('type','NA')
        amount=strategy.get('amount',0)
        range=strategy.get('range','NA')
        depth=strategy.get('depth','NA')
        tp = strategy.get('tp', 'NA')
        sl=strategy.get('sl','NA')

        message+=(f"Strategy name-{name}, trade direction-{side}, order type-{type}, amount-{amount}, "
                  f"price range-{range}, min order depth-{depth}, stop loss-{sl}, tp-{tp}\n")

    await update.message.reply_text(message)

def register_status(app):
    app.add_handler(CommandHandler("status", check_strategy_status))
