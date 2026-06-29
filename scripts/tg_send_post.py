#!/usr/bin/env python3
import asyncio, random, sys
from tg_common import CFG, SESS, API_ID, API_HASH
from telethon import TelegramClient
from telethon.sessions import SQLiteSession
from telethon.tl.types import InputReplyToMessage
from telethon.tl.functions.messages import SendMessageRequest

CHAT_ID = int(sys.argv[1])
TOPIC_ID = int(sys.argv[2])
TEXT = sys.stdin.read()

async def main():
    c = TelegramClient(SQLiteSession(SESS), API_ID, API_HASH)
    await c.connect()
    if not await c.is_user_authorized():
        print('NOT_AUTHORIZED')
        return
    peer = await c.get_input_entity(CHAT_ID)
    updates = await c(SendMessageRequest(
        peer=peer, message=TEXT,
        reply_to=InputReplyToMessage(reply_to_msg_id=TOPIC_ID, top_msg_id=TOPIC_ID),
        random_id=random.randint(-10**18, 10**18),
    ))
    print(f'SENT: updates={updates}')

asyncio.run(main())
