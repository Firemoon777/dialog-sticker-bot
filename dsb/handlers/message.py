from io import BytesIO

from telegram import Update, UserProfilePhotos, File
from telegram.error import BadRequest
from telegram.ext import CallbackContext

from dsb.drawer import BubbleDrawer

DEFAULT_EMOJI="\U0001F4AC"  # :speech_balloon:


def on_message_received(update: Update, context: CallbackContext):
    sticker_set_name = f"custom{update.message.from_user.id}_by_{context.bot_data['name']}"
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
        sticker_set = context.bot.get_sticker_set(sticker_set_name)
        context.bot.add_sticker_to_set(
            user_id=update.message.from_user.id,
            name=sticker_set_name,
            emojis=DEFAULT_EMOJI,
            png_sticker=bio
        )
        update.message.reply_text("Added")
    except BadRequest:
        created = context.bot.create_new_sticker_set(
            user_id=update.message.from_user.id,
            name=sticker_set_name,
            title=f"Custom Sticker for user {update.message.from_user.first_name}",
            emojis=DEFAULT_EMOJI,
            png_sticker=bio
        )
        print(created)
        update.message.reply_text(f"Created: {created}")