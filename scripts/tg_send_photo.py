#!/usr/bin/env python3
import asyncio, sys
from tg_common import CFG, SESS, API_ID, API_HASH
from telethon import TelegramClient
from telethon.sessions import SQLiteSession
from telethon.tl.types import InputReplyToMessage, InputMediaUploadedPhoto
from telethon.tl.functions.messages import SendMediaRequest

CHAT_ID = int(sys.argv[1])
TOPIC_ID = int(sys.argv[2])
PHOTO = sys.argv[3]

async def main():
    c = TelegramClient(SQLiteSession(SESS), API_ID, API_HASH)
    await c.connect()
    if not await c.is_user_authorized():
        print('NOT_AUTHORIZED')
        return
    peer = await c.get_input_entity(CHAT_ID)
    uploaded = await c.upload_file(PHOTO)
    updates = await c(SendMediaRequest(
        peer=peer, media=InputMediaUploadedPhoto(file=uploaded),
        reply_to=InputReplyToMessage(reply_to_msg_id=TOPIC_ID, top_msg_id=TOPIC_ID),
        random_id=random.randint(-10**18, 10**18), message=''
    ))
    print('SENT PHOTO')

asyncio.run(main())
