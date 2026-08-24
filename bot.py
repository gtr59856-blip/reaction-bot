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

REACTIONS = ["👍", "❤️", "🔥", "🥰", "👏", "😁", "🎉"]


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
    # ချန်နယ်ထဲမှာ ပို့စ်အသစ်တင်တိုင်း Reaction ပေးရန် စစ်ဆေးခြင်း
    if update.channel_post:
        await react_to_message(
            update.channel_post.chat_id,
            update.channel_post.message_id,
            context,
        )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    app = Application.builder().token(BOT_TOKEN).build()

    # Group / Supergroup အတွက်
    app.add_handler(
        MessageHandler(
            filters.ALL & ~filters.StatusUpdate.ALL,
            group_message,
        )
    )

    # 🌟 ချန်နယ်ပို့စ်များကို သေချာပေါက်ဖတ်နိုင်ရန် UpdateType ကိုပါ ထည့်သွင်းပြင်ဆင်ထားပါသည်
    app.add_handler(
        MessageHandler(
            filters.ChatType.CHANNEL | filters.UpdateType.CHANNEL_POST,
            channel_post,
        )
    )

    print("Reaction Bot is running...")

    app.run_polling(
        allowed_updates=["message", "channel_post"]
    )


if __name__ == "__main__":
    main()
