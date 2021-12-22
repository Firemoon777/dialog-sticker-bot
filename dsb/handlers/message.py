from io import BytesIO

from telegram import Update
from telegram.ext import CallbackContext

from dsb.drawer import BubbleDrawer


def on_message_received(update: Update, context: CallbackContext):
    bio = BytesIO()
    b = BubbleDrawer(update.message)
    b.draw()
    b.save(bio)
    bio.seek(0)
    update.message.reply_document(bio, "example.png")