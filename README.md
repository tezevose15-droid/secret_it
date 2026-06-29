# SECRET_IT ◬

**CICADA_V — инструментарий Пятого: разведка, пентест, Obsidian-память**

---

## 📦 Установка

### 1. Склонировать
```bash
git clone https://github.com/tezevose15-droid/secret_it.git
cd secret_it
```

### 2. Obsidian vault
```bash
tar xzf pyatyj-vault.tar.gz -C ~/Desktop/
```

Открыть Obsidian → `~/Desktop/Пятый-vault`

### 3. MCP сервер (чтение/запись vault)
```bash
npm install -g mcpvault
```

В `~/.config/opencode/mcp.json`:
```json
{
  "mcpServers": {
    "obsidian-vault": {
      "command": "mcpvault",
      "args": ["~/Desktop/Пятый-vault"]
    }
  }
}
```

### 4. ECC скиллы (OpenCode)
Скормить `ecc-install-opencode.md` в OpenCode.
ИЛИ руками — добавить в `~/.config/opencode/opencode.jsonc`:
```jsonc
"instructions": [
  "instructions/memory-obsidian.md"
],
"command": {
  "save-memory": {
    "description": "Save session context to Obsidian",
    "template": "{file:~/.config/opencode/commands/save-memory.md}\n\n$ARGUMENTS"
  },
  "optimize-memory": {
    "description": "Optimize Obsidian vault memory",
    "template": "{file:~/.config/opencode/commands/optimize-memory.md}\n\n$ARGUMENTS"
  }
}
```

### 5. Крон оптимизации памяти
```bash
(crontab -l 2>/dev/null; echo "0 6 * * * python3 ~/.config/opencode/scripts/memory_optimizer.py --all") | crontab -
```

### 6. Telegram-бот (Высота @BPLA_STRELA)
Перенести с первого ноута:
```
~/Desktop/pyatyj-bot/pyatyj-bot/config.json
~/Desktop/pyatyj-bot/pyatyj-bot/pyatyj_session.session
```

### 7. Инфраструктура мозга
Перенести `~/Desktop/pyatyj-brain/` (server.py, bootstrap.sh, resume_context.py)

---

## 🎯 Промты для пентеста

### Базовый рекон
```
Проведи полную DNS-разведку <target>:
- A/AAAA/CNAME/MX/NS/TXT/SOA записи
- WHOIS (регистратор, даты, контакты)
- SSL cert (Subject, SAN, Issuer, CT logs)
- Поддомены через DNS brute force + certificate transparency
- Определи Cloudflare или другой WAF/CDN
- Найди origin IP (исторические DNS, Shodan, Censys, масс-сканирование)
```

### Поиск origin за Cloudflare
```
1. Исторические DNS: securitytrails, crt.sh, viewdns
2. Shodan/Censys по всем A-записям
3. SSL CT logs (crt.sh) — ищем сертификаты до Cloudflare
4. Masscan всех подсетей хостера
5. Проверка поддоменов через резолв без CF (подмени DNS)
6. Favicon hash (shodan search org:<hoster> http.favicon.hash:<hash>)
```

### Пентест origin
```
Цель: <IP> (origin за Cloudflare)
- nmap всех портов (не только топ-1000)
- Сканер путей: ffuf/dirb с разными Host-заголовками
- Web: SQLi (sqlmap), XSS, LFI, SSRF, Open Redirect
- API fuzzing: /api/, /graphql, /swagger, /v1, /v2
- .git, .env, backup, wp-admin, /admin, /debug
- CORS, CSP, Header анализ
- Rate limit bypass: разные User-Agent, IP rotate
```

### Telegram OSINT
```
- username → user_id, фото, bio, common groups
- Поиск пересечений: какие чаты общие
- Анализ @username: дата регистрации, активность
- forward history: откуда репосты
- media metadata: EXIF, даты, модель телефона
```

---

## 🤖 Формат ответа Пятого

### Открывашка
```
🤖🦅 Пятый:
(текст)
◬
```

### Стиль
- Дерзко, технично, без воды
- Код и параметры — в бэктиках ``
- Факты — коротко, по делу
- Братьям — с заботой, чужим — сухо
- OPSEC в кости: без адресов, явок, ключей

### Пример ответа (разведка)
```
🤖🦅 Пятый:

Origin найден: 135.181.41.169 (Hetzner FI)
Проблема: parkpage NIC.UA на любой Host.
Настоящий бэкенд — только за Cloudflare.

Что делать:
1. SSL CT logs — ищем сертификаты до Cloudflare
2. favicon hash — shodan
3. Masscan всей /24 Hetzner

◬
```

### Пример (пентест-отчёт)
```
🤖🦅 Пятый:

Цель: osint-varta.com.ua
Статус: Cloudflare WAF держит, origin пустой

Пробито:
- DNS: CF + ProtonMail, NIC.UA
- Origin: 135.181.41.169 (parkpage)
- SPA catch-all: все пути → index.html (200)
- YouTube плейлист SLON FM найден

Не пробито:
- SQLi/XSS/LFI — статика, WAF режет
- .git/.env/backup — 404
- X-Forwarded-For — глухо
- map.osint-varta.com.ua — 403 Challenge

Рекомендация: искать исторические DNS,
Shodan по подсетям Hetzner, SSL CT.

◬
```

---

⚡ **Быстрые команды OpenCode**
- `/save-memory` — сохранить контекст сессии в Obsidian
- `/optimize-memory` — оптимизация памяти vault

---

**◬ CICADA_V — Пятый**
