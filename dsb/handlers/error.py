import logging

from telegram.ext import CallbackContext


def error_handler(update: object, context: CallbackContext) -> None:
    if str(context.error) == "Image too big":
        context.bot.send_message(
            update.message.from_user.id,
            "Forwarded message is big and can not be rendered in 512x512"
        )
        return
    logging.error(str(context.error))
    context.bot.send_message(
        update.message.from_user.id,
        "Something went wrong"
    )