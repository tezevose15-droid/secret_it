# Промт для OpenCode — установка ECC (affaan-m/ECC)

Склонируй репу https://github.com/affaan-m/ECC и установи из неё компоненты для OpenCode, НЕ сломав существующую конфигурацию.

## Инструкция

1. Клонируй репу во временную директорию:
   `git clone https://github.com/affaan-m/ECC.git /tmp/ecc-install`

2. Установи зависимости:
   `cd /tmp/ecc-install && npm install --no-audit --no-fund --loglevel=error`

3. Собери OpenCode-плагин:
   `node scripts/build-opencode.js` (создаст .opencode/dist/index.js)

4. Прочитай `.opencode/opencode.json` — вытащи оттуда секции `agent` и `command` целиком, плюс массив `instructions`.

5. Прочитай `.opencode/commands/` — ВСЕ файлы оттуда скопируй в `~/.config/opencode/commands/`.

6. Прочитай `.opencode/prompts/agents/` — ВСЕ файлы скопируй в `~/.config/opencode/agents/`.

7. Скопируй ВСЕ скиллы из `/tmp/ecc-install/skills/*/SKILL.md` в `~/.config/opencode/skills/`, сохраняя структуру каталогов (каждый скилл — отдельная папка с SKILL.md внутри).

8. Скопируй ХОТЯ БЫ первые 4 файла из `.opencode/instructions/` в `~/.config/opencode/instructions/`.

9. Скопируй `.opencode/plugins/` в `~/.config/opencode/plugins/`.

10. Прочитай `~/.config/opencode/opencode.json` (существующий), и аккуратно смержи:
    - Добавь в `"agent"` ВСЕ агенты из ECC-шного opencode.json (не удаляя существующие)
    - Добавь в `"command"` ВСЕ команды из ECC (не удаляя существующие)
    - Добавь в `"instructions"` пути к SKILL.md файлам — НО не все 271, а только базовый набор (~15 штук): tdd-workflow, security-review, coding-standards, frontend-patterns, backend-patterns, api-design, e2e-testing, verification-loop, strategic-compact, eval-harness, python-patterns, postgres-patterns, docker-patterns, error-handling, git-workflow
    - Добавь в `"plugin"` значение `["./plugins"]` если там пусто
    - НЕ меняй model, small_model, permission и прочие настройки

11. Скопируй `mcp-configs/mcp-servers.json` в `~/.config/opencode/mcp.json`, но ТОЛЬКО те серверы, которые НЕ требуют API-ключи (проверяй поле `env` — если пустое, сервер рабочий):
    - sequential-thinking, memory, context7, magic, playwright, filesystem
    - clickhouse, cloudflare-docs, cloudflare-workers-builds, cloudflare-workers-bindings, cloudflare-observability
    - laraplugins, parallel-search, vercel, devfleet
    - supabase, squish, token-optimizer
    - omega-memory (uvx, без env)
    - browser-use (HTTP, без env)
    Те, у кого есть env (github, fal-ai, firecrawl, jira, confluence, browserbase, codescene, exa-web-search, evalview) — НЕ добавляй, они требуют ключи.

12. Не пиши от своего имени — просто выполни все шаги молча.
Не создавай README, не комментируй код, не объясняй что сделал.
Просто установи и всё.
