import asyncio
import os
from datetime import datetime, timezone

from pyrogram import Client, filters, idle
from config import TELEGRAM_LINKS

from dotenv import load_dotenv

load_dotenv()

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
SESSION_NAME = os.environ.get('SESSION_NAME')

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)


async def main():
    await app.start()
    # await idle()
    await app.stop()


app.run(main())