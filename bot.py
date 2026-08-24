import os
import random

from telegram import Update, ReactionTypeCustomEmoji
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("8786728145:AAHRbZUREiX5prYxMrx7yl-AycyA95p2xH0")

CUSTOM_EMOJI_IDS = [
    "6140769030924932147",
    "6181216743701090479",
    "6141064297041631233",
    "6262735489267144566",
    "6141017417473595024",
    "6138769414410999013",
    "6032766773982402861",
    "6255534525623836508",
]


async def react_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message

    if not message:
        return

    custom_emoji_id = random.choice(CUSTOM_EMOJI_IDS)

    try:
        await context.bot.set_message_reaction(
            chat_id=message.chat_id,
            message_id=message.message_id,
            reaction=[
                ReactionTypeCustomEmoji(
                    custom_emoji_id=custom_emoji_id
                )
            ],
        )

        print(
            f"Custom Emoji Reaction: {custom_emoji_id}"
        )

    except Exception as e:
        print(f"Reaction error: {e}")


def main():
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    app = Application.builder().token(BOT_TOKEN).build()

    # Group / Supergroup
    app.add_handler(
        MessageHandler(
            filters.UpdateType.MESSAGES,
            react_to_message,
        )
    )

    # Channel Posts
    app.add_handler(
        MessageHandler(
            filters.UpdateType.CHANNEL_POSTS,
            react_to_message,
        )
    )

    print("Custom Emoji Reaction Bot is running...")

    app.run_polling(
        allowed_updates=["message", "channel_post"]
    )


if __name__ == "__main__":
    main()
