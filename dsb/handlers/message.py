import logging
import uuid
from io import BytesIO

from telegram import Update, UserProfilePhotos, File, StickerSet
from telegram.error import BadRequest
from telegram.ext import CallbackContext

from dsb.drawer import BubbleDrawer

DEFAULT_EMOJI="\U0001F4AC"  # :speech_balloon:


def on_message_received(update: Update, context: CallbackContext):
    # Ignore another updates
    if not update.message:
        return

    # Ignore groups
    if update.message.chat_id != update.message.from_user.id:
        return

    if not update.message.forward_from:
        update.message.reply_text("Only forwarded messages supported!")
        return

    # Generate sticker id
    sid = f"{update.message.from_user.id}-{context.bot_data.get('salt', '')}"
    # Generate hash-based uuid
    uid = str(uuid.uuid5(uuid.NAMESPACE_X500, sid))
    # Remove dashes from name
    uid = uid.replace("-", "")
    # Telegram API requires letter at beginning of the name
    sticker_set_name = f"s{uid}_by_{context.bot_data['name']}"

    # Create message bubble
    bio = BytesIO()
    b = BubbleDrawer(update.message)

    # get latest user avatar
    result = context.bot.get_user_profile_photos(update.message.forward_from.id, limit=1)   # type: UserProfilePhotos
    if result.total_count > 0:
        # TODO: get smallest suitable userpic
        file = context.bot.get_file(result.photos[0][0].file_id)    # type: File
        b.set_avatar(file.download_as_bytearray())

    b.draw()
    b.save(bio)
    bio.seek(0)

    try:
        # Try to fetch sticker set
        sticker_set = context.bot.get_sticker_set(sticker_set_name) # type: StickerSet

        if len(sticker_set.stickers) >= 120:
            update.message.reply_text("Sticker set is full")
            return

        context.bot.add_sticker_to_set(
            user_id=update.message.from_user.id,
            name=sticker_set_name,
            emojis=DEFAULT_EMOJI,
            png_sticker=bio
        )
    except BadRequest as e:
        if e.message != "Stickerset_invalid":
            logging.error(e.message)
            return
        # If no sticker set fetched, create new
        created = context.bot.create_new_sticker_set(
            user_id=update.message.from_user.id,
            name=sticker_set_name,
            title=f"Custom Sticker for user {update.message.from_user.first_name}",
            emojis=DEFAULT_EMOJI,
            png_sticker=bio
        )

        logging.info(f"Created sticker pack {sticker_set_name}")

    sticker_set = context.bot.get_sticker_set(sticker_set_name)  # type: StickerSet
    update.message.reply_sticker(sticker_set.stickers[-1])
