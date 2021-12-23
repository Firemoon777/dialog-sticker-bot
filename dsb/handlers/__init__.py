from telegram.ext import MessageHandler, Filters

from dsb.handlers.error import error_handler
from dsb.handlers.message import on_message_received

handlers = [
    MessageHandler(Filters.text & ~Filters.command, on_message_received)
]

error_handlers = [
    error_handler
]