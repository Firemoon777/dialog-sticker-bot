# -*- coding: utf-8 -*-
import textwrap
from io import BytesIO
from typing import List, Dict, Optional

from PIL import Image, ImageDraw, ImageFilter, ImageOps
from PIL import ImageFont
from telegram import Message

from .const import *

OPEN_SANS = ImageFont.truetype('OpenSans.ttf', 26)


class BubbleDrawer:
    img: Image.Image
    avatar: Optional[Image.Image]
    message: Message

    def __init__(self, msg):
        self.message = msg
        self.avatar = None

    @property
    def _name(self) -> str:
        try:
            result = self.message["forward_from"]["first_name"]
            if self.message["forward_from"]["last_name"]:
                result += " " + self.message["forward_from"]["last_name"]
            return result
        except (KeyError, TypeError):
            return self.message["forward_sender_name"]

    @property
    def _shortname(self) -> str:
        return self._name[0].upper()

    @property
    def _text(self) -> List[str]:
        return textwrap.wrap(self.message["text"], width=30)

    def set_avatar(self, data) -> None:
        # Open original image
        avatar = Image.open(BytesIO(data))  # type: Image.Image

        # Resize it to avatar size, assuming it's already square
        size = (AVATAR_SIZE, AVATAR_SIZE)
        avatar = avatar.resize(size, Image.ANTIALIAS)

        # Make circle with mask
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)

        self.avatar = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
        self.avatar.putalpha(mask)

    def draw(self) -> None:
        # Calculate size of sticker
        # width is constant and fixed to 512
        font_height = OPEN_SANS.getsize(self._text[0])[1]

        width = 512
        height = font_height * (len(self._text) + 1) + 2*BUBBLE_PADDING

        if height > 512:
            raise OverflowError("Image too big")

        self.img = Image.new('RGBA', (width, height), color=(255, 255, 255, 0))

        d = ImageDraw.Draw(self.img)

        # Draw avatar circle
        if self.avatar:
            # Image present, just insert it
            self.img.paste(self.avatar, (0, 0))
        else:
            # Draw circle
            d.ellipse((0, 0, AVATAR_SIZE, AVATAR_SIZE), fill=(64, 167, 227, 255))

            position = (
                (AVATAR_SIZE / 2) - (OPEN_SANS.getsize(self._shortname)[0] / 2),
                (AVATAR_SIZE / 2) - (OPEN_SANS.getsize(self._shortname)[1] / 2) - 4,
            )
            d.text(
                position,
                self._shortname,
                fill="white",
                font=OPEN_SANS
            )

        # Draw message bubble
        d.rounded_rectangle((BUBBLE_X_START, 0, width, height), fill="black", radius=BUBBLE_RADIUS)

        # Draw title, a.k.a. name of sender
        d.text((TEXT_X_START, BUBBLE_PADDING), self._name, fill="pink", font=OPEN_SANS)

        # Draw message body
        offset = BUBBLE_PADDING + font_height
        for line in self._text:
            d.text((TEXT_X_START, offset), line, fill="white", font=OPEN_SANS)
            offset += font_height

    def show(self) -> None:
        if self.img is None:
            return

        self.img.show()

    def save(self, filename) -> None:
        if self.img is None:
            return

        self.img.save(filename, 'PNG')