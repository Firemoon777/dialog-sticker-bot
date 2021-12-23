# Dialog-sticker-bot

Telegram bot receives forwarded message and renders as sticker in a pack.

Created as example for generating stickers with Bot API.

## Requirements

- python 3.8+
- Telegram bot API token

## Install

```bash
# Install dependencies
python3 -m pip install -r requirements.txt

# Copy example config and fill it 
cp dsb.example.toml dsb.toml
```

## Run

```bash
python3 -m dsb
```

## Limitations

- only forwarded messages supported;
- one message at time handled (e.g. sequence of messages will be handled as separate messages);
- no error handling;
- no configuration for stickerset title;