#!/usr/bin/env python3
import asyncio, json, sys, random
from pathlib import Path
sys.path.insert(0, '/home/comvivat/Desktop/pyatyj-bot/venv/lib/python3.13/site-packages')
from telethon import TelegramClient
from telethon.sessions import SQLiteSession

CFG = json.loads(Path('/home/comvivat/Desktop/pyatyj-bot/pyatyj-bot/config.json').read_text())
SESS = CFG['session_path']
CHAT_ID = int(sys.argv[1])
TEXT = sys.stdin.read()

async def main():
    c = TelegramClient(SQLiteSession(SESS), CFG['telegram_api_id'], CFG['telegram_api_hash'])
    await c.connect()
    if not await c.is_user_authorized():
        print('NOT_AUTHORIZED')
        return
    msg = await c.send_message(CHAT_ID, TEXT)
    print(f'SENT: id={msg.id}')

asyncio.run(main())
