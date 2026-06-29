#!/usr/bin/env python3
"""
Memory Optimizer for Пятый Obsidian Vault
- Сжимает старые сессии
- Дедуплицирует записи
- Обновляет аналитику графа
- Ротирует архивы
"""

import os, json, re, shutil, argparse
from datetime import datetime, timedelta
from collections import defaultdict

VAULT = os.path.expanduser("~/Desktop/Пятый-vault")
SESSIONS_DIR = os.path.join(VAULT, "_rag/sessions")
ARCHIVE_DIR = os.path.join(VAULT, "_rag/archive")
PEOPLE_DIR = os.path.join(VAULT, "Люди")
META_DIR = os.path.join(VAULT, "_meta")
NOW = datetime.now()
REPORT = {"sessions_compressed": 0, "duplicates_removed": 0, "orphans_removed": 0, "errors": []}


def ensure_dirs():
    for d in [SESSIONS_DIR, ARCHIVE_DIR, META_DIR]:
        os.makedirs(d, exist_ok=True)


def compress_old_sessions(days=7):
    """Сжать сессии старше N дней в краткие summary"""
    cutoff = NOW - timedelta(days=days)
    if not os.path.isdir(SESSIONS_DIR):
        return
    for fname in os.listdir(SESSIONS_DIR):
        fpath = os.path.join(SESSIONS_DIR, fname)
        if not fname.endswith(".md"):
            continue
        mtime = datetime.fromtimestamp(os.path.getmtime(fpath))
        if mtime > cutoff:
            continue
        with open(fpath) as f:
            content = f.read()
        summary = extract_summary(content)
        summary_path = os.path.join(ARCHIVE_DIR, fname.replace(".md", "_summary.md"))
        with open(summary_path, "w") as f:
            f.write(f"# Compressed: {fname}\n## Summary\n{summary}\n")
        os.remove(fpath)
        REPORT["sessions_compressed"] += 1


def extract_summary(content):
    """Вытащить summary из markdown или взять первые 500 символов"""
    m = re.search(r"## Summary\s*\n(.+?)(?:\n##|\Z)", content, re.DOTALL)
    if m:
        return m.group(1).strip()[:500]
    return content[:500].strip()


def deduplicate_people():
    """Дедуплицировать записи в Люди/ по содержимому"""
    if not os.path.isdir(PEOPLE_DIR):
        return
    hashes = {}
    for fname in os.listdir(PEOPLE_DIR):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(PEOPLE_DIR, fname)
        with open(fpath) as f:
            content = f.read()
        content_hash = hash(content.strip())
        if content_hash in hashes:
            print(f"  [-] Duplicate: {fname} == {hashes[content_hash]}")
            os.remove(fpath)
            REPORT["duplicates_removed"] += 1
        else:
            hashes[content_hash] = fname


def remove_orphans():
    """Удалить заметки без внутренних ссылок"""
    if not os.path.isdir(PEOPLE_DIR):
        return
    for fname in os.listdir(PEOPLE_DIR):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(PEOPLE_DIR, fname)
        with open(fpath) as f:
            content = f.read()
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        if not links and len(content.strip()) < 200:
            print(f"  [-] Orphan: {fname}")
            shutil.move(fpath, os.path.join(ARCHIVE_DIR, f"orphan_{fname}"))
            REPORT["orphans_removed"] += 1


def update_insights():
    """Обновить _meta/insights.md с базовой статистикой"""
    people_count = 0
    if os.path.isdir(PEOPLE_DIR):
        people_count = len([f for f in os.listdir(PEOPLE_DIR) if f.endswith(".md")])
    
    session_count = 0
    if os.path.isdir(SESSIONS_DIR):
        session_count = len([f for f in os.listdir(SESSIONS_DIR) if f.endswith(".md")])
    
    archive_count = 0
    if os.path.isdir(ARCHIVE_DIR):
        archive_count = len([f for f in os.listdir(ARCHIVE_DIR) if f.endswith(".md")])

    insights = f"""# Insights (auto-generated: {NOW.isoformat()})

## Stats
- People cards: {people_count}
- Active sessions: {session_count}
- Archived sessions: {archive_count}

## Recent Changes
- Compressed: {REPORT['sessions_compressed']} old sessions
- Removed: {REPORT['duplicates_removed']} duplicates, {REPORT['orphans_removed']} orphans
"""
    with open(os.path.join(META_DIR, "insights.md"), "w") as f:
        f.write(insights)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="Run all optimizations")
    parser.add_argument("--compress", action="store_true", help="Compress old sessions")
    parser.add_argument("--dedup", action="store_true", help="Deduplicate people")
    parser.add_argument("--orphans", action="store_true", help="Remove orphan notes")
    parser.add_argument("--report", action="store_true", help="Print report")
    args = parser.parse_args()

    if not any(vars(args).values()):
        args.all = True

    ensure_dirs()

    if args.all or args.compress:
        print("[*] Compressing old sessions...")
        compress_old_sessions()
    if args.all or args.dedup:
        print("[*] Deduplicating people...")
        deduplicate_people()
    if args.all or args.orphans:
        print("[*] Removing orphans...")
        remove_orphans()
    
    update_insights()

    report_path = "/tmp/memory_optimizer_report.json"
    with open(report_path, "w") as f:
        json.dump(REPORT, f, indent=2)
    print(f"\n[+] Report: {report_path}")
    print(json.dumps(REPORT, indent=2))


if __name__ == "__main__":
    main()
