# -*- coding: utf-8 -*-
import logging

import toml
from dsb.bot import DialogStickerBot
from .drawer import BubbleDrawer
from .handlers import handlers, error_handlers

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

config = toml.load('dsb.toml')

bot = DialogStickerBot(
    token=config["telegram"]["token"]
)

for h in handlers:
    bot.dispatcher.add_handler(h)

for eh in error_handlers:
    bot.dispatcher.add_error_handler(eh)

bot.dispatcher.bot_data = {
    "name": config["telegram"]["name"],
    "salt": config["telegram"].get("salt", "")
}
bot.start_polling()
bot.idle()
