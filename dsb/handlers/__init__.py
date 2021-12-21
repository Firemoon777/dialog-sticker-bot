from telegram.ext import MessageHandler, Filters

from dsb.handlers.message import on_message_received

handlers = [
    MessageHandler(Filters.update.message, on_message_received)
]