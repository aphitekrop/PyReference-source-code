#!/usr/bin/env python3
import json
from pathlib import Path


ENT_IN = [Path("data/entries.json"), Path("entries.json")]
ART_IN = [Path("data/articles.json"), Path("articles.json")]
ENT_OUT = Path("data/entries.json")
ART_OUT = Path("data/articles.json")


CATEGORY_DEFAULT_RANK = {
    "core": 1500, "builtin": 2000, "file": 2400, "string": 2500, "list": 2600,
    "dict": 2700, "set": 2800, "types": 3000, "operators": 4000, "exceptions": 5000,
    "stdlib": 6000, "python-cli": 7000, "dev-tools": 7500, "packages": 8000, "os": 9000,
}


# (id, name, type, category, summary, syntax, example, tags)
NEW2 = [
    # ---- методы файлов ----
    ("file-read", "file.read()", "method", "file", "Читает содержимое файла.", "file.read(size=-1)", "f.read()", ["read"]),
    ("file-readline", "file.readline()", "method", "file", "Читает одну строку.", "file.readline()", "f.readline()", ["readline"]),
    ("file-readlines", "file.readlines()", "method", "file", "Читает все строки в список.", "file.readlines()", "f.readlines()", ["readlines"]),
    ("file-write", "file.write()", "method", "file", "Записывает строку в файл.", "file.write(s)", "f.write('text')", ["write"]),
    ("file-writelines", "file.writelines()", "method", "file", "Записывает список строк.", "file.writelines(list)", "f.writelines(lines)", ["writelines"]),
    ("file-close", "file.close()", "method", "file", "Закрывает файл.", "file.close()", "f.close()", ["close"]),
    ("file-seek", "file.seek()", "method", "file", "Перемещает курсор чтения.", "file.seek(offset)", "f.seek(0)", ["seek"]),
    ("file-tell", "file.tell()", "method", "file", "Текущая позиция курсора.", "file.tell()", "f.tell()", ["tell"]),
    ("file-flush", "file.flush()", "method", "file", "Сбрасывает буфер в файл.", "file.flush()", "f.flush()", ["flush"]),

    # ---- новые методы строк ----
    ("str-partition", "str.partition()", "method", "string", "Разбивает по разделителю на 3 части.", "str.partition(sep)", "'a=b'.partition('=')", ["partition"]),
    ("str-rpartition", "str.rpartition()", "method", "string", "Разбивает с конца.", "str.rpartition(sep)", "'a=b'.rpartition('=')", ["rpartition"]),
    ("str-splitlines", "str.splitlines()", "method", "string", "Разбивает на строки.", "str.splitlines()", "'a\\nb'.splitlines()", ["splitlines"]),
    ("str-zfill", "str.zfill()", "method", "string", "Заполняет нулями слева.", "str.zfill(width)", "'5'.zfill(3)", ["zfill"]),
    ("str-ljust", "str.ljust()", "method", "string", "Выравнивает по левому краю.", "str.ljust(width)", "'x'.ljust(5)", ["ljust"]),
    ("str-rjust", "str.rjust()", "method", "string", "Выравнивает по правому краю.", "str.rjust(width)", "'x'.rjust(5)", ["rjust"]),
    ("str-center", "str.center()", "method", "string", "Центрирует строку.", "str.center(width)", "'x'.center(5)", ["center"]),
    ("str-swapcase", "str.swapcase()", "method", "string", "Меняет регистр на противоположный.", "str.swapcase()", "'AbC'.swapcase()", ["swapcase"]),
    ("str-casefold", "str.casefold()", "method", "string", "Агрессивное приведение к нижнему регистру.", "str.casefold()", "'Straße'.casefold()", ["casefold"]),
    ("str-isalpha", "str.isalpha()", "method", "string", "Только буквы?", "str.isalpha()", "'abc'.isalpha()", ["isalpha"]),
    ("str-isalnum", "str.isalnum()", "method", "string", "Буквы и цифры?", "str.isalnum()", "'a1'.isalnum()", ["isalnum"]),
    ("str-isspace", "str.isspace()", "method", "string", "Только пробелы?", "str.isspace()", "' '.isspace()", ["isspace"]),
    ("str-lstrip", "str.lstrip()", "method", "string", "Убирает пробелы слева.", "str.lstrip()", "' x'.lstrip()", ["lstrip"]),
    ("str-rstrip", "str.rstrip()", "method", "string", "Убирает пробелы справа.", "str.rstrip()", "'x '.rstrip()", ["rstrip"]),
    ("str-rfind", "str.rfind()", "method", "string", "Ищет подстроку с конца.", "str.rfind(sub)", "'ab'.rfind('b')", ["rfind"]),
    ("str-index", "str.index()", "method", "string", "Индекс подстроки (ошибка если нет).", "str.index(sub)", "'abc'.index('b')", ["index"]),
    ("str-encode", "str.encode()", "method", "string", "Кодирует строку в байты.", "str.encode(encoding)", "'пр'.encode('utf-8')", ["encode"]),

    # ---- int / float / bytes ----
    ("int-bit-length", "int.bit_length()", "method", "types", "Число битов для представления.", "int.bit_length()", "(10).bit_length()", ["bit_length"]),
    ("int-to-bytes", "int.to_bytes()", "method", "types", "Число в байты.", "int.to_bytes(length, byteorder)", "(255).to_bytes(2, 'big')", ["to_bytes"]),
    ("int-from-bytes", "int.from_bytes()", "method", "types", "Байты в число.", "int.from_bytes(bytes, byteorder)", "int.from_bytes(b'\\xff', 'big')", ["from_bytes"]),
    ("float-is-integer", "float.is_integer()", "method", "types", "Целое ли float-число.", "float.is_integer()", "(2.0).is_integer()", ["is_integer"]),
    ("bytes-decode", "bytes.decode()", "method", "types", "Декодирует байты в строку.", "bytes.decode(encoding)", "b'ab'.decode('utf-8')", ["decode"]),

    # ---- слияние словарей ----
    ("dict-merge", "dict | dict", "syntax", "dict", "Объединение словарей (Python 3.9+).", "a | b", "{'a': 1} | {'b': 2}", ["merge"]),
    ("dict-update-merge", "dict |= other", "syntax", "dict", "Обновление словаря на месте.", "a |= b", "data |= {'b': 2}", ["merge"]),

    # ---- match-паттерны ----
    ("match-capture", "case x", "syntax", "core", "Захват значения в переменную.", "case x:", "case value:", ["match"]),
    ("match-literal", "case 'value'", "syntax", "core", "Сопоставление с литералом.", "case 'quit':", "case 'quit':", ["match"]),
    ("match-sequence", "case [a, b]", "syntax", "core", "Сопоставление последовательности.", "case [a, b]:", "case [x, y]:", ["match"]),
    ("match-mapping", "case {'k': v}", "syntax", "core", "Сопоставление словаря.", "case {'key': v}:", "case {'user': u}:", ["match"]),
    ("match-class", "case Point(x, y)", "syntax", "core", "Сопоставление класса.", "case Cls(attr):", "case Point(x=0):", ["match"]),
    ("match-guard", "case n if n > 0", "syntax", "core", "Условие-страж в case.", "case p if cond:", "case n if n > 0:", ["match"]),
    ("match-wildcard", "case _", "syntax", "core", "Универсальный шаблон.", "case _:", "case _:", ["match"]),
    ("match-or", "case 1 | 2", "syntax", "core", "Несколько вариантов.", "case a | b:", "case 404 | 500:", ["match"]),

    # ---- отладка и прочее ----
    ("breakpoint", "breakpoint()", "builtin-function", "builtin", "Точка останова для отладчика.", "breakpoint()", "breakpoint()", ["debug"]),
    ("ascii", "ascii()", "builtin-function", "builtin", "Строка с экранированием не-ASCII.", "ascii(obj)", "ascii('пр')", ["ascii"]),
]


RELATED2 = {
    "file-read": {"alternatives": ["file-readlines", "file-readline"], "complements": ["open", "with"], "seealso": ["open"]},
    "file-write": {"alternatives": ["file-writelines"], "complements": ["open", "with", "file-flush"], "seealso": ["open"]},
    "file-close": {"alternatives": ["with"], "complements": ["open"], "seealso": ["with"]},
    "str-partition": {"alternatives": ["str-split", "str-rpartition"], "complements": ["str"], "seealso": ["str-split"]},
    "str-splitlines": {"alternatives": ["str-split"], "complements": ["str"], "seealso": ["str-split"]},
    "str-index": {"alternatives": ["str-find", "str-rfind"], "complements": ["str"], "seealso": ["str-find"]},
    "str-encode": {"alternatives": ["bytes"], "complements": ["bytes-decode"], "seealso": ["bytes"]},
    "bytes-decode": {"alternatives": ["str"], "complements": ["str-encode"], "seealso": ["str-encode"]},
    "int-bit-length": {"alternatives": ["bin"], "complements": ["int"], "seealso": ["bin"]},
    "int-to-bytes": {"alternatives": ["bytes"], "complements": ["int-from-bytes"], "seealso": ["int-from-bytes"]},
    "int-from-bytes": {"alternatives": ["int"], "complements": ["int-to-bytes"], "seealso": ["int-to-bytes"]},
    "dict-merge": {"alternatives": ["dict-update", "dict-update-merge"], "complements": ["dict"], "seealso": ["dict-update"]},
    "dict-update-merge": {"alternatives": ["dict-merge", "dict-update"], "complements": ["dict"], "seealso": ["dict-merge"]},
    "match-capture": {"alternatives": [], "complements": ["match", "case"], "seealso": ["match"]},
    "match-literal": {"alternatives": ["match"], "complements": ["match"], "seealso": ["match"]},
    "match-sequence": {"alternatives": [], "complements": ["match", "list"], "seealso": ["match"]},
    "match-mapping": {"alternatives": [], "complements": ["match", "dict"], "seealso": ["match"]},
    "match-guard": {"alternatives": ["if"], "complements": ["match"], "seealso": ["match", "if"]},
    "match-wildcard": {"alternatives": ["else"], "complements": ["match"], "seealso": ["match"]},
    "match-or": {"alternatives": ["or"], "complements": ["match"], "seealso": ["match"]},
    "breakpoint": {"alternatives": ["pdb"], "complements": ["pdb"], "seealso": ["pdb"]},
}


CATEGORY_ALT2 = {
    "file": ["open", "pathlib", "with"],
}


# article_id -> [entry_id, ...]
ARTICLES_MAP = {
    "venv": ["python-m-venv", "python", "pip"],
    "install-library": ["pip", "pip-install", "requests"],
    "save-dependencies": ["pip-freeze", "pip-install", "pip"],
    "run-server": ["python-m-http-server", "flask", "fastapi"],
    "download-file": ["curl", "wget", "requests", "urllib-request"],
    "handle-error": ["try", "except", "finally", "raise", "ValueError", "FileNotFoundError", "ZeroDivisionError"],
    "read-json": ["json", "requests", "open", "file-read"],
    "write-csv": ["csv", "open", "dict", "file-write"],
    "create-project": ["python", "python-m-venv", "pip-install"],
    "install-flask": ["flask", "pip-install"],
    "install-fastapi": ["fastapi", "pip-install"],
    "github": ["git", "git-init", "git-clone", "git-push"],
    "git-commit": ["git", "git-add", "git-status", "git-push"],
    "http-request": ["requests", "curl", "urllib-request", "httpx"],
    "telegram-bot": ["python-telegram-bot", "aiogram"],
    "sqlite": ["sqlite3"],
    "logging": ["logging", "try", "except"],
    "tests": ["pytest", "assert"],
}


def related_key(item):
    if isinstance(item, str):
        return f"id:{item}"
    if isinstance(item, dict):
        if item.get("id"):
            return f"id:{item['id']}"
        return f"name:{item.get('name', '')}|{item.get('syntax', '')}"
    return f"raw:{item}"


def merge_list(existing, extra, ids):
    existing = list(existing or [])
    keys = {related_key(i) for i in existing}
    for item in extra:
        if isinstance(item, str) and item not in ids:
            continue
        k = related_key(item)
        if k not in keys:
            existing.append(item)
            keys.add(k)
    return existing


def default_returns(t):
    return {
        "method": "Зависит от метода.",
        "syntax": "Зависит от выражения.",
        "builtin-function": "Зависит от функции.",
    }.get(t, "")


def make_entry(item):
    eid, name, etype, category, summary, syntax, example, tags = item
    return {
        "id": eid, "name": name, "type": etype, "category": category,
        "summary": summary, "syntax": syntax, "params": [],
        "returns": default_returns(etype), "errors": [], "example": example,
        "version": {"since": None, "deprecated": None, "removed": None, "checked": "3.13"},
        "tags": tags, "links": [], "articles": [],
        "related": {"alternatives": [], "complements": [], "seealso": []},
    }


def load(path_list):
    for p in path_list:
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    return None


def main():
    ent = load(ENT_IN)
    art = load(ART_IN)

    if ent is None:
        print("Сначала запусти build_entries.py")
        return

    if isinstance(ent, list):
        ent = {"meta": {}, "entries": ent}
    if art is None:
        art = {"meta": {}, "articles": []}
    if isinstance(art, list):
        art = {"meta": {}, "articles": art}

    entries = ent.get("entries", [])
    by_id = {e["id"]: e for e in entries if "id" in e}

    for item in NEW2:
        e = make_entry(item)
        if e["id"] not in by_id:
            by_id[e["id"]] = e

    ids = set(by_id)

    for e in by_id.values():
        rel = e.setdefault("related", {"alternatives": [], "complements": [], "seealso": []})

        extra = RELATED2.get(e["id"])
        if extra:
            for k in ["alternatives", "complements", "seealso"]:
                rel[k] = merge_list(rel.get(k, []), extra.get(k, []), ids)

        if e.get("type") == "method" and e.get("category") in CATEGORY_ALT2:
            pool = CATEGORY_ALT2[e["category"]]
            rel["alternatives"] = merge_list(rel.get("alternatives", []), pool, ids)
            rel["complements"] = merge_list(rel.get("complements", []), ["open", "with"], ids)
            rel["seealso"] = merge_list(rel.get("seealso", []), ["open"], ids)

        if e.get("category") == "core" and e["id"].startswith("match-"):
            rel["complements"] = merge_list(rel.get("complements", []), ["match", "case"], ids)
            rel["seealso"] = merge_list(rel.get("seealso", []), ["match"], ids)

    # ---- перекрёстные ссылки ----
    articles = art.get("articles", [])
    art_by_id = {a["id"]: a for a in articles if "id" in a}

    for art_id, entry_ids in ARTICLES_MAP.items():
        article = art_by_id.get(art_id)
        if not article:
            continue

        existing = article.setdefault("entries", [])
        for eid in entry_ids:
            if eid not in existing:
                existing.append(eid)

            entry = by_id.get(eid)
            if entry:
                alist = entry.setdefault("articles", [])
                if art_id not in alist:
                    alist.append(art_id)

    # ---- финализация ----
    prepared = []
    for e in by_id.values():
        e["related"]["alternatives"] = e["related"]["alternatives"][:3]
        e["rank"] = e.get("rank", CATEGORY_DEFAULT_RANK.get(e.get("category"), 10000))
        prepared.append(e)

    prepared.sort(key=lambda x: (x.get("rank", 10000), x.get("name", "").lower()))
    ent["entries"] = prepared

    ENT_OUT.parent.mkdir(parents=True, exist_ok=True)
    ENT_OUT.write_text(json.dumps(ent, ensure_ascii=False, indent=2), encoding="utf-8")

    ART_OUT.parent.mkdir(parents=True, exist_ok=True)
    ART_OUT.write_text(json.dumps(art, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Saved {len(prepared)} entries and {len(articles)} articles")


if __name__ == "__main__":
    main()