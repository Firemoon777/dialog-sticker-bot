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
    def _name(self):
        if "forward_sender_name" in self.message:
            return self.message["forward_sender_name"]
        result = self.message["forward_from"]["first_name"]
        if self.message["forward_from"]["last_name"]:
            result += " " + self.message["forward_from"]["last_name"]
        return result

    @property
    def _text(self):
        return textwrap.wrap(self.message["text"], width=30)

    def set_avatar(self, data):
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

    def draw(self):
        # Calculate size of sticker
        # width is constant and fixed to 512
        font_height = OPEN_SANS.getsize(self._text[0])[1]

        width = 512
        height = font_height * (len(self._text) + 1) + 2*BUBBLE_PADDING

        if height > 512:
            raise OverflowError("Image too big")

        self.img = Image.new('RGBA', (width, height), color=(255, 255, 255, 0))

        d = ImageDraw.Draw(self.img)
        if self.avatar:
            self.img.paste(self.avatar, (0, 0))
        else:
            d.ellipse((0, 0, AVATAR_SIZE, AVATAR_SIZE), fill="blue")
        d.rounded_rectangle((BUBBLE_X_START, 0, width, height), fill="black", radius=BUBBLE_RADIUS)
        d.text((TEXT_X_START, BUBBLE_PADDING), self._name, fill="pink", font=OPEN_SANS)

        offset = BUBBLE_PADDING + font_height
        for line in self._text:
            d.text((TEXT_X_START, offset), line, fill="white", font=OPEN_SANS)
            offset += font_height

    def show(self):
        if self.img is None:
            return

        self.img.show()

    def save(self, filename):
        if self.img is None:
            return

        self.img.save(filename, 'PNG')