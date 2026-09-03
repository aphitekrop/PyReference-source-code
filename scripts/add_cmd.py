#!/usr/bin/env python3
import json
from pathlib import Path

INPUT_PATHS = [Path("data/entries.json"), Path("entries.json")]
OUTPUT_PATH = Path("data/entries.json")

NEW_CMD = [
    ("chcp", "chcp", "os-command", "os", "Показывает или меняет кодовую страницу Windows.", "chcp [page]", "chcp 65001", ["cmd", "windows", "кодировка"]),
    ("setx", "setx", "os-command", "os", "Создаёт или меняет переменные окружения Windows.", "setx var value", "setx PATH \"%PATH%;C:\\bin\"", ["cmd", "windows", "env"]),
    ("robocopy", "robocopy", "os-command", "os", "Надёжное копирование файлов и папок в Windows.", "robocopy src dst", "robocopy C:\\src D:\\dst /E", ["cmd", "windows", "копирование"]),
    ("xcopy", "xcopy", "os-command", "os", "Копирование файлов и деревьев папок в Windows.", "xcopy src dst", "xcopy C:\\src D:\\dst /E", ["cmd", "windows", "копирование"]),
    ("sfc", "sfc", "os-command", "os", "Проверка и восстановление системных файлов Windows.", "sfc /scannow", "sfc /scannow", ["cmd", "windows", "система"]),
    ("dism", "dism", "os-command", "os", "Управление образами Windows.", "dism /online /cleanup-image", "dism /online /cleanup-image /restorehealth", ["cmd", "windows", "система"]),
    ("chkdsk", "chkdsk", "os-command", "os", "Проверка диска на ошибки.", "chkdsk [drive]", "chkdsk C: /f", ["cmd", "windows", "диск"]),
    ("tasklist", "tasklist", "os-command", "os", "Список запущенных процессов Windows.", "tasklist", "tasklist /FI \"IMAGENAME eq python.exe\"", ["cmd", "windows", "процессы"]),
    ("taskkill", "taskkill", "os-command", "os", "Завершение процессов Windows.", "taskkill /PID id", "taskkill /IM python.exe /F", ["cmd", "windows", "процессы"]),
    ("tracert", "tracert", "os-command", "os", "Трассировка маршрута Windows.", "tracert host", "tracert example.com", ["cmd", "windows", "сеть"]),
    ("traceroute", "traceroute", "os-command", "os", "Трассировка маршрута Unix.", "traceroute host", "traceroute example.com", ["bash", "unix", "сеть"]),
    ("netstat", "netstat", "os-command", "os", "Сетевые подключения и порты.", "netstat -an", "netstat -ano | findstr 8000", ["cmd", "сеть", "порты"]),
    ("nslookup", "nslookup", "os-command", "os", "Запрос DNS-записей.", "nslookup host", "nslookup example.com", ["cmd", "dns", "сеть"]),
    ("systemctl", "systemctl", "os-command", "os", "Управление службами systemd.", "systemctl cmd unit", "systemctl restart nginx", ["bash", "linux", "службы"]),
    ("journalctl", "journalctl", "os-command", "os", "Просмотр логов systemd.", "journalctl -u unit", "journalctl -u nginx -f", ["bash", "linux", "логи"]),
    ("apt", "apt", "os-command", "os", "Пакетный менеджер Debian/Ubuntu.", "apt cmd pkg", "sudo apt update && sudo apt install git", ["bash", "linux", "пакеты"]),
    ("chown", "chown", "os-command", "os", "Меняет владельца файла.", "chown user:group file", "chown root:root /etc/passwd", ["bash", "unix", "права"]),
    ("chmod", "chmod", "os-command", "os", "Меняет права доступа.", "chmod mode file", "chmod +x script.sh", ["bash", "unix", "права"]),
    ("tar", "tar", "os-command", "os", "Архиватор tar.", "tar -czf a.tgz d", "tar -xzf archive.tar.gz", ["bash", "unix", "архивы"]),
    ("zip", "zip", "os-command", "os", "Создание ZIP-архивов.", "zip a.zip file", "zip -r archive.zip folder/", ["bash", "unix", "архивы"]),
    ("unzip", "unzip", "os-command", "os", "Распаковка ZIP-архивов.", "unzip a.zip", "unzip archive.zip -d out/", ["bash", "unix", "архивы"]),
    ("ssh", "ssh", "os-command", "os", "Удалённое подключение по SSH.", "ssh user@host", "ssh root@192.168.1.10", ["bash", "сеть", "ssh"]),
    ("scp", "scp", "os-command", "os", "Копирование файлов по SSH.", "scp src dst", "scp file.txt user@host:~/", ["bash", "сеть", "ssh"]),
    ("node", "node", "os-command", "dev-tools", "Запуск Node.js.", "node script.js", "node app.js", ["node", "js"]),
    ("npm", "npm", "os-command", "dev-tools", "Пакетный менеджер Node.js.", "npm cmd", "npm install express", ["node", "js", "пакеты"]),
]

def make_entry(item):
    eid, name, etype, category, summary, syntax, example, tags = item
    return {
        "id": eid, "name": name, "type": etype, "category": category,
        "summary": summary, "syntax": syntax, "params": [],
        "returns": "Текстовый вывод или код завершения.", "errors": [], "example": example,
        "version": {"since": None, "deprecated": None, "removed": None, "checked": None},
        "tags": tags, "links": [], "articles": [],
        "related": {"alternatives": [], "complements": [], "seealso": []},
        "rank": 9000,
    }

def main():
    payload = None
    for path in INPUT_PATHS:
        if path.exists():
            payload = json.loads(path.read_text(encoding="utf-8"))
            break

    if payload is None:
        print("Сначала запусти build_all.py")
        return

    if isinstance(payload, list):
        payload = {"meta": {}, "entries": payload}

    entries = payload.get("entries", [])
    by_id = {e["id"]: e for e in entries if "id" in e}

    added = 0
    for item in NEW_CMD:
        e = make_entry(item)
        if e["id"] not in by_id:
            by_id[e["id"]] = e
            added += 1

    prepared = list(by_id.values())
    prepared.sort(key=lambda x: (x.get("rank", 10000), x.get("name", "").lower()))
    payload["entries"] = prepared

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Added {added} CMD commands. Total: {len(prepared)}")

if __name__ == "__main__":
    main()