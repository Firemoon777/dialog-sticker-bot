import toml
from dsb.bot import DialogStickerBot
from .handlers import handlers

config = toml.load('dsb.toml')

bot = DialogStickerBot(
    token=config["telegram"]["token"]
)

for h in handlers:
    bot.dispatcher.add_handler(h)

bot.start_polling()
bot.idle()
