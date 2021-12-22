# -*- coding: utf-8 -*-
import toml
from dsb.bot import DialogStickerBot
from .drawer import BubbleDrawer
from .handlers import handlers

config = toml.load('dsb.toml')

bot = DialogStickerBot(
    token=config["telegram"]["token"]
)

for h in handlers:
    bot.dispatcher.add_handler(h)

bot.dispatcher.bot_data = {
    "name": config["telegram"]["name"]
}
bot.start_polling()
bot.idle()

