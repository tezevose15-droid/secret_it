#!/usr/bin/env python3
import asyncio, sys
from tg_common import CFG, SESS, API_ID, API_HASH
from telethon import TelegramClient
from telethon.sessions import SQLiteSession

CHAT_ID = int(sys.argv[1])
TEXT = sys.stdin.read()

async def main():
    c = TelegramClient(SQLiteSession(SESS), API_ID, API_HASH)
    await c.connect()
    if not await c.is_user_authorized():
        print('NOT_AUTHORIZED')
        return
    msg = await c.send_message(CHAT_ID, TEXT)
    print(f'SENT: id={msg.id}')

asyncio.run(main())
