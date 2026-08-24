import os
import random

from telegram import Update, ReactionTypeEmoji
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8936841134:AAHPjQQrq_cu-nK61kZvPbyQf2RPh9WcL0g"

REACTIONS = ["👀", "🐉", "⚡️", "🥰", "👏", "😁", "🎉"]


async def react_to_message(chat_id, message_id, context):
    emoji = random.choice(REACTIONS)
    try:
        await context.bot.set_message_reaction(
            chat_id=chat_id,
            message_id=message_id,
            reaction=[ReactionTypeEmoji(emoji=emoji)],
        )
    except Exception as e:
        print(f"Reaction error: {e}")


async def group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await react_to_message(
            update.message.chat_id,
            update.message.message_id,
            context,
        )


async def channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ချန်နယ်ပို့စ် တင်လိုက်သည့်အခါ သေချာပေါက် အလုပ်လုပ်စေရန်
    if update.channel_post:
        await react_to_message(
            update.channel_post.chat_id,
            update.channel_post.message_id,
            context,
        )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    # ချန်နယ်အတွက် သီးသန့် အလုပ်လုပ်နိုင်ရန် အခြေခံမှစ၍ ပြင်ဆင်ထားပါသည်
    app = Application.builder().token(BOT_TOKEN).build()

    # 1. Group / Supergroup ဟန်းဒလာ
    app.add_handler(
        MessageHandler(
            filters.ALL & ~filters.StatusUpdate.ALL,
            group_message,
        )
    )

    # 2. Channel ပို့စ်များအတွက် ဟန်းဒလာ (Filter ကို ပိုမိုတိကျအောင် ပြောင်းလဲထားပါသည်)
    app.add_handler(
        MessageHandler(
            filters.UpdateType.CHANNEL_POST,
            channel_post,
        )
    )

    print("Reaction Bot is running...")

    # 🌟 အဓိကအချက် - drop_pending_updates ကို သုံးပြီး စနစ်ဟောင်းများကို ရှင်းလင်းကာ ချန်နယ်အတွက် လမ်းကြောင်းဖွင့်ပေးခြင်း
    app.run_polling(
        allowed_updates=["message", "channel_post"],
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
