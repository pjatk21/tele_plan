import asyncio
import logging
import os
from typing import List
import httpx

from datetime import date
from aiogram import Bot, Dispatcher, types, utils, executor
from timetable_entry import Entry

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Init bot and dispatcher
if not os.getenv("TELEGRAM_BOT_API"):
    raise Exception("TELEGRAM_BOT_API env variable not set")

bot = Bot(token=os.getenv("TELEGRAM_BOT_API"))
dp = Dispatcher(bot)


@dp.message_handler(commands=["today"])
async def get_timetable(telegram_message: types.Message):
    date_today = date.today()
    # TODO: Make groups customizable by env (?) or select them at `/start`
    url = f"https://altapi.kpostek.dev/v1/timetable/date/{date_today.isoformat()}"

    async with httpx.AsyncClient() as client:
        r = await client.get(url, params={"groups": ["WIs I.2 - 46c", "WIs I.2 - 1w"]})
    payload = r.json()

    if not payload['entries']:
        message = utils.markdown.bold("Dzisiaj nie masz lekcji! 😎")
        await telegram_message.answer(message, types.ParseMode.MARKDOWN_V2)
    else:
        message = "*Oto twój plan lekcji na dziś:*\n"
        entries: List[Entry] = list(map(Entry.from_json, payload['entries']))
        entries.sort(key=lambda entry: entry.begin)

        await telegram_message.answer(message + "".join(map(lambda x: x.to_markdown(), entries)), parse_mode=types.ParseMode.MARKDOWN_V2)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
