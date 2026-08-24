import os
import random
from telegram import Update, ReactionTypeEmoji
from telegram.ext import (
    Application,
    MessageHandler,
    ChannelPostHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

REACTIONS = ["👍", "❤️", "🔥", "🥰", "👏", "😁", "🎉"]


async def react_to_message(chat_id, message_id, context):
    emoji = random.choice(REACTIONS)

    try:
        await context.bot.set_message_reaction(
            chat_id=chat_id,
            message_id=message_id,
            reaction=[ReactionTypeEmoji(emoji)],
        )
        print(f"Reaction: {emoji}")

    except Exception as e:
        print(f"Error: {e}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message:
        return

    await react_to_message(
        update.effective_chat.id,
        update.effective_message.message_id,
        context,
    )


async def handle_channel_post(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.channel_post:
        return

    await react_to_message(
        update.channel_post.chat.id,
        update.channel_post.message_id,
        context,
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.ALL,
            handle_message,
        )
    )

    app.add_handler(
        ChannelPostHandler(handle_channel_post)
    )

    print("Reaction Bot Started...")

    app.run_polling(
        allowed_updates=[
            "message",
            "channel_post",
        ]
    )


if __name__ == "__main__":
    main()
