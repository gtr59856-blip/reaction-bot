import os
import random

from telegram import Update, ReactionTypeCustomEmoji  # Custom Emoji အတွက်
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8802266198:AAHmzywZuGKt2XjVt_BqckEfrYKkQoIsLE8"

# 🌟 သင်ပေးပို့ထားသော ပရီမီယံ အီမိုဂျီ ID များကို မှန်ကန်စွာ ထည့်သွင်းပေးထားပါသည်
PREMIUM_EMOJIS = [
    "6140769030924932147",
    "6181216743701090479",
    "6141064297041631233",
    "6262735489267144566",
    "6141017417473595024",
    "6138769414410999013",
    "6032766773982402861",
    "6255534525623836508",
]


async def react_to_message(chat_id, message_id, context):
    chosen_emoji_id = random.choice(PREMIUM_EMOJIS)

    try:
        await context.bot.set_message_reaction(
            chat_id=chat_id,
            message_id=message_id,
            # ReactionTypeCustomEmoji ဖြင့် ပရီမီယံအီမိုဂျီ ID ကို ပို့ပေးခြင်း
            reaction=[ReactionTypeCustomEmoji(custom_emoji_id=chosen_emoji_id)],
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

    # 1. Group / Supergroup ဟန်းဒလာ
    app.add_handler(
        MessageHandler(
            filters.ALL & ~filters.StatusUpdate.ALL,
            group_message,
        )
    )

    # 2. Channel ပို့စ်များအတွက် ဟန်းဒလာ
    app.add_handler(
        MessageHandler(
            filters.UpdateType.CHANNEL_POST,
            channel_post,
        )
    )

    print("Premium Reaction Bot is running...")

    app.run_polling(
        allowed_updates=["message", "channel_post"],
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
