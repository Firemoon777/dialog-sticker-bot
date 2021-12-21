from telegram import Update
from telegram.ext import CallbackContext


def on_message_received(update: Update, context: CallbackContext):
    print(update.message.text)