# YouBike Status Telegram Bot

A Telegram bot written in Python with [aiogram](https://github.com/aiogram/aiogram) (a fully asynchronous framework).

## Motivation

The reason why I develope this bot is because I think the searching function provided by official YouBike mobile application is no good. Since I am a heavy user of Telegram, I decide to create a bot on Telegram platform instead of other mobile communication applications.

## What can this chatbot do

Users can search and check the status of YouBike stations by sending keywords or GPS coordinates to the bot.

## Try it!

Demo: [@youbike_toolman_bot](https://t.me/youbike_toolman_bot)

## Or create one by yourself

### Requirements
- Python 3.7+
- [aiogram](https://github.com/aiogram/aiogram)
- [requests](https://docs.python-requests.org/en/latest/)

### Usage

1. Create a telegram bot by [@BotFather](https://t.me/BotFather)
2. Fill in [`bot_token`](bot.py#L7) in [`bot.py`](bot.py) with your Telegram bot token
3. Run `python3 bot.py`
