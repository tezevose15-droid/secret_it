#!/usr/bin/env python3
import asyncio, json, random, sys
from pathlib import Path
sys.path.insert(0, '/home/comvivat/Desktop/pyatyj-bot/venv/lib/python3.13/site-packages')
from telethon import TelegramClient
from telethon.sessions import SQLiteSession
from telethon.tl.types import InputReplyToMessage
from telethon.tl.functions.messages import SendMessageRequest

CFG = json.loads(Path('/home/comvivat/Desktop/pyatyj-bot/pyatyj-bot/config.json').read_text())
SESS = CFG['session_path']
CHAT_ID = int(sys.argv[1])
TOPIC_ID = int(sys.argv[2])
TEXT = sys.stdin.read()

async def main():
    c = TelegramClient(SQLiteSession(SESS), CFG['telegram_api_id'], CFG['telegram_api_hash'])
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
