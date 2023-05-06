import asyncio
import os
import sys
from datetime import datetime, timedelta

import pyrogram
from progress.bar import IncrementalBar
from pyrogram.enums import ChatType

from config import TELEGRAM_LINKS, my_channel_link

from pyrogram import Client, types, filters

from dotenv import load_dotenv

load_dotenv()

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
SESSION_NAME = os.environ.get('SESSION_NAME')

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)
target_date = datetime(2023, 5, 5)
chat_ids = []


async def send_message(message):
    if message.text:
        await app.send_message(my_channel, message.text, entities=message.entities)
    elif message.photo:
        await app.send_photo(
            my_channel,
            message.photo.file_id,
            caption=message.caption
        )
    elif message.video:
        await app.send_video(
            my_channel,
            message.video.file_id,
            caption=message.caption
        )
    elif message.audio:
        await app.send_audio(
            my_channel,
            message.audio.file_id,
            caption=message.caption
        )
    elif message.document:
        await app.send_document(
            my_channel,
            message.document.file_id,
            caption=message.caption
        )


@app.on_message(filters.chat(chat_ids))
async def handle_new_message(client, message):
    await send_message(message)


async def main():
    await app.start()
    messages_to_forward = []
    seen_messages = set()

    date_month_ago = target_date - timedelta(days=30)

    global my_channel
    my_channel = await app.get_chat(my_channel_link if my_channel_link.split('/')[-1].startswith('+') else my_channel_link.split('/')[-1])
    if my_channel.type == 'channel' and type(my_channel) == types.ChatPreview:
        my_channel = await app.join_chat(my_channel_link)
    elif my_channel.type != ChatType.CHANNEL:
        print('Ссылка на ваш чат не является ссылкой на группу')
        sys.exit(1)
    my_channel = my_channel.id

    async for message in app.get_chat_history(my_channel):
        if message.date < date_month_ago:
            break
        seen_messages.add(message.text)
    bar = IncrementalBar('Обработка прошлых сообщений', max=len(TELEGRAM_LINKS), suffix='%(percent)d%% [%(eta)d сек]')
    bar.start()
    for chat in TELEGRAM_LINKS:
        source_channel = await app.get_chat(chat if chat.split('/')[-1].startswith('+') else chat.split('/')[-1])
        if source_channel.type == 'channel' and type(source_channel) == types.ChatPreview:
            source_channel = await app.join_chat(chat)
        elif source_channel.type != ChatType.CHANNEL:
            print(f'Ссылка на чат {chat} не является ссылкой на группу')

        source_channel = source_channel.id
        chat_ids.append(source_channel)

        async for message in app.get_chat_history(source_channel):
            if message.date < target_date:
                break
            if message.text and message.text not in seen_messages:
                seen_messages.add(message.text)
                messages_to_forward.append(message)
        await asyncio.sleep(1)
        bar.next()
    bar.finish()
    if messages_to_forward:
        bar = IncrementalBar('Отправка сообщений', max=len(messages_to_forward))
        bar.start()
        for message in sorted(messages_to_forward, key=lambda mes: mes.date):
            await send_message(message)
            bar.next()
        bar.finish()

        print('Все старые сообщения обработаны')
    else:
        print('Нет старых сообщений')

    await pyrogram.idle()
    await app.stop()
app.run(main())
