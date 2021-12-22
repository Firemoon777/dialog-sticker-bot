# -*- coding: utf-8 -*-
import textwrap
from typing import List, Dict

from PIL import Image, ImageDraw
from PIL import ImageFont
from telegram import Message

from .const import *

OPEN_SANS = ImageFont.truetype('OpenSans.ttf', 20)


class BubbleDrawer:
    img: Image
    message: Message

    def __init__(self, msg):
        self.message = msg

    @property
    def _name(self):
        result = self.message["forward_from"]["first_name"]
        if self.message["forward_from"]["last_name"]:
            result += " " + self.message["forward_from"]["last_name"]
        return result

    @property
    def _text(self):
        return textwrap.wrap(self.message["text"], width=38)

    def draw(self):
        # Calculate size of sticker
        # width is constant and fixed to 512
        font_height = OPEN_SANS.getsize(self._text[0])[1]

        width = 512
        height = font_height * (len(self._text) + 1) + 2*BUBBLE_PADDING

        self.img = Image.new('RGBA', (width, height), color=(255, 255, 255, 0))

        d = ImageDraw.Draw(self.img)
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