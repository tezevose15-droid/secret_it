#!/usr/bin/env python3
import os, sys, json
from pathlib import Path

CFG_PATH = Path(os.path.expanduser("~/tg_config.json"))
if not CFG_PATH.exists():
    print(f"NOT_AUTHORIZED: {CFG_PATH} not found — run tg_authorize.py first")
    sys.exit(1)

CFG = json.loads(CFG_PATH.read_text())
SESS = CFG.get("session_path", "")

API_ID = CFG["telegram_api_id"]
API_HASH = CFG["telegram_api_hash"]

# don't hardcode venv path — try system telethon first
try:
    from telethon import TelegramClient
    from telethon.sessions import SQLiteSession
except ImportError:
    # fallback: scan common venv locations
    for p in [
        os.path.expanduser("~/.local/share/virtualenvs/*/lib/python*/site-packages"),
        os.path.expanduser("~/venv/*/lib/python*/site-packages"),
    ]:
        from glob import glob
        matches = glob(p)
        if matches:
            sys.path.insert(0, matches[0])
            break
    from telethon import TelegramClient
    from telethon.sessions import SQLiteSession
