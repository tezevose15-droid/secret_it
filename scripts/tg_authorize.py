#!/usr/bin/env python3
"""
Telegram авторизация через Пятого.
Запускаешь → вводишь код из SMS → сессия готова.
Скрипт сам создаст config.json и session файл.
"""

import asyncio, json, os, sys
from telethon import TelegramClient

API_ID = int(os.environ.get("TG_API_ID", 2040))
API_HASH = os.environ.get("TG_API_HASH", "b18441a1ff607e10a989891a5462e627")

async def main():
    print("🤖🦅 Пятый: Подключаю Telegram...")
    phone = input("Введи номер телефона (+380...): ").strip()

    session_path = os.path.expanduser(f"~/tg_session_{phone.replace('+','')}.session")
    client = TelegramClient(session_path, API_ID, API_HASH)

    await client.connect()
    if await client.is_user_authorized():
        print("✅ Уже авторизован!")
        me = await client.get_me()
        print(f"   User: {me.username or me.first_name} (id={me.id})")
    else:
        sent = await client.send_code_request(phone)
        code = input(f"Введи код из Telegram (пришёл на {phone}): ").strip()
        try:
            await client.sign_in(phone, code)
        except Exception as e:
            if "2FA" in str(e) or "password" in str(e):
                pwd = input("Требуется 2FA пароль: ").strip()
                await client.sign_in(password=pwd)
            else:
                print(f"❌ Ошибка: {e}")
                await client.disconnect()
                return

        me = await client.get_me()
        print(f"✅ Авторизован! User: {me.username or me.first_name} (id={me.id})")

    session_string = await client.session.save()
    await client.disconnect()

    # Сохраняем config
    cfg = {
        "telegram_api_id": API_ID,
        "telegram_api_hash": API_HASH,
        "telegram_phone": phone,
        "telegram_2fa_password": "",
        "session_path": session_path
    }
    cfg_path = os.path.expanduser("~/tg_config.json")
    with open(cfg_path, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Конфиг: {cfg_path}")
    print(f"✅ Сессия: {session_path}")
    print("\n🤖🦅 Пятый: Готово. Можешь юзать tg_send_*.py скрипты.")
    print("   Копируй config.json и session файл в ~/Desktop/pyatyj-bot/pyatyj-bot/")

if __name__ == "__main__":
    asyncio.run(main())
