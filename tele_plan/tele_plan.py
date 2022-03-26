
import asyncio
from html import entities
import logging
import os
from typing import List
import httpx

from datetime import date
from aiogram import Bot, Dispatcher, types, utils
from timetable_entry import Entry, from_json, to_markdown

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
    )

logger = logging.getLogger(__name__)


async def get_timetable(telegram_message: types.Message):
    date_today = date.today()
    # TODO: Make groups customizable by env (?) or select them at `/start`
    base_url="https://altapi.kpostek.dev/v1/timetable/date/{}?groups={}&groups={}".format(date_today,"WIs I.2 - 46c","WIs I.2 - 1w")
    async with httpx.AsyncClient() as client:
        r = await client.get(base_url)
    json = r.json()
    if len(json['entries']) == 0:
        message = utils.markdown.bold("Dzisiaj nie masz lekcji! 😎")
        await telegram_message.answer(message,types.ParseMode.MARKDOWN_V2)
    else:
        message = "*Oto twój plan lekcji na dziś:*\n"
        entries: List[Entry] = []
        for entry in json['entries']:
            entries.append(from_json(entry))
        await telegram_message.answer(message + "".join(map(to_markdown,entries)),parse_mode=types.ParseMode.MARKDOWN_V2)

async def main():
    # Grab an API token from `env``
    token = os.getenv("TELEGRAM_BOT_API")
    # Create the Bot
    bot = Bot(token)
    try:
        # Get the dispatcher to register handlers
        dispatcher = Dispatcher(bot)
        # Register commands
        dispatcher.register_message_handler(get_timetable,commands={"today"})
        # Start the bot
        await dispatcher.start_polling()
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
    