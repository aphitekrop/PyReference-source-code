#!/usr/bin/env python3
import json
from pathlib import Path

INPUT_PATHS = [Path("data/entries.json"), Path("entries.json")]
OUTPUT_PATH = Path("data/entries.json")

CATEGORY_DEFAULT_RANK = {
    "core": 1500, "builtin": 2000, "file": 2400, "string": 2500, "list": 2600,
    "dict": 2700, "set": 2800, "tuple": 2850, "bytes": 2900, "types": 3000,
    "re": 3100, "pathlib": 3150, "datetime": 3200, "time": 3250, "calendar": 3300,
    "itertools": 3400, "collections": 3450, "functools": 3500, "operator": 3550,
    "bisect": 3600, "heapq": 3650, "copy": 3700, "pprint": 3750,
    "warnings": 3800, "contextlib": 3850, "enum": 3900, "logging": 3950,
    "unittest": 4000, "argparse": 4050, "configparser": 4100,
    "zipfile": 4150, "tarfile": 4200, "gzip": 4250, "bz2": 4300, "lzma": 4350, "zlib": 4400,
    "base64": 4450, "hashlib": 4500, "hmac": 4550, "secrets": 4600, "random": 4650,
    "statistics": 4700, "decimal": 4750, "fractions": 4800, "cmath": 4850,
    "struct": 4900, "array": 4950, "weakref": 5000, "types": 5050,
    "inspect": 5100, "ast": 5150, "dis": 5200, "pdb": 5250, "timeit": 5300,
    "profile": 5350, "sysconfig": 5400, "platform": 5450, "locale": 5500,
    "gettext": 5550, "codecs": 5600, "unicodedata": 5650, "difflib": 5700,
    "textwrap": 5750, "string": 5800, "glob": 5850, "fnmatch": 5900,
    "linecache": 5950, "tokenize": 6000, "keyword": 6050, "io": 6100,
    "signal": 6150, "mmap": 6200, "ctypes": 6250,
    "multiprocessing": 6300, "threading": 6350, "concurrent": 6400,
    "asyncio": 6450, "selectors": 6500, "queue": 6550, "sched": 6600,
    "atexit": 6650, "gc": 6700, "tracemalloc": 6750, "faulthandler": 6800,
    "webbrowser": 6850, "socket": 6900, "ssl": 6950, "urllib": 7000,
    "http-server": 7050, "http-client": 7100, "http-cookies": 7150,
    "html-parser": 7200, "xml": 7250, "email": 7300, "mailbox": 7350,
    "mimetypes": 7400, "ftplib": 7450, "poplib": 7500, "imaplib": 7550,
    "smtplib": 7600, "uuid": 7650, "socketserver": 7700, "xmlrpc": 7750,
    "wsgiref": 7800, "cmd": 7850, "shlex": 7900, "filecmp": 7950, "stat": 8000,
    "pickle": 8050, "shelve": 8100, "marshal": 8150, "dbm": 8200,
    "sqlite3": 8250, "csv": 8300, "json": 8350, "tomllib": 8400, "plistlib": 8450,
    "special": 3500, "operators": 4000, "exceptions": 5000,
    "stdlib": 6000, "python-cli": 7000, "dev-tools": 7500, "packages": 8000, "os": 9000,
}

# (id, name, type, category, summary, syntax, example, tags)
NEW4 = [
    # ---- tuple ----
    ("tuple-count", "tuple.count()", "method", "tuple", "Считает вхождения значения.", "t.count(x)", "t.count(1)", ["tuple", "count"]),
    ("tuple-index", "tuple.index()", "method", "tuple", "Индекс первого вхождения.", "t.index(x)", "t.index(1)", ["tuple", "index"]),

    # ---- frozenset ----
    ("frozenset-union", "frozenset.union()", "method", "set", "Объединение.", "fs.union(other)", "fs | t", ["frozenset"]),
    ("frozenset-intersection", "frozenset.intersection()", "method", "set", "Пересечение.", "fs.intersection(other)", "fs & t", ["frozenset"]),
    ("frozenset-difference", "frozenset.difference()", "method", "set", "Разность.", "fs.difference(other)", "fs - t", ["frozenset"]),
    ("frozenset-symmetric-difference", "frozenset.symmetric_difference()", "method", "set", "Симметрическая разность.", "fs.symmetric_difference(other)", "fs ^ t", ["frozenset"]),
    ("frozenset-issubset", "frozenset.issubset()", "method", "set", "Подмножество?", "fs.issubset(other)", "fs <= t", ["frozenset"]),
    ("frozenset-issuperset", "frozenset.issuperset()", "method", "set", "Надмножество?", "fs.issuperset(other)", "fs >= t", ["frozenset"]),
    ("frozenset-isdisjoint", "frozenset.isdisjoint()", "method", "set", "Нет общих элементов?", "fs.isdisjoint(other)", "fs.isdisjoint(t)", ["frozenset"]),

    # ---- bytes ----
    ("bytes-count", "bytes.count()", "method", "bytes", "Считает байты.", "b.count(x)", "b'aaa'.count(b'a')", ["bytes"]),
    ("bytes-find", "bytes.find()", "method", "bytes", "Ищет байты.", "b.find(sub)", "b'abc'.find(b'b')", ["bytes"]),
    ("bytes-rfind", "bytes.rfind()", "method", "bytes", "Ищет с конца.", "b.rfind(sub)", "b.rfind(b'b')", ["bytes"]),
    ("bytes-index", "bytes.index()", "method", "bytes", "Индекс (ошибка если нет).", "b.index(sub)", "b'abc'.index(b'b')", ["bytes"]),
    ("bytes-split", "bytes.split()", "method", "bytes", "Разбивает байты.", "b.split(sep)", "b'a,b'.split(b',')", ["bytes"]),
    ("bytes-join", "bytes.join()", "method", "bytes", "Собирает байты.", "sep.join(iter)", "b','.join([b'a', b'b'])", ["bytes"]),
    ("bytes-replace", "bytes.replace()", "method", "bytes", "Заменяет байты.", "b.replace(old, new)", "b.replace(b'a', b'b')", ["bytes"]),
    ("bytes-startswith", "bytes.startswith()", "method", "bytes", "Начинается с?", "b.startswith(prefix)", "b.startswith(b'ab')", ["bytes"]),
    ("bytes-endswith", "bytes.endswith()", "method", "bytes", "Заканчивается на?", "b.endswith(suffix)", "b.endswith(b'bc')", ["bytes"]),
    ("bytes-strip", "bytes.strip()", "method", "bytes", "Убирает байты по краям.", "b.strip()", "b' x '.strip()", ["bytes"]),
    ("bytes-upper", "bytes.upper()", "method", "bytes", "В верхний регистр.", "b.upper()", "b'abc'.upper()", ["bytes"]),
    ("bytes-lower", "bytes.lower()", "method", "bytes", "В нижний регистр.", "b.lower()", "b'ABC'.lower()", ["bytes"]),
    ("bytes-translate", "bytes.translate()", "method", "bytes", "Применяет таблицу.", "b.translate(table)", "b.translate(table)", ["bytes"]),
    ("bytes-removeprefix", "bytes.removeprefix()", "method", "bytes", "Убирает префикс.", "b.removeprefix(p)", "b.removeprefix(b'a')", ["bytes"]),
    ("bytes-removesuffix", "bytes.removesuffix()", "method", "bytes", "Убирает суффикс.", "b.removesuffix(s)", "b.removesuffix(b'c')", ["bytes"]),
    ("bytearray-insert", "bytearray.insert()", "method", "bytes", "Вставляет байт.", "ba.insert(i, x)", "ba.insert(0, 65)", ["bytearray"]),
    ("bytearray-pop", "bytearray.pop()", "method", "bytes", "Удаляет и возвращает.", "ba.pop()", "ba.pop()", ["bytearray"]),
    ("bytearray-remove", "bytearray.remove()", "method", "bytes", "Удаляет первый.", "ba.remove(x)", "ba.remove(65)", ["bytearray"]),
    ("bytearray-reverse", "bytearray.reverse()", "method", "bytes", "Разворачивает.", "ba.reverse()", "ba.reverse()", ["bytearray"]),
    ("bytearray-clear", "bytearray.clear()", "method", "bytes", "Очищает.", "ba.clear()", "ba.clear()", ["bytearray"]),

    # ---- regex ----
    ("re-match", "re.match()", "function", "re", "Ищет совпадение с начала.", "re.match(pattern, s)", "re.match(r'\\d+', '123')", ["re"]),
    ("re-search", "re.search()", "function", "re", "Ищет первое совпадение.", "re.search(pattern, s)", "re.search(r'\\d+', 'a1b')", ["re"]),
    ("re-findall", "re.findall()", "function", "re", "Все совпадения.", "re.findall(pattern, s)", "re.findall(r'\\d+', 'a1b2')", ["re"]),
    ("re-finditer", "re.finditer()", "function", "re", "Итератор совпадений.", "re.finditer(pattern, s)", "list(re.finditer(r'\\d+', 'a1b'))", ["re"]),
    ("re-sub", "re.sub()", "function", "re", "Заменяет совпадения.", "re.sub(pattern, repl, s)", "re.sub(r'\\d+', '*', 'a1b2')", ["re"]),
    ("re-subn", "re.subn()", "function", "re", "Заменяет, возвращает счёт.", "re.subn(pattern, repl, s)", "re.subn(r'\\d+', '*', 'a1b2')", ["re"]),
    ("re-split", "re.split()", "function", "re", "Разбивает по шаблону.", "re.split(pattern, s)", "re.split(r'\\d+', 'a1b2c')", ["re"]),
    ("re-compile", "re.compile()", "function", "re", "Компилирует шаблон.", "re.compile(pattern)", "re.compile(r'\\d+')", ["re"]),
    ("re-fullmatch", "re.fullmatch()", "function", "re", "Полное совпадение.", "re.fullmatch(pattern, s)", "re.fullmatch(r'\\d+', '123')", ["re"]),
    ("re-escape", "re.escape()", "function", "re", "Экранирует спецсимволы.", "re.escape(s)", "re.escape('a.b')", ["re"]),
    ("re-purge", "re.purge()", "function", "re", "Чистит кэш шаблонов.", "re.purge()", "re.purge()", ["re"]),
    ("match-group", "Match.group()", "method", "re", "Возвращает группу.", "match.group(0)", "m.group(1)", ["re"]),
    ("match-groups", "Match.groups()", "method", "re", "Все группы.", "match.groups()", "m.groups()", ["re"]),
    ("match-groupdict", "Match.groupdict()", "method", "re", "Словарь именованных групп.", "match.groupdict()", "m.groupdict()", ["re"]),
    ("match-start", "Match.start()", "method", "re", "Начальная позиция.", "match.start()", "m.start()", ["re"]),
    ("match-end", "Match.end()", "method", "re", "Конечная позиция.", "match.end()", "m.end()", ["re"]),
    ("match-span", "Match.span()", "method", "re", "Пара (start, end).", "match.span()", "m.span()", ["re"]),

    # ---- pathlib ----
    ("path-exists", "Path.exists()", "method", "pathlib", "Существует ли путь?", "p.exists()", "Path('f.txt').exists()", ["pathlib"]),
    ("path-is-file", "Path.is_file()", "method", "pathlib", "Это файл?", "p.is_file()", "Path('f.txt').is_file()", ["pathlib"]),
    ("path-is-dir", "Path.is_dir()", "method", "pathlib", "Это папка?", "p.is_dir()", "Path('d').is_dir()", ["pathlib"]),
    ("path-mkdir", "Path.mkdir()", "method", "pathlib", "Создаёт папку.", "p.mkdir(parents=True, exist_ok=True)", "Path('d').mkdir()", ["pathlib"]),
    ("path-rmdir", "Path.rmdir()", "method", "pathlib", "Удаляет пустую папку.", "p.rmdir()", "Path('d').rmdir()", ["pathlib"]),
    ("path-unlink", "Path.unlink()", "method", "pathlib", "Удаляет файл.", "p.unlink(missing_ok=True)", "Path('f').unlink()", ["pathlib"]),
    ("path-rename", "Path.rename()", "method", "pathlib", "Переименовывает.", "p.rename(target)", "Path('a').rename('b')", ["pathlib"]),
    ("path-replace", "Path.replace()", "method", "pathlib", "Перемещает/заменяет.", "p.replace(target)", "Path('a').replace('b')", ["pathlib"]),
    ("path-touch", "Path.touch()", "method", "pathlib", "Создаёт или обновляет.", "p.touch()", "Path('f').touch()", ["pathlib"]),
    ("path-read-text", "Path.read_text()", "method", "pathlib", "Читает текст.", "p.read_text(encoding='utf-8')", "Path('f').read_text()", ["pathlib"]),
    ("path-write-text", "Path.write_text()", "method", "pathlib", "Пишет текст.", "p.write_text(text)", "Path('f').write_text('hi')", ["pathlib"]),
    ("path-read-bytes", "Path.read_bytes()", "method", "pathlib", "Читает байты.", "p.read_bytes()", "Path('f').read_bytes()", ["pathlib"]),
    ("path-write-bytes", "Path.write_bytes()", "method", "pathlib", "Пишет байты.", "p.write_bytes(data)", "Path('f').write_bytes(b'x')", ["pathlib"]),
    ("path-glob", "Path.glob()", "method", "pathlib", "Ищет по шаблону.", "p.glob(pattern)", "Path('.').glob('*.py')", ["pathlib"]),
    ("path-rglob", "Path.rglob()", "method", "pathlib", "Рекурсивный glob.", "p.rglob(pattern)", "Path('.').rglob('*.py')", ["pathlib"]),
    ("path-iterdir", "Path.iterdir()", "method", "pathlib", "Содержимое папки.", "p.iterdir()", "list(Path('.').iterdir())", ["pathlib"]),
    ("path-parent", "Path.parent", "attr", "pathlib", "Родительская папка.", "p.parent", "Path('a/b').parent", ["pathlib"]),
    ("path-name", "Path.name", "attr", "pathlib", "Имя файла.", "p.name", "Path('a/b.txt').name", ["pathlib"]),
    ("path-stem", "Path.stem", "attr", "pathlib", "Имя без расширения.", "p.stem", "Path('f.txt').stem", ["pathlib"]),
    ("path-suffix", "Path.suffix", "attr", "pathlib", "Расширение.", "p.suffix", "Path('f.txt').suffix", ["pathlib"]),
    ("path-with-suffix", "Path.with_suffix()", "method", "pathlib", "Меняет расширение.", "p.with_suffix('.md')", "Path('f.txt').with_suffix('.md')", ["pathlib"]),
    ("path-with-name", "Path.with_name()", "method", "pathlib", "Меняет имя.", "p.with_name('b')", "Path('a').with_name('b')", ["pathlib"]),
    ("path-joinpath", "Path.joinpath()", "method", "pathlib", "Склеивает пути.", "p.joinpath(*parts)", "Path('a').joinpath('b', 'c')", ["pathlib"]),
    ("path-resolve", "Path.resolve()", "method", "pathlib", "Абсолютный путь.", "p.resolve()", "Path('a').resolve()", ["pathlib"]),
    ("path-relative-to", "Path.relative_to()", "method", "pathlib", "Относительный путь.", "p.relative_to(base)", "Path('/a/b').relative_to('/a')", ["pathlib"]),
    ("path-stat", "Path.stat()", "method", "pathlib", "Информация о файле.", "p.stat()", "Path('f').stat()", ["pathlib"]),
    ("path-owner", "Path.owner()", "method", "pathlib", "Владелец файла.", "p.owner()", "Path('f').owner()", ["pathlib"]),
    ("path-chmod", "Path.chmod()", "method", "pathlib", "Меняет права.", "p.chmod(mode)", "Path('f').chmod(0o644)", ["pathlib"]),

    # ---- datetime ----
    ("datetime-now", "datetime.now()", "method", "datetime", "Текущие дата и время.", "datetime.now(tz=None)", "datetime.now()", ["datetime"]),
    ("datetime-utcnow", "datetime.utcnow()", "method", "datetime", "Текущее UTC время.", "datetime.utcnow()", "datetime.utcnow()", ["datetime"]),
    ("datetime-today", "date.today()", "method", "datetime", "Сегодняшняя дата.", "date.today()", "date.today()", ["datetime"]),
    ("datetime-fromtimestamp", "datetime.fromtimestamp()", "method", "datetime", "Из timestamp.", "datetime.fromtimestamp(ts)", "datetime.fromtimestamp(0)", ["datetime"]),
    ("datetime-fromisoformat", "datetime.fromisoformat()", "method", "datetime", "Из ISO-строки.", "datetime.fromisoformat(s)", "datetime.fromisoformat('2024-01-01')", ["datetime"]),
    ("datetime-strptime", "datetime.strptime()", "method", "datetime", "Из строки по формату.", "datetime.strptime(s, fmt)", "datetime.strptime('2024-01-01', '%Y-%m-%d')", ["datetime"]),
    ("datetime-strftime", "datetime.strftime()", "method", "datetime", "В строку по формату.", "dt.strftime(fmt)", "dt.strftime('%Y-%m-%d')", ["datetime"]),
    ("datetime-isoformat", "datetime.isoformat()", "method", "datetime", "В ISO-строку.", "dt.isoformat()", "dt.isoformat()", ["datetime"]),
    ("datetime-timestamp", "datetime.timestamp()", "method", "datetime", "Unix-время.", "dt.timestamp()", "dt.timestamp()", ["datetime"]),
    ("datetime-replace", "datetime.replace()", "method", "datetime", "Копия с заменами.", "dt.replace(year=2025)", "dt.replace(year=2025)", ["datetime"]),
    ("datetime-weekday", "datetime.weekday()", "method", "datetime", "День недели (0=Пн).", "dt.weekday()", "dt.weekday()", ["datetime"]),
    ("datetime-isoweekday", "datetime.isoweekday()", "method", "datetime", "День недели (1=Пн).", "dt.isoweekday()", "dt.isoweekday()", ["datetime"]),
    ("datetime-date", "datetime.date()", "method", "datetime", "Извлекает дату.", "dt.date()", "dt.date()", ["datetime"]),
    ("datetime-time", "datetime.time()", "method", "datetime", "Извлекает время.", "dt.time()", "dt.time()", ["datetime"]),
    ("datetime-combine", "datetime.combine()", "method", "datetime", "Объединяет дату и время.", "datetime.combine(date, time)", "datetime.combine(d, t)", ["datetime"]),
    ("timedelta-days", "timedelta.days", "attr", "datetime", "Количество дней.", "td.days", "td.days", ["datetime"]),
    ("timedelta-seconds", "timedelta.seconds", "attr", "datetime", "Секунды в дне.", "td.seconds", "td.seconds", ["datetime"]),
    ("timedelta-total-seconds", "timedelta.total_seconds()", "method", "datetime", "Полные секунды.", "td.total_seconds()", "td.total_seconds()", ["datetime"]),
    ("date-fromisoformat", "date.fromisoformat()", "method", "datetime", "Дата из ISO.", "date.fromisoformat(s)", "date.fromisoformat('2024-01-01')", ["datetime"]),
    ("date-fromtimestamp", "date.fromtimestamp()", "method", "datetime", "Дата из timestamp.", "date.fromtimestamp(ts)", "date.fromtimestamp(0)", ["datetime"]),
    ("date-year", "date.year", "attr", "datetime", "Год.", "d.year", "d.year", ["datetime"]),
    ("date-month", "date.month", "attr", "datetime", "Месяц.", "d.month", "d.month", ["datetime"]),
    ("date-day", "date.day", "attr", "datetime", "День.", "d.day", "d.day", ["datetime"]),

    # ---- time ----
    ("time-time", "time.time()", "function", "time", "Текущий timestamp.", "time.time()", "time.time()", ["time"]),
    ("time-sleep", "time.sleep()", "function", "time", "Пауза в секундах.", "time.sleep(secs)", "time.sleep(1)", ["time"]),
    ("time-perf-counter", "time.perf_counter()", "function", "time", "Точный таймер.", "time.perf_counter()", "time.perf_counter()", ["time"]),
    ("time-monotonic", "time.monotonic()", "function", "time", "Монотонный таймер.", "time.monotonic()", "time.monotonic()", ["time"]),
    ("time-process-time", "time.process_time()", "function", "time", "CPU-время.", "time.process_time()", "time.process_time()", ["time"]),
    ("time-localtime", "time.localtime()", "function", "time", "Локальное время.", "time.localtime()", "time.localtime()", ["time"]),
    ("time-gmtime", "time.gmtime()", "function", "time", "UTC время.", "time.gmtime()", "time.gmtime()", ["time"]),
    ("time-strftime", "time.strftime()", "function", "time", "Формат времени.", "time.strftime(fmt, t)", "time.strftime('%Y-%m-%d')", ["time"]),
    ("time-strptime", "time.strptime()", "function", "time", "Парсинг времени.", "time.strptime(s, fmt)", "time.strptime('2024', '%Y')", ["time"]),
    ("time-mktime", "time.mktime()", "function", "time", "Из struct_time в timestamp.", "time.mktime(t)", "time.mktime(time.localtime())", ["time"]),
    ("time-ctime", "time.ctime()", "function", "time", "Человекочитаемая строка.", "time.ctime()", "time.ctime()", ["time"]),
    ("time-asctime", "time.asctime()", "function", "time", "Время как строка.", "time.asctime(t)", "time.asctime()", ["time"]),

    # ---- calendar ----
    ("calendar-isleap", "calendar.isleap()", "function", "calendar", "Високосный год?", "calendar.isleap(year)", "calendar.isleap(2024)", ["calendar"]),
    ("calendar-leapdays", "calendar.leapdays()", "function", "calendar", "Число високосных.", "calendar.leapdays(y1, y2)", "calendar.leapdays(2000, 2024)", ["calendar"]),
    ("calendar-monthrange", "calendar.monthrange()", "function", "calendar", "День недели и дней в месяце.", "calendar.monthrange(y, m)", "calendar.monthrange(2024, 2)", ["calendar"]),
    ("calendar-weekday", "calendar.weekday()", "function", "calendar", "День недели даты.", "calendar.weekday(y, m, d)", "calendar.weekday(2024, 1, 1)", ["calendar"]),
    ("calendar-month", "calendar.month()", "function", "calendar", "Текстовый месяц.", "calendar.month(y, m)", "calendar.month(2024, 1)", ["calendar"]),
    ("calendar-calendar", "calendar.calendar()", "function", "calendar", "Текстовый год.", "calendar.calendar(y)", "calendar.calendar(2024)", ["calendar"]),
    ("calendar-textcalendar", "TextCalendar", "class", "calendar", "Текстовый календарь.", "calendar.TextCalendar()", "calendar.TextCalendar()", ["calendar"]),
    ("calendar-htmlcalendar", "HTMLCalendar", "class", "calendar", "HTML-календарь.", "calendar.HTMLCalendar()", "calendar.HTMLCalendar()", ["calendar"]),

    # ---- itertools ----
    ("itertools-count", "itertools.count()", "function", "itertools", "Бесконечный счётчик.", "count(start, step)", "count(0, 2)", ["itertools"]),
    ("itertools-cycle", "itertools.cycle()", "function", "itertools", "Бесконечный цикл.", "cycle(iter)", "cycle([1, 2])", ["itertools"]),
    ("itertools-repeat", "itertools.repeat()", "function", "itertools", "Повтор значения.", "repeat(obj, n)", "repeat('x', 3)", ["itertools"]),
    ("itertools-chain", "itertools.chain()", "function", "itertools", "Сцепляет итераторы.", "chain(*iters)", "chain([1], [2])", ["itertools"]),
    ("itertools-chain-from-iterable", "itertools.chain.from_iterable()", "function", "itertools", "Сцепляет один итератор.", "chain.from_iterable(it)", "chain.from_iterable([[1],[2]])", ["itertools"]),
    ("itertools-accumulate", "itertools.accumulate()", "function", "itertools", "Накопление.", "accumulate(iter, func)", "accumulate([1,2,3])", ["itertools"]),
    ("itertools-product", "itertools.product()", "function", "itertools", "Декартово произведение.", "product(*iters, repeat)", "product([0,1], repeat=2)", ["itertools"]),
    ("itertools-permutations", "itertools.permutations()", "function", "itertools", "Перестановки.", "permutations(iter, r)", "permutations([1,2,3])", ["itertools"]),
    ("itertools-combinations", "itertools.combinations()", "function", "itertools", "Комбинации.", "combinations(iter, r)", "combinations([1,2,3], 2)", ["itertools"]),
    ("itertools-combinations-with-replacement", "itertools.combinations_with_replacement()", "function", "itertools", "С повторами.", "combinations_with_replacement(iter, r)", "...", ["itertools"]),
    ("itertools-groupby", "itertools.groupby()", "function", "itertools", "Группирует по ключу.", "groupby(iter, key)", "groupby('AABBC')", ["itertools"]),
    ("itertools-starmap", "itertools.starmap()", "function", "itertools", "Применяет func(*args).", "starmap(func, iter)", "starmap(pow, [(2,3)])", ["itertools"]),
    ("itertools-compress", "itertools.compress()", "function", "itertools", "Фильтрует по маске.", "compress(data, selectors)", "compress([1,2,3], [1,0,1])", ["itertools"]),
    ("itertools-dropwhile", "itertools.dropwhile()", "function", "itertools", "Отбрасывает пока true.", "dropwhile(pred, iter)", "dropwhile(lambda x: x<3, [1,2,3,4])", ["itertools"]),
    ("itertools-takewhile", "itertools.takewhile()", "function", "itertools", "Берёт пока true.", "takewhile(pred, iter)", "takewhile(lambda x: x<3, [1,2,3,4])", ["itertools"]),
    ("itertools-filterfalse", "itertools.filterfalse()", "function", "itertools", "Обратный фильтр.", "filterfalse(pred, iter)", "filterfalse(bool, [0,1,2])", ["itertools"]),
    ("itertools-islice", "itertools.islice()", "function", "itertools", "Срез итератора.", "islice(iter, stop)", "islice(count(), 5)", ["itertools"]),
    ("itertools-tee", "itertools.tee()", "function", "itertools", "N копий итератора.", "tee(iter, n)", "tee(iter([1,2]), 2)", ["itertools"]),
    ("itertools-pairwise", "itertools.pairwise()", "function", "itertools", "Пары соседних.", "pairwise(iter)", "pairwise([1,2,3])", ["itertools"]),
    ("itertools-zip-longest", "itertools.zip_longest()", "function", "itertools", "Zip до самой длинной.", "zip_longest(*iters, fillvalue)", "zip_longest([1,2], [3])", ["itertools"]),

    # ---- collections ----
    ("collections-counter", "Counter", "class", "collections", "Подсчёт элементов.", "Counter(iter)", "Counter('aabbc')", ["collections"]),
    ("collections-deque", "deque", "class", "collections", "Двусторонняя очередь.", "deque(iter, maxlen)", "deque([1,2])", ["collections"]),
    ("collections-defaultdict", "defaultdict", "class", "collections", "Словарь с дефолтом.", "defaultdict(factory)", "defaultdict(list)", ["collections"]),
    ("collections-namedtuple", "namedtuple()", "function", "collections", "Именованный кортеж.", "namedtuple(name, fields)", "namedtuple('Point', 'x y')", ["collections"]),
    ("collections-ordereddict", "OrderedDict", "class", "collections", "Словарь с порядком.", "OrderedDict()", "OrderedDict()", ["collections"]),
    ("collections-chainmap", "ChainMap", "class", "collections", "Объединение словарей.", "ChainMap(*maps)", "ChainMap(d1, d2)", ["collections"]),

    # ---- functools ----
    ("functools-partial", "partial()", "function", "functools", "Фиксирует аргументы.", "partial(func, *args)", "partial(pow, 2)", ["functools"]),
    ("functools-lru-cache", "lru_cache()", "decorator", "functools", "Кэш LRU.", "@lru_cache(maxsize=128)", "@lru_cache(None)", ["functools"]),
    ("functools-cache", "cache()", "decorator", "functools", "Бесконечный кэш.", "@cache", "@cache", ["functools"]),
    ("functools-reduce", "reduce()", "function", "functools", "Свёртка.", "reduce(func, iter, init)", "reduce(add, [1,2,3])", ["functools"]),
    ("functools-wraps", "wraps()", "decorator", "functools", "Сохраняет метаданные.", "@wraps(func)", "@wraps(f)", ["functools"]),
    ("functools-total-ordering", "total_ordering()", "decorator", "functools", "Авто-сравнение.", "@total_ordering", "@total_ordering", ["functools"]),
    ("functools-singledispatch", "singledispatch()", "decorator", "functools", "Диспетчеризация по типу.", "@singledispatch", "@singledispatch", ["functools"]),
    ("functools-cmp-to-key", "cmp_to_key()", "function", "functools", "cmp → key для sort.", "cmp_to_key(cmp)", "cmp_to_key(cmp)", ["functools"]),

    # ---- operator ----
    ("operator-add", "operator.add()", "function", "operator", "a + b.", "add(a, b)", "add(1, 2)", ["operator"]),
    ("operator-sub", "operator.sub()", "function", "operator", "a - b.", "sub(a, b)", "sub(3, 1)", ["operator"]),
    ("operator-mul", "operator.mul()", "function", "operator", "a * b.", "mul(a, b)", "mul(2, 3)", ["operator"]),
    ("operator-truediv", "operator.truediv()", "function", "operator", "a / b.", "truediv(a, b)", "truediv(4, 2)", ["operator"]),
    ("operator-floordiv", "operator.floordiv()", "function", "operator", "a // b.", "floordiv(a, b)", "floordiv(5, 2)", ["operator"]),
    ("operator-mod", "operator.mod()", "function", "operator", "a % b.", "mod(a, b)", "mod(5, 2)", ["operator"]),
    ("operator-pow", "operator.pow()", "function", "operator", "a ** b.", "pow(a, b)", "pow(2, 3)", ["operator"]),
    ("operator-neg", "operator.neg()", "function", "operator", "-a.", "neg(a)", "neg(5)", ["operator"]),
    ("operator-eq", "operator.eq()", "function", "operator", "a == b.", "eq(a, b)", "eq(1, 1)", ["operator"]),
    ("operator-ne", "operator.ne()", "function", "operator", "a != b.", "ne(a, b)", "ne(1, 2)", ["operator"]),
    ("operator-lt", "operator.lt()", "function", "operator", "a < b.", "lt(a, b)", "lt(1, 2)", ["operator"]),
    ("operator-le", "operator.le()", "function", "operator", "a <= b.", "le(a, b)", "le(1, 1)", ["operator"]),
    ("operator-gt", "operator.gt()", "function", "operator", "a > b.", "gt(a, b)", "gt(2, 1)", ["operator"]),
    ("operator-ge", "operator.ge()", "function", "operator", "a >= b.", "ge(a, b)", "ge(1, 1)", ["operator"]),
    ("operator-and", "operator.and_()", "function", "operator", "a & b.", "and_(a, b)", "and_(3, 1)", ["operator"]),
    ("operator-or", "operator.or_()", "function", "operator", "a | b.", "or_(a, b)", "or_(1, 2)", ["operator"]),
    ("operator-xor", "operator.xor()", "function", "operator", "a ^ b.", "xor(a, b)", "xor(1, 3)", ["operator"]),
    ("operator-invert", "operator.invert()", "function", "operator", "~a.", "invert(a)", "invert(0)", ["operator"]),
    ("operator-lshift", "operator.lshift()", "function", "operator", "a << b.", "lshift(a, b)", "lshift(1, 2)", ["operator"]),
    ("operator-rshift", "operator.rshift()", "function", "operator", "a >> b.", "rshift(a, b)", "rshift(4, 1)", ["operator"]),
    ("operator-itemgetter", "itemgetter()", "class", "operator", "Получает элементы.", "itemgetter(key)", "itemgetter(0)", ["operator"]),
    ("operator-attrgetter", "attrgetter()", "class", "operator", "Получает атрибуты.", "attrgetter(attr)", "attrgetter('x')", ["operator"]),
    ("operator-methodcaller", "methodcaller()", "class", "operator", "Вызывает метод.", "methodcaller(name)", "methodcaller('upper')", ["operator"]),
    ("operator-length-hint", "operator.length_hint()", "function", "operator", "Ожидаемая длина.", "length_hint(obj)", "length_hint(iter([1,2]))", ["operator"]),

    # ---- bisect ----
    ("bisect-left", "bisect_left()", "function", "bisect", "Индекс вставки слева.", "bisect_left(a, x)", "bisect_left([1,3,5], 3)", ["bisect"]),
    ("bisect-right", "bisect_right()", "function", "bisect", "Индекс вставки справа.", "bisect_right(a, x)", "bisect_right([1,3,5], 3)", ["bisect"]),
    ("bisect-insort-left", "insort_left()", "function", "bisect", "Вставляет слева.", "insort_left(a, x)", "insort_left([1,3], 2)", ["bisect"]),
    ("bisect-insort-right", "insort_right()", "function", "bisect", "Вставляет справа.", "insort_right(a, x)", "insort_right([1,3], 2)", ["bisect"]),

    # ---- heapq ----
    ("heapq-heappush", "heappush()", "function", "heapq", "Добавляет в кучу.", "heappush(h, item)", "heappush(h, 1)", ["heapq"]),
    ("heapq-heappop", "heappop()", "function", "heapq", "Извлекает минимум.", "heappop(h)", "heappop(h)", ["heapq"]),
    ("heapq-heapify", "heapify()", "function", "heapq", "Делает кучу из списка.", "heapify(list)", "heapify([3,1,2])", ["heapq"]),
    ("heapq-heapreplace", "heapreplace()", "function", "heapq", "Заменяет корень.", "heapreplace(h, item)", "heapreplace(h, 5)", ["heapq"]),
    ("heapq-nlargest", "nlargest()", "function", "heapq", "N наибольших.", "nlargest(n, iter)", "nlargest(3, [5,1,3,2,4])", ["heapq"]),
    ("heapq-nsmallest", "nsmallest()", "function", "heapq", "N наименьших.", "nsmallest(n, iter)", "nsmallest(2, [5,1,3])", ["heapq"]),
    ("heapq-merge", "merge()", "function", "heapq", "Сливает сортированные.", "merge(*iters)", "merge([1,3], [2,4])", ["heapq"]),

    # ---- copy ----
    ("copy-copy", "copy.copy()", "function", "copy", "Поверхностная копия.", "copy.copy(x)", "copy.copy([1,[2]])", ["copy"]),
    ("copy-deepcopy", "copy.deepcopy()", "function", "copy", "Глубокая копия.", "copy.deepcopy(x)", "copy.deepcopy([1,[2]])", ["copy"]),

    # ---- pprint ----
    ("pprint-pprint", "pprint()", "function", "pprint", "Красивый вывод.", "pprint(obj)", "pprint({'a': 1})", ["pprint"]),
    ("pprint-pformat", "pformat()", "function", "pprint", "Строковое представление.", "pformat(obj)", "pformat([1,2,3])", ["pprint"]),
    ("pprint-pp", "pp()", "function", "pprint", "Компактный pprint.", "pp(obj)", "pp({'a': 1})", ["pprint"]),
    ("pprint-isreadable", "isreadable()", "function", "pprint", "Читаемое repr?", "isreadable(obj)", "isreadable(1)", ["pprint"]),

    # ---- warnings ----
    ("warnings-warn", "warn()", "function", "warnings", "Выдаёт предупреждение.", "warn(msg, category)", "warn('old', DeprecationWarning)", ["warnings"]),
    ("warnings-filterwarnings", "filterwarnings()", "function", "warnings", "Фильтр предупреждений.", "filterwarnings(action)", "filterwarnings('ignore')", ["warnings"]),
    ("warnings-simplefilter", "simplefilter()", "function", "warnings", "Простой фильтр.", "simplefilter(action)", "simplefilter('default')", ["warnings"]),
    ("warnings-catch-warnings", "catch_warnings()", "class", "warnings", "Контекст для предупреждений.", "with catch_warnings():", "with catch_warnings(): ...", ["warnings"]),
    ("warnings-resetwarnings", "resetwarnings()", "function", "warnings", "Сбрасывает фильтры.", "resetwarnings()", "resetwarnings()", ["warnings"]),

    # ---- contextlib ----
    ("contextlib-contextmanager", "contextmanager()", "decorator", "contextlib", "Декоратор-контекст.", "@contextmanager", "@contextmanager", ["contextlib"]),
    ("contextlib-closing", "closing()", "class", "contextlib", "Автозакрытие.", "closing(obj)", "closing(open('f'))", ["contextlib"]),
    ("contextlib-suppress", "suppress()", "class", "contextlib", "Подавляет исключения.", "suppress(*exc)", "suppress(FileNotFoundError)", ["contextlib"]),
    ("contextlib-redirect-stdout", "redirect_stdout()", "class", "contextlib", "Перенаправляет stdout.", "redirect_stdout(f)", "redirect_stdout(io.StringIO())", ["contextlib"]),
    ("contextlib-redirect-stderr", "redirect_stderr()", "class", "contextlib", "Перенаправляет stderr.", "redirect_stderr(f)", "redirect_stderr(io.StringIO())", ["contextlib"]),
    ("contextlib-nullcontext", "nullcontext()", "class", "contextlib", "Пустой контекст.", "nullcontext()", "nullcontext()", ["contextlib"]),
    ("contextlib-asynccontextmanager", "asynccontextmanager()", "decorator", "contextlib", "Async декоратор-контекст.", "@asynccontextmanager", "@asynccontextmanager", ["contextlib"]),
    ("contextlib-exitstack", "ExitStack()", "class", "contextlib", "Стек контекстов.", "ExitStack()", "ExitStack()", ["contextlib"]),

    # ---- enum ----
    ("enum-Enum", "Enum", "class", "enum", "База перечислений.", "class C(Enum):", "class Color(Enum): ...", ["enum"]),
    ("enum-IntEnum", "IntEnum", "class", "enum", "Enum с int-значениями.", "class C(IntEnum):", "class Num(IntEnum): ...", ["enum"]),
    ("enum-Flag", "Flag", "class", "enum", "Битовые флаги.", "class C(Flag):", "class Perm(Flag): ...", ["enum"]),
    ("enum-IntFlag", "IntFlag", "class", "enum", "Битовые int-флаги.", "class C(IntFlag):", "class F(IntFlag): ...", ["enum"]),
    ("enum-auto", "auto()", "function", "enum", "Авто-значение.", "auto()", "RED = auto()", ["enum"]),
    ("enum-unique", "unique()", "decorator", "enum", "Проверяет уникальность.", "@unique", "@unique", ["enum"]),

    # ---- logging ----
    ("logging-basicConfig", "basicConfig()", "function", "logging", "Базовая настройка.", "basicConfig(level=...)", "basicConfig(level=logging.INFO)", ["logging"]),
    ("logging-getLogger", "getLogger()", "function", "logging", "Получает логгер.", "getLogger(name)", "getLogger('app')", ["logging"]),
    ("logging-debug", "logging.debug()", "function", "logging", "Отладка.", "debug(msg)", "logging.debug('x')", ["logging"]),
    ("logging-info", "logging.info()", "function", "logging", "Информация.", "info(msg)", "logging.info('x')", ["logging"]),
    ("logging-warning", "logging.warning()", "function", "logging", "Предупреждение.", "warning(msg)", "logging.warning('x')", ["logging"]),
    ("logging-error", "logging.error()", "function", "logging", "Ошибка.", "error(msg)", "logging.error('x')", ["logging"]),
    ("logging-critical", "logging.critical()", "function", "logging", "Критическая ошибка.", "critical(msg)", "logging.critical('x')", ["logging"]),
    ("logging-exception", "logging.exception()", "function", "logging", "Лог исключения.", "exception(msg)", "logging.exception('fail')", ["logging"]),
    ("logging-FileHandler", "FileHandler", "class", "logging", "Пишет в файл.", "FileHandler('app.log')", "FileHandler('a.log')", ["logging"]),
    ("logging-StreamHandler", "StreamHandler", "class", "logging", "Пишет в поток.", "StreamHandler()", "StreamHandler(sys.stderr)", ["logging"]),
    ("logging-Formatter", "Formatter", "class", "logging", "Формат сообщения.", "Formatter(fmt)", "Formatter('%(message)s')", ["logging"]),
    ("logging-setLevel", "setLevel()", "method", "logging", "Устанавливает уровень.", "logger.setLevel(level)", "logger.setLevel(logging.DEBUG)", ["logging"]),
    ("logging-disable", "logging.disable()", "function", "logging", "Отключает уровни.", "disable(level)", "disable(logging.CRITICAL)", ["logging"]),

    # ---- unittest ----
    ("unittest-TestCase", "TestCase", "class", "unittest", "База тестов.", "class T(TestCase):", "class TestFoo(TestCase): ...", ["unittest"]),
    ("unittest-main", "main()", "function", "unittest", "Запуск тестов.", "main()", "unittest.main()", ["unittest"]),
    ("unittest-assertEqual", "assertEqual()", "method", "unittest", "Проверяет равенство.", "assertEqual(a, b)", "self.assertEqual(1, 1)", ["unittest"]),
    ("unittest-assertTrue", "assertTrue()", "method", "unittest", "Проверяет истину.", "assertTrue(x)", "self.assertTrue(x)", ["unittest"]),
    ("unittest-assertFalse", "assertFalse()", "method", "unittest", "Проверяет ложь.", "assertFalse(x)", "self.assertFalse(x)", ["unittest"]),
    ("unittest-assertRaises", "assertRaises()", "method", "unittest", "Проверяет исключение.", "assertRaises(exc)", "self.assertRaises(ValueError)", ["unittest"]),
    ("unittest-skip", "skip()", "decorator", "unittest", "Пропуск теста.", "@skip(reason)", "@skip('wip')", ["unittest"]),
    ("unittest-skipIf", "skipIf()", "decorator", "unittest", "Пропуск при условии.", "@skipIf(cond)", "@skipIf(sys.platform=='win32')", ["unittest"]),
    ("unittest-mock", "unittest.mock", "module", "unittest", "Моки.", "from unittest.mock import Mock", "Mock()", ["unittest"]),
    ("unittest-patch", "patch()", "decorator", "unittest", "Патч импортов.", "@patch('mod.func')", "@patch('os.getcwd')", ["unittest"]),

    # ---- argparse ----
    ("argparse-ArgumentParser", "ArgumentParser", "class", "argparse", "Парсер аргументов.", "ArgumentParser()", "ArgumentParser(description='...')", ["argparse"]),
    ("argparse-add-argument", "add_argument()", "method", "argparse", "Добавляет аргумент.", "add_argument(name, ...)", "parser.add_argument('-n', type=int)", ["argparse"]),
    ("argparse-parse-args", "parse_args()", "method", "argparse", "Разбирает аргументы.", "parse_args()", "parser.parse_args()", ["argparse"]),
    ("argparse-Namespace", "Namespace", "class", "argparse", "Результат разбора.", "Namespace()", "Namespace(x=1)", ["argparse"]),
    ("argparse-FileType", "FileType()", "function", "argparse", "Файл как тип.", "FileType('r')", "FileType('w')", ["argparse"]),

    # ---- configparser ----
    ("configparser-ConfigParser", "ConfigParser", "class", "configparser", "Парсер INI.", "ConfigParser()", "ConfigParser()", ["configparser"]),
    ("configparser-read", "read()", "method", "configparser", "Читает INI.", "read(file)", "config.read('config.ini')", ["configparser"]),
    ("configparser-write", "write()", "method", "configparser", "Пишет INI.", "write(f)", "config.write(f)", ["configparser"]),
    ("configparser-get", "get()", "method", "configparser", "Получает значение.", "get(section, key)", "config.get('db', 'host')", ["configparser"]),
    ("configparser-set", "set()", "method", "configparser", "Устанавливает значение.", "set(section, key, val)", "config.set('db', 'host', 'x')", ["configparser"]),
    ("configparser-sections", "sections()", "method", "configparser", "Список секций.", "sections()", "config.sections()", ["configparser"]),
    ("configparser-has-section", "has_section()", "method", "configparser", "Есть секция?", "has_section(name)", "config.has_section('db')", ["configparser"]),
    ("configparser-has-option", "has_option()", "method", "configparser", "Есть опция?", "has_option(sec, opt)", "config.has_option('db', 'host')", ["configparser"]),

    # ---- zipfile ----
    ("zipfile-ZipFile", "ZipFile", "class", "zipfile", "Открывает ZIP.", "ZipFile(path, mode)", "ZipFile('a.zip', 'r')", ["zipfile"]),
    ("zipfile-namelist", "namelist()", "method", "zipfile", "Список файлов в архиве.", "namelist()", "z.namelist()", ["zipfile"]),
    ("zipfile-read", "read()", "method", "zipfile", "Читает файл.", "read(name)", "z.read('a.txt')", ["zipfile"]),
    ("zipfile-write", "write()", "method", "zipfile", "Добавляет файл.", "write(filename, arcname)", "z.write('a.txt')", ["zipfile"]),
    ("zipfile-extractall", "extractall()", "method", "zipfile", "Распаковывает всё.", "extractall(path)", "z.extractall('out')", ["zipfile"]),
    ("zipfile-extract", "extract()", "method", "zipfile", "Распаковывает файл.", "extract(member, path)", "z.extract('a.txt')", ["zipfile"]),
    ("zipfile-close", "close()", "method", "zipfile", "Закрывает архив.", "close()", "z.close()", ["zipfile"]),

    # ---- tarfile ----
    ("tarfile-open", "open()", "function", "tarfile", "Открывает tar.", "open(name, mode)", "tarfile.open('a.tar.gz')", ["tarfile"]),
    ("tarfile-getmembers", "getmembers()", "method", "tarfile", "Список элементов.", "getmembers()", "t.getmembers()", ["tarfile"]),
    ("tarfile-extractall", "extractall()", "method", "tarfile", "Распаковывает всё.", "extractall(path)", "t.extractall('out')", ["tarfile"]),
    ("tarfile-add", "add()", "method", "tarfile", "Добавляет файл.", "add(name)", "t.add('f.txt')", ["tarfile"]),

    # ---- gzip / bz2 / lzma / zlib ----
    ("gzip-open", "gzip.open()", "function", "gzip", "Открывает gz-файл.", "gzip.open(name, mode)", "gzip.open('f.gz', 'rt')", ["gzip"]),
    ("gzip-compress", "gzip.compress()", "function", "gzip", "Сжимает байты.", "gzip.compress(data)", "gzip.compress(b'x')", ["gzip"]),
    ("gzip-decompress", "gzip.decompress()", "function", "gzip", "Распаковывает байты.", "gzip.decompress(data)", "gzip.decompress(b'...')", ["gzip"]),
    ("bz2-open", "bz2.open()", "function", "bz2", "Открывает bz2.", "bz2.open(name, mode)", "bz2.open('f.bz2')", ["bz2"]),
    ("bz2-compress", "bz2.compress()", "function", "bz2", "Сжимает байты.", "bz2.compress(data)", "bz2.compress(b'x')", ["bz2"]),
    ("bz2-decompress", "bz2.decompress()", "function", "bz2", "Распаковывает байты.", "bz2.decompress(data)", "bz2.decompress(b'...')", ["bz2"]),
    ("lzma-open", "lzma.open()", "function", "lzma", "Открывает lzma.", "lzma.open(name, mode)", "lzma.open('f.xz')", ["lzma"]),
    ("lzma-compress", "lzma.compress()", "function", "lzma", "Сжимает байты.", "lzma.compress(data)", "lzma.compress(b'x')", ["lzma"]),
    ("lzma-decompress", "lzma.decompress()", "function", "lzma", "Распаковывает байты.", "lzma.decompress(data)", "lzma.decompress(b'...')", ["lzma"]),
    ("zlib-compress", "zlib.compress()", "function", "zlib", "Сжимает байты.", "zlib.compress(data)", "zlib.compress(b'x')", ["zlib"]),
    ("zlib-decompress", "zlib.decompress()", "function", "zlib", "Распаковывает байты.", "zlib.decompress(data)", "zlib.decompress(b'...')", ["zlib"]),
    ("zlib-crc32", "zlib.crc32()", "function", "zlib", "CRC32.", "zlib.crc32(data)", "zlib.crc32(b'x')", ["zlib"]),
    ("zlib-adler32", "zlib.adler32()", "function", "zlib", "Adler-32.", "zlib.adler32(data)", "zlib.adler32(b'x')", ["zlib"]),

    # ---- base64 ----
    ("base64-b64encode", "b64encode()", "function", "base64", "Кодирует в base64.", "b64encode(data)", "b64encode(b'hi')", ["base64"]),
    ("base64-b64decode", "b64decode()", "function", "base64", "Декодирует base64.", "b64decode(s)", "b64decode('aGk=')", ["base64"]),
    ("base64-urlsafe-b64encode", "urlsafe_b64encode()", "function", "base64", "URL-safe base64.", "urlsafe_b64encode(data)", "urlsafe_b64encode(b'x')", ["base64"]),
    ("base64-urlsafe-b64decode", "urlsafe_b64decode()", "function", "base64", "URL-safe decode.", "urlsafe_b64decode(s)", "urlsafe_b64decode('...')", ["base64"]),
    ("base64-standard-b64encode", "standard_b64encode()", "function", "base64", "Стандартный base64.", "standard_b64encode(data)", "...", ["base64"]),

    # ---- hashlib ----
    ("hashlib-md5", "hashlib.md5()", "function", "hashlib", "MD5 хэш.", "md5(data)", "hashlib.md5(b'x').hexdigest()", ["hashlib"]),
    ("hashlib-sha1", "hashlib.sha1()", "function", "hashlib", "SHA-1 хэш.", "sha1(data)", "hashlib.sha1(b'x').hexdigest()", ["hashlib"]),
    ("hashlib-sha256", "hashlib.sha256()", "function", "hashlib", "SHA-256 хэш.", "sha256(data)", "hashlib.sha256(b'x').hexdigest()", ["hashlib"]),
    ("hashlib-sha512", "hashlib.sha512()", "function", "hashlib", "SHA-512 хэш.", "sha512(data)", "hashlib.sha512(b'x').hexdigest()", ["hashlib"]),
    ("hashlib-new", "hashlib.new()", "function", "hashlib", "Хэш по имени.", "new(name, data)", "hashlib.new('sha3_256')", ["hashlib"]),
    ("hashlib-algorithms-available", "algorithms_available", "attr", "hashlib", "Доступные алгоритмы.", "algorithms_available", "hashlib.algorithms_available", ["hashlib"]),
    ("hashlib-algorithms-guaranteed", "algorithms_guaranteed", "attr", "hashlib", "Гарантированные алгоритмы.", "algorithms_guaranteed", "hashlib.algorithms_guaranteed", ["hashlib"]),

    # ---- hmac ----
    ("hmac-new", "hmac.new()", "function", "hmac", "Создаёт HMAC.", "new(key, msg, digestmod)", "hmac.new(b'k', b'm', 'sha256')", ["hmac"]),
    ("hmac-compare-digest", "hmac.compare_digest()", "function", "hmac", "Безопасное сравнение.", "compare_digest(a, b)", "hmac.compare_digest(a, b)", ["hmac"]),

    # ---- secrets ----
    ("secrets-token-bytes", "token_bytes()", "function", "secrets", "Случайные байты.", "token_bytes(n)", "token_bytes(16)", ["secrets"]),
    ("secrets-token-hex", "token_hex()", "function", "secrets", "Случайная hex-строка.", "token_hex(n)", "token_hex(16)", ["secrets"]),
    ("secrets-token-urlsafe", "token_urlsafe()", "function", "secrets", "URL-safe токен.", "token_urlsafe(n)", "token_urlsafe(16)", ["secrets"]),
    ("secrets-choice", "choice()", "function", "secrets", "Случайный элемент.", "choice(seq)", "choice('abc')", ["secrets"]),
    ("secrets-randbelow", "randbelow()", "function", "secrets", "Случайное < n.", "randbelow(n)", "randbelow(100)", ["secrets"]),

    # ---- random ----
    ("random-random", "random()", "function", "random", "Float [0, 1).", "random()", "random.random()", ["random"]),
    ("random-randint", "randint()", "function", "random", "Int в [a, b].", "randint(a, b)", "randint(1, 10)", ["random"]),
    ("random-randrange", "randrange()", "function", "random", "Int в range.", "randrange(start, stop, step)", "randrange(0, 10, 2)", ["random"]),
    ("random-choice", "choice()", "function", "random", "Случайный элемент.", "choice(seq)", "choice([1, 2, 3])", ["random"]),
    ("random-choices", "choices()", "function", "random", "Случайные с повторами.", "choices(population, k)", "choices('abc', k=5)", ["random"]),
    ("random-sample", "sample()", "function", "random", "Случайные без повторов.", "sample(population, k)", "sample([1,2,3,4], 2)", ["random"]),
    ("random-shuffle", "shuffle()", "function", "random", "Перемешивает.", "shuffle(list)", "shuffle(items)", ["random"]),
    ("random-uniform", "uniform()", "function", "random", "Float в [a, b].", "uniform(a, b)", "uniform(0, 1)", ["random"]),
    ("random-gauss", "gauss()", "function", "random", "Гауссово.", "gauss(mu, sigma)", "gauss(0, 1)", ["random"]),
    ("random-seed", "seed()", "function", "random", "Зерно.", "seed(n)", "seed(42)", ["random"]),
    ("random-getstate", "getstate()", "function", "random", "Состояние ГСЧ.", "getstate()", "getstate()", ["random"]),
    ("random-setstate", "setstate()", "function", "random", "Восстанавливает.", "setstate(state)", "setstate(s)", ["random"]),

    # ---- statistics ----
    ("statistics-mean", "mean()", "function", "statistics", "Среднее.", "mean(data)", "mean([1, 2, 3])", ["statistics"]),
    ("statistics-median", "median()", "function", "statistics", "Медиана.", "median(data)", "median([1, 2, 3])", ["statistics"]),
    ("statistics-mode", "mode()", "function", "statistics", "Мода.", "mode(data)", "mode([1, 1, 2])", ["statistics"]),
    ("statistics-multimode", "multimode()", "function", "statistics", "Все моды.", "multimode(data)", "multimode([1, 1, 2, 2])", ["statistics"]),
    ("statistics-stdev", "stdev()", "function", "statistics", "Станд. отклонение.", "stdev(data)", "stdev([1, 2, 3])", ["statistics"]),
    ("statistics-variance", "variance()", "function", "statistics", "Дисперсия.", "variance(data)", "variance([1, 2, 3])", ["statistics"]),
    ("statistics-pstdev", "pstdev()", "function", "statistics", "Станд. откл. ген. совокуп.", "pstdev(data)", "pstdev([1, 2, 3])", ["statistics"]),
    ("statistics-pvariance", "pvariance()", "function", "statistics", "Дисперсия ген. совокуп.", "pvariance(data)", "pvariance([1, 2, 3])", ["statistics"]),
    ("statistics-correlation", "correlation()", "function", "statistics", "Корреляция.", "correlation(x, y)", "correlation(x, y)", ["statistics"]),
    ("statistics-covariance", "covariance()", "function", "statistics", "Ковариация.", "covariance(x, y)", "covariance(x, y)", ["statistics"]),
    ("statistics-quantiles", "quantiles()", "function", "statistics", "Квантили.", "quantiles(data)", "quantiles(data, n=4)", ["statistics"]),

    # ---- decimal ----
    ("decimal-Decimal", "Decimal", "class", "decimal", "Десятичное число.", "Decimal(value)", "Decimal('0.1')", ["decimal"]),
    ("decimal-getcontext", "getcontext()", "function", "decimal", "Текущий контекст.", "getcontext()", "getcontext().prec", ["decimal"]),
    ("decimal-setcontext", "setcontext()", "function", "decimal", "Устанавливает контекст.", "setcontext(ctx)", "setcontext(ctx)", ["decimal"]),
    ("decimal-ROUND-HALF-UP", "ROUND_HALF_UP", "const", "decimal", "Округление вверх.", "ROUND_HALF_UP", "ROUND_HALF_UP", ["decimal"]),
    ("decimal-quantize", "Decimal.quantize()", "method", "decimal", "Округляет.", "quantize(exp)", "Decimal('1.23').quantize(Decimal('0.1'))", ["decimal"]),

    # ---- fractions ----
    ("fractions-Fraction", "Fraction", "class", "fractions", "Рациональное число.", "Fraction(num, den)", "Fraction(1, 3)", ["fractions"]),

    # ---- cmath ----
    ("cmath-phase", "phase()", "function", "cmath", "Фаза комплексного.", "phase(x)", "phase(1+1j)", ["cmath"]),
    ("cmath-polar", "polar()", "function", "cmath", "Полярные координаты.", "polar(x)", "polar(1+1j)", ["cmath"]),
    ("cmath-rect", "rect()", "function", "cmath", "Из полярных в комплекс.", "rect(r, phi)", "rect(1, 0)", ["cmath"]),
    ("cmath-sqrt", "cmath.sqrt()", "function", "cmath", "Корень комплексного.", "sqrt(x)", "sqrt(-1)", ["cmath"]),
    ("cmath-exp", "cmath.exp()", "function", "cmath", "Экспонента.", "exp(x)", "exp(1j)", ["cmath"]),
    ("cmath-log", "cmath.log()", "function", "cmath", "Логарифм.", "log(x)", "log(1+1j)", ["cmath"]),
    ("cmath-sin", "cmath.sin()", "function", "cmath", "Синус.", "sin(x)", "sin(1+0j)", ["cmath"]),
    ("cmath-cos", "cmath.cos()", "function", "cmath", "Косинус.", "cos(x)", "cos(1+0j)", ["cmath"]),
    ("cmath-isnan", "cmath.isnan()", "function", "cmath", "NaN?", "isnan(x)", "isnan(nan)", ["cmath"]),
    ("cmath-isinf", "cmath.isinf()", "function", "cmath", "Бесконечность?", "isinf(x)", "isinf(inf)", ["cmath"]),
    ("cmath-isfinite", "cmath.isfinite()", "function", "cmath", "Конечно?", "isfinite(x)", "isfinite(1)", ["cmath"]),

    # ---- struct ----
    ("struct-pack", "pack()", "function", "struct", "Пакует в байты.", "pack(fmt, *args)", "pack('i', 1)", ["struct"]),
    ("struct-unpack", "unpack()", "function", "struct", "Распаковывает.", "unpack(fmt, buffer)", "unpack('i', b'\\x01\\x00\\x00\\x00')", ["struct"]),
    ("struct-calcsize", "calcsize()", "function", "struct", "Размер формата.", "calcsize(fmt)", "calcsize('i')", ["struct"]),

    # ---- array ----
    ("array-array", "array()", "class", "array", "Компактный массив.", "array(typecode, init)", "array('i', [1, 2, 3])", ["array"]),

    # ---- weakref ----
    ("weakref-ref", "ref()", "function", "weakref", "Слабая ссылка.", "ref(obj)", "ref(o)", ["weakref"]),
    ("weakref-proxy", "proxy()", "function", "weakref", "Слабый прокси.", "proxy(obj)", "proxy(o)", ["weakref"]),
    ("weakref-WeakValueDictionary", "WeakValueDictionary", "class", "weakref", "Слабый словарь (значения).", "WeakValueDictionary()", "WeakValueDictionary()", ["weakref"]),
    ("weakref-WeakKeyDictionary", "WeakKeyDictionary", "class", "weakref", "Слабый словарь (ключи).", "WeakKeyDictionary()", "WeakKeyDictionary()", ["weakref"]),

    # ---- types ----
    ("types-SimpleNamespace", "SimpleNamespace", "class", "types", "Простой объект.", "SimpleNamespace(**kwargs)", "SimpleNamespace(a=1)", ["types"]),
    ("types-FunctionType", "FunctionType", "class", "types", "Тип функции.", "FunctionType", "isinstance(f, FunctionType)", ["types"]),
    ("types-MethodType", "MethodType", "class", "types", "Тип метода.", "MethodType", "...", ["types"]),
    ("types-LambdaType", "LambdaType", "class", "types", "Тип лямбды.", "LambdaType", "...", ["types"]),
    ("types-ModuleType", "ModuleType", "class", "types", "Тип модуля.", "ModuleType", "...", ["types"]),
    ("types-NoneType", "NoneType", "class", "types", "Тип None.", "NoneType", "type(None)", ["types"]),
    ("types-UnionType", "UnionType", "class", "types", "Тип A | B.", "UnionType", "type(int | str)", ["types"]),

    # ---- inspect ----
    ("inspect-signature", "signature()", "function", "inspect", "Сигнатура функции.", "signature(func)", "signature(f)", ["inspect"]),
    ("inspect-getsource", "getsource()", "function", "inspect", "Код объекта.", "getsource(obj)", "getsource(f)", ["inspect"]),
    ("inspect-getdoc", "getdoc()", "function", "inspect", "Документация.", "getdoc(obj)", "getdoc(f)", ["inspect"]),
    ("inspect-getfile", "getfile()", "function", "inspect", "Путь к файлу.", "getfile(obj)", "getfile(f)", ["inspect"]),
    ("inspect-isclass", "isclass()", "function", "inspect", "Это класс?", "isclass(obj)", "isclass(int)", ["inspect"]),
    ("inspect-isfunction", "isfunction()", "function", "inspect", "Это функция?", "isfunction(obj)", "isfunction(f)", ["inspect"]),
    ("inspect-ismethod", "ismethod()", "function", "inspect", "Это метод?", "ismethod(obj)", "ismethod(f)", ["inspect"]),
    ("inspect-ismodule", "ismodule()", "function", "inspect", "Это модуль?", "ismodule(obj)", "ismodule(sys)", ["inspect"]),
    ("inspect-isbuiltin", "isbuiltin()", "function", "inspect", "Встроенный?", "isbuiltin(obj)", "isbuiltin(print)", ["inspect"]),
    ("inspect-getmembers", "getmembers()", "function", "inspect", "Члены объекта.", "getmembers(obj)", "getmembers(cls)", ["inspect"]),
    ("inspect-getmro", "getmro()", "function", "inspect", "Порядок MRO.", "getmro(cls)", "getmro(C)", ["inspect"]),
    ("inspect-stack", "stack()", "function", "inspect", "Стек вызовов.", "stack()", "stack()", ["inspect"]),
    ("inspect-currentframe", "currentframe()", "function", "inspect", "Текущий фрейм.", "currentframe()", "currentframe()", ["inspect"]),

    # ---- ast ----
    ("ast-parse", "parse()", "function", "ast", "Парсит код.", "parse(source)", "parse('x = 1')", ["ast"]),
    ("ast-literal-eval", "literal_eval()", "function", "ast", "Безопасный eval.", "literal_eval(node_or_string)", "literal_eval('[1, 2]')", ["ast"]),
    ("ast-dump", "dump()", "function", "ast", "Текстовое дерево.", "dump(node)", "dump(parse('x=1'))", ["ast"]),
    ("ast-unparse", "unparse()", "function", "ast", "Код из AST.", "unparse(node)", "unparse(node)", ["ast"]),
    ("ast-NodeVisitor", "NodeVisitor", "class", "ast", "Обход дерева.", "class V(NodeVisitor):", "NodeVisitor()", ["ast"]),

    # ---- dis ----
    ("dis-dis", "dis()", "function", "dis", "Дизассемблирует.", "dis(func)", "dis(f)", ["dis"]),
    ("dis-code-info", "code_info()", "function", "dis", "Инфо о байткоде.", "code_info(func)", "code_info(f)", ["dis"]),
    ("dis-Bytecode", "Bytecode", "class", "dis", "Объект байткода.", "Bytecode(func)", "Bytecode(f)", ["dis"]),

    # ---- pdb ----
    ("pdb-set-trace", "set_trace()", "function", "pdb", "Точка останова.", "set_trace()", "pdb.set_trace()", ["pdb"]),
    ("pdb-run", "run()", "function", "pdb", "Запуск с отладкой.", "run(statement)", "pdb.run('main()')", ["pdb"]),
    ("pdb-runcall", "runcall()", "function", "pdb", "Вызов с отладкой.", "runcall(func, *args)", "pdb.runcall(f)", ["pdb"]),
    ("pdb-pm", "pm()", "function", "pdb", "Пост-мортем.", "pm()", "pdb.pm()", ["pdb"]),
    ("pdb-post-mortem", "post_mortem()", "function", "pdb", "Отладка исключения.", "post_mortem(tb)", "post_mortem()", ["pdb"]),

    # ---- timeit ----
    ("timeit-timeit", "timeit()", "function", "timeit", "Замер времени.", "timeit(stmt, setup, number)", "timeit('sum(range(10))')", ["timeit"]),
    ("timeit-repeat", "repeat()", "function", "timeit", "Несколько замеров.", "repeat(stmt, setup, repeat, number)", "repeat('pass')", ["timeit"]),
    ("timeit-Timer", "Timer", "class", "timeit", "Объект таймера.", "Timer(stmt, setup)", "Timer('pass')", ["timeit"]),

    # ---- profile ----
    ("profile-run", "cProfile.run()", "function", "profile", "Профилирует код.", "cProfile.run(stmt)", "cProfile.run('main()')", ["profile"]),
    ("profile-Profile", "cProfile.Profile", "class", "profile", "Объект профилировщика.", "Profile()", "cProfile.Profile()", ["profile"]),

    # ---- sysconfig ----
    ("sysconfig-get-paths", "get_paths()", "function", "sysconfig", "Пути установки.", "get_paths()", "get_paths()", ["sysconfig"]),
    ("sysconfig-get-config-var", "get_config_var()", "function", "sysconfig", "Конфиг-переменная.", "get_config_var(name)", "get_config_var('SOABI')", ["sysconfig"]),

    # ---- platform ----
    ("platform-system", "system()", "function", "platform", "ОС.", "system()", "system()", ["platform"]),
    ("platform-release", "release()", "function", "platform", "Версия ОС.", "release()", "release()", ["platform"]),
    ("platform-version", "version()", "function", "platform", "Версия ядра.", "version()", "version()", ["platform"]),
    ("platform-machine", "machine()", "function", "platform", "Архитектура.", "machine()", "machine()", ["platform"]),
    ("platform-processor", "processor()", "function", "platform", "Процессор.", "processor()", "processor()", ["platform"]),
    ("platform-python-version", "python_version()", "function", "platform", "Версия Python.", "python_version()", "python_version()", ["platform"]),
    ("platform-python-implementation", "python_implementation()", "function", "platform", "Реализация.", "python_implementation()", "python_implementation()", ["platform"]),
    ("platform-node", "node()", "function", "platform", "Имя хоста.", "node()", "node()", ["platform"]),
    ("platform-architecture", "architecture()", "function", "platform", "Архитектура бинарника.", "architecture()", "architecture()", ["platform"]),
    ("platform-uname", "uname()", "function", "platform", "Инфо о системе.", "uname()", "uname()", ["platform"]),

    # ---- locale ----
    ("locale-getlocale", "getlocale()", "function", "locale", "Текущая локаль.", "getlocale()", "getlocale()", ["locale"]),
    ("locale-setlocale", "setlocale()", "function", "locale", "Устанавливает локаль.", "setlocale(category, locale)", "setlocale(LC_ALL, '')", ["locale"]),
    ("locale-format-string", "format_string()", "function", "locale", "Форматирование с локалью.", "format_string(fmt, val)", "format_string('%.2f', 1.5)", ["locale"]),
    ("locale-currency", "currency()", "function", "locale", "Валюта.", "currency(val)", "currency(100)", ["locale"]),

    # ---- gettext ----
    ("gettext-gettext", "gettext()", "function", "gettext", "Переводит строку.", "gettext(msg)", "gettext('hi')", ["gettext"]),
    ("gettext-ngettext", "ngettext()", "function", "gettext", "Перевод с числом.", "ngettext(s1, s2, n)", "ngettext('item', 'items', 5)", ["gettext"]),
    ("gettext-install", "install()", "function", "gettext", "Устанавливает _().", "install(domain, localedir)", "install('app')", ["gettext"]),
    ("gettext-bindtextdomain", "bindtextdomain()", "function", "gettext", "Привязка домена к папке.", "bindtextdomain(domain, dir)", "bindtextdomain('app', 'locale')", ["gettext"]),

    # ---- codecs ----
    ("codecs-open", "open()", "function", "codecs", "Открывает с кодировкой.", "open(name, mode, encoding)", "codecs.open('f', encoding='utf-8')", ["codecs"]),
    ("codecs-encode", "encode()", "function", "codecs", "Кодирует строку.", "encode(obj, encoding)", "codecs.encode('x', 'utf-8')", ["codecs"]),
    ("codecs-decode", "decode()", "function", "codecs", "Декодирует байты.", "decode(obj, encoding)", "codecs.decode(b'x', 'utf-8')", ["codecs"]),
    ("codecs-lookup", "lookup()", "function", "codecs", "Инфо о кодировке.", "lookup(name)", "lookup('utf-8')", ["codecs"]),
    ("codecs-register", "register()", "function", "codecs", "Регистрирует кодек.", "register(search_function)", "register(sf)", ["codecs"]),

    # ---- unicodedata ----
    ("unicodedata-name", "name()", "function", "unicodedata", "Имя символа.", "name(chr)", "name('a')", ["unicodedata"]),
    ("unicodedata-lookup", "lookup()", "function", "unicodedata", "Символ по имени.", "lookup(name)", "lookup('LATIN SMALL LETTER A')", ["unicodedata"]),
    ("unicodedata-category", "category()", "function", "unicodedata", "Категория.", "category(chr)", "category('a')", ["unicodedata"]),
    ("unicodedata-bidirectional", "bidirectional()", "function", "unicodedata", "Направление.", "bidirectional(chr)", "bidirectional('a')", ["unicodedata"]),
    ("unicodedata-combining", "combining()", "function", "unicodedata", "Комбинирующий?", "combining(chr)", "combining('a')", ["unicodedata"]),
    ("unicodedata-normalize", "normalize()", "function", "unicodedata", "Нормализация.", "normalize(form, s)", "normalize('NFC', s)", ["unicodedata"]),
    ("unicodedata-decimal", "decimal()", "function", "unicodedata", "Десятичное значение.", "decimal(chr)", "decimal('5')", ["unicodedata"]),
    ("unicodedata-digit", "digit()", "function", "unicodedata", "Цифра.", "digit(chr)", "digit('5')", ["unicodedata"]),

    # ---- difflib ----
    ("difflib-SequenceMatcher", "SequenceMatcher", "class", "difflib", "Сравнивает.", "SequenceMatcher(None, a, b)", "SequenceMatcher(None, 'ab', 'ac')", ["difflib"]),
    ("difflib-Differ", "Differ", "class", "difflib", "Разница построчно.", "Differ()", "Differ()", ["difflib"]),
    ("difflib-unified-diff", "unified_diff()", "function", "difflib", "Unified diff.", "unified_diff(a, b)", "unified_diff(a, b)", ["difflib"]),
    ("difflib-ndiff", "ndiff()", "function", "difflib", "Построчный diff.", "ndiff(a, b)", "ndiff(a, b)", ["difflib"]),
    ("difflib-get-close-matches", "get_close_matches()", "function", "difflib", "Похожие строки.", "get_close_matches(w, p)", "get_close_matches('abc', ['ab', 'ac'])", ["difflib"]),
    ("difflib-HtmlDiff", "HtmlDiff", "class", "difflib", "HTML-diff.", "HtmlDiff()", "HtmlDiff()", ["difflib"]),

    # ---- textwrap ----
    ("textwrap-wrap", "wrap()", "function", "textwrap", "Переносит строку.", "wrap(text, width)", "wrap(text, 40)", ["textwrap"]),
    ("textwrap-fill", "fill()", "function", "textwrap", "Переносы + сборка.", "fill(text, width)", "fill(text, 40)", ["textwrap"]),
    ("textwrap-shorten", "shorten()", "function", "textwrap", "Сокращает.", "shorten(text, width)", "shorten(text, 20)", ["textwrap"]),
    ("textwrap-dedent", "dedent()", "function", "textwrap", "Убирает отступы.", "dedent(text)", "dedent('  x\\n  y')", ["textwrap"]),
    ("textwrap-indent", "indent()", "function", "textwrap", "Добавляет отступ.", "indent(text, prefix)", "indent(text, '  ')", ["textwrap"]),

    # ---- string ----
    ("string-Template", "Template", "class", "string", "Шаблон.", "Template(s)", "Template('$name')", ["string"]),
    ("string-Formatter", "Formatter", "class", "string", "Форматтер.", "Formatter()", "Formatter()", ["string"]),
    ("string-ascii-letters", "ascii_letters", "const", "string", "Все ASCII буквы.", "ascii_letters", "string.ascii_letters", ["string"]),
    ("string-digits", "digits", "const", "string", "Цифры.", "digits", "string.digits", ["string"]),
    ("string-punctuation", "punctuation", "const", "string", "Знаки пунктуации.", "punctuation", "string.punctuation", ["string"]),
    ("string-whitespace", "whitespace", "const", "string", "Пробельные.", "whitespace", "string.whitespace", ["string"]),
    ("string-hexdigits", "hexdigits", "const", "string", "Hex-цифры.", "hexdigits", "string.hexdigits", ["string"]),
    ("string-octdigits", "octdigits", "const", "string", "Oct-цифры.", "octdigits", "string.octdigits", ["string"]),

    # ---- glob ----
    ("glob-glob", "glob()", "function", "glob", "Поиск по шаблону.", "glob(pattern)", "glob('*.py')", ["glob"]),
    ("glob-iglob", "iglob()", "function", "glob", "Итератор поиска.", "iglob(pattern)", "iglob('*.py')", ["glob"]),
    ("glob-escape", "escape()", "function", "glob", "Экранирование.", "escape(path)", "escape('dir/')", ["glob"]),

    # ---- fnmatch ----
    ("fnmatch-fnmatch", "fnmatch()", "function", "fnmatch", "Соответствие шаблону.", "fnmatch(name, pat)", "fnmatch('a.txt', '*.txt')", ["fnmatch"]),
    ("fnmatch-filter", "filter()", "function", "fnmatch", "Фильтр имён.", "filter(names, pat)", "filter(names, '*.py')", ["fnmatch"]),
    ("fnmatch-translate", "translate()", "function", "fnmatch", "Шаблон → regex.", "translate(pat)", "translate('*.txt')", ["fnmatch"]),

    # ---- linecache ----
    ("linecache-getline", "getline()", "function", "linecache", "Читает строку файла.", "getline(filename, lineno)", "getline('f.py', 1)", ["linecache"]),
    ("linecache-clearcache", "clearcache()", "function", "linecache", "Очищает кэш.", "clearcache()", "clearcache()", ["linecache"]),

    # ---- tokenize ----
    ("tokenize-tokenize", "tokenize()", "function", "tokenize", "Токенизирует.", "tokenize(readline)", "tokenize(f.readline)", ["tokenize"]),
    ("tokenize-untokenize", "untokenize()", "function", "tokenize", "Из токенов в строку.", "untokenize(iter)", "untokenize(tokens)", ["tokenize"]),

    # ---- keyword ----
    ("keyword-kwlist", "kwlist", "const", "keyword", "Ключевые слова.", "kwlist", "keyword.kwlist", ["keyword"]),
    ("keyword-iskeyword", "iskeyword()", "function", "keyword", "Ключевое слово?", "iskeyword(s)", "keyword.iskeyword('if')", ["keyword"]),
    ("keyword-softkwlist", "softkwlist", "const", "keyword", "Мягкие ключевые.", "softkwlist", "keyword.softkwlist", ["keyword"]),

    # ---- io ----
    ("io-StringIO", "StringIO", "class", "io", "Строка как файл.", "StringIO(s)", "StringIO('hi')", ["io"]),
    ("io-BytesIO", "BytesIO", "class", "io", "Байты как файл.", "BytesIO(b)", "BytesIO(b'hi')", ["io"]),
    ("io-FileIO", "FileIO", "class", "io", "Низкоуровневый файл.", "FileIO(name, mode)", "FileIO('f', 'r')", ["io"]),
    ("io-TextIOWrapper", "TextIOWrapper", "class", "io", "Текст поверх потока.", "TextIOWrapper(buf)", "TextIOWrapper(buf)", ["io"]),
    ("io-BufferedReader", "BufferedReader", "class", "io", "Буфер чтения.", "BufferedReader(raw)", "BufferedReader(raw)", ["io"]),
    ("io-BufferedWriter", "BufferedWriter", "class", "io", "Буфер записи.", "BufferedWriter(raw)", "BufferedWriter(raw)", ["io"]),

    # ---- signal ----
    ("signal-signal", "signal()", "function", "signal", "Обработчик сигнала.", "signal(signum, handler)", "signal(SIGINT, h)", ["signal"]),
    ("signal-alarm", "alarm()", "function", "signal", "Таймер сигнала.", "alarm(secs)", "alarm(5)", ["signal"]),
    ("signal-pause", "pause()", "function", "signal", "Ждёт сигнал.", "pause()", "pause()", ["signal"]),
    ("signal-raise-signal", "raise_signal()", "function", "signal", "Шлёт сигнал себе.", "raise_signal(signum)", "raise_signal(SIGINT)", ["signal"]),
    ("signal-SIGINT", "SIGINT", "const", "signal", "Сигнал Ctrl+C.", "SIGINT", "signal.SIGINT", ["signal"]),
    ("signal-SIGTERM", "SIGTERM", "const", "signal", "Сигнал завершения.", "SIGTERM", "signal.SIGTERM", ["signal"]),

    # ---- mmap ----
    ("mmap-mmap", "mmap()", "class", "mmap", "Файл в память.", "mmap(fileno, length)", "mmap(f.fileno(), 0)", ["mmap"]),

    # ---- ctypes ----
    ("ctypes-CDLL", "CDLL", "class", "ctypes", "Загружает .so/.dll.", "CDLL(name)", "CDLL('libc.so')", ["ctypes"]),
    ("ctypes-WinDLL", "WinDLL", "class", "ctypes", "Windows DLL.", "WinDLL(name)", "WinDLL('kernel32')", ["ctypes"]),
    ("ctypes-Structure", "Structure", "class", "ctypes", "C-структура.", "class S(Structure):", "Structure", ["ctypes"]),
    ("ctypes-Union", "Union", "class", "ctypes", "C-объединение.", "class U(Union):", "Union", ["ctypes"]),
    ("ctypes-c-int", "c_int", "class", "ctypes", "C int.", "c_int(v)", "c_int(1)", ["ctypes"]),
    ("ctypes-c-float", "c_float", "class", "ctypes", "C float.", "c_float(v)", "c_float(1.0)", ["ctypes"]),
    ("ctypes-c-char-p", "c_char_p", "class", "ctypes", "C char*.", "c_char_p(s)", "c_char_p(b's')", ["ctypes"]),
    ("ctypes-POINTER", "POINTER()", "function", "ctypes", "Указатель.", "POINTER(type)", "POINTER(c_int)", ["ctypes"]),
    ("ctypes-byref", "byref()", "function", "ctypes", "Ссылка.", "byref(obj)", "byref(v)", ["ctypes"]),
    ("ctypes-pointer", "pointer()", "function", "ctypes", "Создаёт указатель.", "pointer(obj)", "pointer(v)", ["ctypes"]),

    # ---- multiprocessing ----
    ("multiprocessing-Process", "Process", "class", "multiprocessing", "Процесс.", "Process(target=func)", "Process(target=f)", ["multiprocessing"]),
    ("multiprocessing-Pool", "Pool", "class", "multiprocessing", "Пул процессов.", "Pool(n)", "Pool(4)", ["multiprocessing"]),
    ("multiprocessing-Queue", "Queue", "class", "multiprocessing", "Очередь процессов.", "Queue()", "Queue()", ["multiprocessing"]),
    ("multiprocessing-Pipe", "Pipe()", "function", "multiprocessing", "Канал между процессами.", "Pipe()", "Pipe()", ["multiprocessing"]),
    ("multiprocessing-Lock", "Lock", "class", "multiprocessing", "Блокировка.", "Lock()", "Lock()", ["multiprocessing"]),
    ("multiprocessing-Value", "Value()", "function", "multiprocessing", "Общее значение.", "Value(typecode, v)", "Value('i', 0)", ["multiprocessing"]),
    ("multiprocessing-Array", "Array()", "function", "multiprocessing", "Общий массив.", "Array(typecode, seq)", "Array('i', 10)", ["multiprocessing"]),
    ("multiprocessing-Manager", "Manager", "class", "multiprocessing", "Менеджер ресурсов.", "Manager()", "Manager()", ["multiprocessing"]),

    # ---- threading ----
    ("threading-Thread", "Thread", "class", "threading", "Поток.", "Thread(target=func)", "Thread(target=f)", ["threading"]),
    ("threading-Lock", "Lock", "class", "threading", "Блокировка.", "Lock()", "Lock()", ["threading"]),
    ("threading-RLock", "RLock", "class", "threading", "Рекурсивная блокировка.", "RLock()", "RLock()", ["threading"]),
    ("threading-Semaphore", "Semaphore", "class", "threading", "Семафор.", "Semaphore()", "Semaphore(5)", ["threading"]),
    ("threading-BoundedSemaphore", "BoundedSemaphore", "class", "threading", "Ограниченный семафор.", "BoundedSemaphore(n)", "BoundedSemaphore(5)", ["threading"]),
    ("threading-Event", "Event", "class", "threading", "Событие.", "Event()", "Event()", ["threading"]),
    ("threading-Condition", "Condition", "class", "threading", "Условие.", "Condition()", "Condition()", ["threading"]),
    ("threading-Barrier", "Barrier", "class", "threading", "Барьер.", "Barrier(parties)", "Barrier(3)", ["threading"]),
    ("threading-Timer", "Timer", "class", "threading", "Таймер.", "Timer(interval, func)", "Timer(1, f)", ["threading"]),
    ("threading-local", "local", "class", "threading", "Локаль потока.", "local()", "local()", ["threading"]),
    ("threading-current-thread", "current_thread()", "function", "threading", "Текущий поток.", "current_thread()", "current_thread()", ["threading"]),
    ("threading-enumerate", "enumerate()", "function", "threading", "Список потоков.", "enumerate()", "enumerate()", ["threading"]),
    ("threading-active-count", "active_count()", "function", "threading", "Число потоков.", "active_count()", "active_count()", ["threading"]),
    ("threading-get-ident", "get_ident()", "function", "threading", "ID текущего потока.", "get_ident()", "get_ident()", ["threading"]),

    # ---- concurrent.futures ----
    ("concurrent-ThreadPoolExecutor", "ThreadPoolExecutor", "class", "concurrent", "Пул потоков.", "ThreadPoolExecutor(n)", "ThreadPoolExecutor(4)", ["concurrent"]),
    ("concurrent-ProcessPoolExecutor", "ProcessPoolExecutor", "class", "concurrent", "Пул процессов.", "ProcessPoolExecutor(n)", "ProcessPoolExecutor(4)", ["concurrent"]),
    ("concurrent-Future", "Future", "class", "concurrent", "Обещание результата.", "Future()", "...", ["concurrent"]),
    ("concurrent-as-completed", "as_completed()", "function", "concurrent", "Итератор завершённых.", "as_completed(futures)", "as_completed(futures)", ["concurrent"]),
    ("concurrent-wait", "wait()", "function", "concurrent", "Ждёт futures.", "wait(futures)", "wait(futures)", ["concurrent"]),

    # ---- asyncio ----
    ("asyncio-run", "run()", "function", "asyncio", "Запуск корутины.", "run(coro)", "run(main())", ["asyncio"]),
    ("asyncio-sleep", "sleep()", "coroutine", "asyncio", "Асинхронная пауза.", "await sleep(secs)", "await sleep(1)", ["asyncio"]),
    ("asyncio-gather", "gather()", "coroutine", "asyncio", "Запуск вместе.", "await gather(*coros)", "await gather(a(), b())", ["asyncio"]),
    ("asyncio-wait", "wait()", "coroutine", "asyncio", "Ждёт futures.", "await wait(fs)", "await wait(fs)", ["asyncio"]),
    ("asyncio-create-task", "create_task()", "function", "asyncio", "Создаёт задачу.", "create_task(coro)", "create_task(main())", ["asyncio"]),
    ("asyncio-Task", "Task", "class", "asyncio", "Объект задачи.", "Task(coro)", "Task(coro)", ["asyncio"]),
    ("asyncio-Event", "Event", "class", "asyncio", "Async событие.", "Event()", "Event()", ["asyncio"]),
    ("asyncio-Lock", "Lock", "class", "asyncio", "Async блокировка.", "Lock()", "Lock()", ["asyncio"]),
    ("asyncio-Semaphore", "Semaphore", "class", "asyncio", "Async семафор.", "Semaphore()", "Semaphore(5)", ["asyncio"]),
    ("asyncio-Queue", "Queue", "class", "asyncio", "Async очередь.", "Queue()", "Queue()", ["asyncio"]),
    ("asyncio-shield", "shield()", "function", "asyncio", "Защищает от отмены.", "shield(coro)", "shield(task)", ["asyncio"]),
    ("asyncio-timeout", "timeout()", "contextmanager", "asyncio", "Тайм-аут.", "async with timeout(t):", "async with timeout(1):", ["asyncio"]),
    ("asyncio-to-thread", "to_thread()", "coroutine", "asyncio", "Запуск в потоке.", "await to_thread(func)", "await to_thread(block)", ["asyncio"]),
    ("asyncio-open-connection", "open_connection()", "coroutine", "asyncio", "TCP-клиент.", "await open_connection(h, p)", "await open_connection('h', 80)", ["asyncio"]),
    ("asyncio-start-server", "start_server()", "coroutine", "asyncio", "TCP-сервер.", "await start_server(cb, h, p)", "await start_server(cb, '0', 8000)", ["asyncio"]),

    # ---- selectors ----
    ("selectors-DefaultSelector", "DefaultSelector", "class", "selectors", "Селектор.", "DefaultSelector()", "DefaultSelector()", ["selectors"]),
    ("selectors-EVENT-READ", "EVENT_READ", "const", "selectors", "Читаемость.", "EVENT_READ", "selectors.EVENT_READ", ["selectors"]),
    ("selectors-EVENT-WRITE", "EVENT_WRITE", "const", "selectors", "Записываемость.", "EVENT_WRITE", "selectors.EVENT_WRITE", ["selectors"]),

    # ---- queue ----
    ("queue-Queue", "Queue", "class", "queue", "FIFO очередь.", "Queue(maxsize)", "Queue()", ["queue"]),
    ("queue-LifoQueue", "LifoQueue", "class", "queue", "LIFO очередь (стек).", "LifoQueue(maxsize)", "LifoQueue()", ["queue"]),
    ("queue-PriorityQueue", "PriorityQueue", "class", "queue", "Приоритетная очередь.", "PriorityQueue(maxsize)", "PriorityQueue()", ["queue"]),
    ("queue-SimpleQueue", "SimpleQueue", "class", "queue", "Простая очередь.", "SimpleQueue()", "SimpleQueue()", ["queue"]),
    ("queue-Empty", "Empty", "exception", "queue", "Очередь пуста.", "raise Empty", "Empty", ["queue"]),
    ("queue-Full", "Full", "exception", "queue", "Очередь полна.", "raise Full", "Full", ["queue"]),

    # ---- sched ----
    ("sched-scheduler", "scheduler", "class", "sched", "Планировщик.", "scheduler()", "scheduler()", ["sched"]),

    # ---- atexit ----
    ("atexit-register", "register()", "function", "atexit", "Регистрирует выход.", "register(func, *args)", "register(cleanup)", ["atexit"]),
    ("atexit-unregister", "unregister()", "function", "atexit", "Убирает регистрацию.", "unregister(func)", "unregister(cleanup)", ["atexit"]),

    # ---- gc ----
    ("gc-collect", "collect()", "function", "gc", "Собирает мусор.", "collect()", "collect()", ["gc"]),
    ("gc-enable", "enable()", "function", "gc", "Включает GC.", "enable()", "enable()", ["gc"]),
    ("gc-disable", "disable()", "function", "gc", "Отключает GC.", "disable()", "disable()", ["gc"]),
    ("gc-isenabled", "isenabled()", "function", "gc", "Включён?", "isenabled()", "isenabled()", ["gc"]),
    ("gc-get-stats", "get_stats()", "function", "gc", "Статистика.", "get_stats()", "get_stats()", ["gc"]),
    ("gc-get-count", "get_count()", "function", "gc", "Счётчики.", "get_count()", "get_count()", ["gc"]),
    ("gc-set-threshold", "set_threshold()", "function", "gc", "Пороги сбора.", "set_threshold(*t)", "set_threshold(700, 10, 10)", ["gc"]),

    # ---- tracemalloc ----
    ("tracemalloc-start", "start()", "function", "tracemalloc", "Старт трассировки.", "start()", "start()", ["tracemalloc"]),
    ("tracemalloc-stop", "stop()", "function", "tracemalloc", "Остановка.", "stop()", "stop()", ["tracemalloc"]),
    ("tracemalloc-take-snapshot", "take_snapshot()", "function", "tracemalloc", "Снимок памяти.", "take_snapshot()", "take_snapshot()", ["tracemalloc"]),
    ("tracemalloc-get-traced-memory", "get_traced_memory()", "function", "tracemalloc", "Текущая память.", "get_traced_memory()", "get_traced_memory()", ["tracemalloc"]),

    # ---- faulthandler ----
    ("faulthandler-enable", "enable()", "function", "faulthandler", "Включает обработчик.", "enable()", "enable()", ["faulthandler"]),
    ("faulthandler-disable", "disable()", "function", "faulthandler", "Отключает.", "disable()", "disable()", ["faulthandler"]),
    ("faulthandler-dump-traceback", "dump_traceback()", "function", "faulthandler", "Дамп стека.", "dump_traceback()", "dump_traceback()", ["faulthandler"]),
    ("faulthandler-register", "register()", "function", "faulthandler", "Сигнал → дамп.", "register(signum)", "register(signal.SIGUSR1)", ["faulthandler"]),

    # ---- webbrowser ----
    ("webbrowser-open", "open()", "function", "webbrowser", "Открывает URL.", "open(url)", "webbrowser.open('https://...')", ["webbrowser"]),
    ("webbrowser-open-new", "open_new()", "function", "webbrowser", "В новом окне.", "open_new(url)", "open_new('https://...')", ["webbrowser"]),
    ("webbrowser-open-new-tab", "open_new_tab()", "function", "webbrowser", "В новой вкладке.", "open_new_tab(url)", "open_new_tab('https://...')", ["webbrowser"]),
    ("webbrowser-get", "get()", "function", "webbrowser", "Получает браузер.", "get(name)", "get('chrome')", ["webbrowser"]),
    ("webbrowser-register", "register()", "function", "webbrowser", "Регистрирует браузер.", "register(name, klass)", "register('br', cls)", ["webbrowser"]),

    # ---- socket ----
    ("socket-socket", "socket()", "class", "socket", "Создаёт сокет.", "socket(family, type)", "socket(AF_INET, SOCK_STREAM)", ["socket"]),
    ("socket-AF-INET", "AF_INET", "const", "socket", "IPv4.", "AF_INET", "AF_INET", ["socket"]),
    ("socket-AF-INET6", "AF_INET6", "const", "socket", "IPv6.", "AF_INET6", "AF_INET6", ["socket"]),
    ("socket-SOCK-STREAM", "SOCK_STREAM", "const", "socket", "TCP.", "SOCK_STREAM", "SOCK_STREAM", ["socket"]),
    ("socket-SOCK-DGRAM", "SOCK_DGRAM", "const", "socket", "UDP.", "SOCK_DGRAM", "SOCK_DGRAM", ["socket"]),
    ("socket-gethostname", "gethostname()", "function", "socket", "Имя хоста.", "gethostname()", "gethostname()", ["socket"]),
    ("socket-gethostbyname", "gethostbyname()", "function", "socket", "IP по имени.", "gethostbyname(name)", "gethostbyname('localhost')", ["socket"]),
    ("socket-getfqdn", "getfqdn()", "function", "socket", "Полное имя хоста.", "getfqdn()", "getfqdn()", ["socket"]),
    ("socket-create-connection", "create_connection()", "function", "socket", "Создаёт TCP.", "create_connection((h, p))", "create_connection(('h', 80))", ["socket"]),
    ("socket-inet-aton", "inet_aton()", "function", "socket", "IP → 4 байта.", "inet_aton(ip)", "inet_aton('1.2.3.4')", ["socket"]),
    ("socket-inet-ntoa", "inet_ntoa()", "function", "socket", "4 байта → IP.", "inet_ntoa(packed)", "inet_ntoa(b'\\x01\\x02\\x03\\x04')", ["socket"]),

    # ---- ssl ----
    ("ssl-create-default-context", "create_default_context()", "function", "ssl", "Стандартный SSL.", "create_default_context()", "create_default_context()", ["ssl"]),
    ("ssl-wrap-socket", "wrap_socket()", "method", "ssl", "Оборачивает в SSL.", "wrap_socket(sock)", "ctx.wrap_socket(s)", ["ssl"]),
    ("ssl-SSLContext", "SSLContext", "class", "ssl", "Контекст SSL.", "SSLContext(protocol)", "SSLContext()", ["ssl"]),
    ("ssl-CERT-REQUIRED", "CERT_REQUIRED", "const", "ssl", "Обязательный сертификат.", "CERT_REQUIRED", "ssl.CERT_REQUIRED", ["ssl"]),

    # ---- urllib ----
    ("urllib-urlopen", "urllib.request.urlopen()", "function", "urllib", "Открывает URL.", "urlopen(url)", "urlopen('https://...')", ["urllib"]),
    ("urllib-urlretrieve", "urllib.request.urlretrieve()", "function", "urllib", "Скачивает URL.", "urlretrieve(url, path)", "urlretrieve('u', 'f')", ["urllib"]),
    ("urllib-urlparse", "urllib.parse.urlparse()", "function", "urllib", "Разбирает URL.", "urlparse(url)", "urlparse('https://a/b')", ["urllib"]),
    ("urllib-quote", "urllib.parse.quote()", "function", "urllib", "URL-encode.", "quote(s)", "quote('a b')", ["urllib"]),
    ("urllib-unquote", "urllib.parse.unquote()", "function", "urllib", "URL-decode.", "unquote(s)", "unquote('a%20b')", ["urllib"]),
    ("urllib-HTTPError", "HTTPError", "exception", "urllib", "Ошибка HTTP.", "HTTPError", "HTTPError", ["urllib"]),

    # ---- http.server ----
    ("http-server-HTTPServer", "HTTPServer", "class", "http-server", "HTTP-сервер.", "HTTPServer((h, p), handler)", "HTTPServer(('', 8000), H)", ["http-server"]),
    ("http-server-BaseHTTPRequestHandler", "BaseHTTPRequestHandler", "class", "http-server", "Базовый обработчик.", "class H(BaseHTTPRequestHandler):", "...", ["http-server"]),
    ("http-server-SimpleHTTPRequestHandler", "SimpleHTTPRequestHandler", "class", "http-server", "Статический сервер.", "SimpleHTTPRequestHandler", "SimpleHTTPRequestHandler", ["http-server"]),

    # ---- http.client ----
    ("http-client-HTTPConnection", "HTTPConnection", "class", "http-client", "HTTP-клиент.", "HTTPConnection(host)", "HTTPConnection('h')", ["http-client"]),
    ("http-client-HTTPSConnection", "HTTPSConnection", "class", "http-client", "HTTPS-клиент.", "HTTPSConnection(host)", "HTTPSConnection('h')", ["http-client"]),
    ("http-client-HTTPResponse", "HTTPResponse", "class", "http-client", "Ответ.", "HTTPResponse", "...", ["http-client"]),

    # ---- http.cookies ----
    ("http-cookies-SimpleCookie", "SimpleCookie", "class", "http-cookies", "Куки.", "SimpleCookie()", "SimpleCookie()", ["http-cookies"]),
    ("http-cookies-Morsel", "Morsel", "class", "http-cookies", "Одна кука.", "Morsel", "Morsel", ["http-cookies"]),

    # ---- html.parser ----
    ("html-parser-HTMLParser", "HTMLParser", "class", "html-parser", "Парсер HTML.", "class P(HTMLParser):", "HTMLParser()", ["html-parser"]),

    # ---- xml.etree ----
    ("xml-Element", "Element", "class", "xml", "Элемент XML.", "Element(tag)", "Element('root')", ["xml"]),
    ("xml-SubElement", "SubElement()", "function", "xml", "Дочерний элемент.", "SubElement(parent, tag)", "SubElement(root, 'a')", ["xml"]),
    ("xml-parse", "parse()", "function", "xml", "Парсит файл.", "parse(file)", "parse('a.xml')", ["xml"]),
    ("xml-tostring", "tostring()", "function", "xml", "Элемент → строка.", "tostring(elem)", "tostring(root)", ["xml"]),
    ("xml-fromstring", "fromstring()", "function", "xml", "Строка → элемент.", "fromstring(s)", "fromstring('<a/>')", ["xml"]),
    ("xml-ElementTree", "ElementTree", "class", "xml", "Дерево XML.", "ElementTree(elem)", "ElementTree(root)", ["xml"]),

    # ---- xml.dom ----
    ("xml-dom-minidom", "xml.dom.minidom", "module", "xml", "DOM-парсер.", "minidom.parse(f)", "minidom.parseString(s)", ["xml"]),

    # ---- xml.sax ----
    ("xml-sax-parse", "parse()", "function", "xml", "SAX-парсинг.", "parse(source, handler)", "parse('a.xml', h)", ["xml"]),
    ("xml-sax-make-parser", "make_parser()", "function", "xml", "Создаёт парсер.", "make_parser()", "make_parser()", ["xml"]),

    # ---- email ----
    ("email-EmailMessage", "EmailMessage", "class", "email", "Сообщение.", "EmailMessage()", "EmailMessage()", ["email"]),
    ("email-message-from-string", "message_from_string()", "function", "email", "Из строки.", "message_from_string(s)", "message_from_string(s)", ["email"]),
    ("email-message-from-bytes", "message_from_bytes()", "function", "email", "Из байт.", "message_from_bytes(b)", "message_from_bytes(b)", ["email"]),
    ("email-MIMEText", "MIMEText", "class", "email", "Текстовое письмо.", "MIMEText(text)", "MIMEText('hi')", ["email"]),
    ("email-MIMEMultipart", "MIMEMultipart", "class", "email", "Многокомпонентное.", "MIMEMultipart()", "MIMEMultipart()", ["email"]),

    # ---- mailbox ----
    ("mailbox-Maildir", "Maildir", "class", "mailbox", "Maildir ящик.", "Maildir(path)", "Maildir('~/Maildir')", ["mailbox"]),
    ("mailbox-mbox", "mbox", "class", "mailbox", "mbox ящик.", "mbox(path)", "mbox('mail.mbox')", ["mailbox"]),
    ("mailbox-MH", "MH", "class", "mailbox", "MH ящик.", "MH(path)", "MH('~/mh')", ["mailbox"]),

    # ---- mimetypes ----
    ("mimetypes-guess-type", "guess_type()", "function", "mimetypes", "MIME по имени.", "guess_type(url)", "guess_type('a.png')", ["mimetypes"]),
    ("mimetypes-add-type", "add_type()", "function", "mimetypes", "Добавляет MIME.", "add_type(type, ext)", "add_type('a/b', '.x')", ["mimetypes"]),
    ("mimetypes-init", "init()", "function", "mimetypes", "Инициализация.", "init()", "init()", ["mimetypes"]),

    # ---- ftplib / poplib / imaplib / smtplib ----
    ("ftplib-FTP", "FTP", "class", "ftplib", "FTP-клиент.", "FTP(host)", "FTP('ftp.example.com')", ["ftplib"]),
    ("poplib-POP3", "POP3", "class", "poplib", "POP3-клиент.", "POP3(host)", "POP3('pop.example.com')", ["poplib"]),
    ("imaplib-IMAP4", "IMAP4", "class", "imaplib", "IMAP-клиент.", "IMAP4(host)", "IMAP4('imap.example.com')", ["imaplib"]),
    ("smtplib-SMTP", "SMTP", "class", "smtplib", "SMTP-клиент.", "SMTP(host)", "SMTP('smtp.example.com')", ["smtplib"]),

    # ---- uuid ----
    ("uuid-uuid1", "uuid1()", "function", "uuid", "UUID из MAC и времени.", "uuid1()", "uuid1()", ["uuid"]),
    ("uuid-uuid3", "uuid3()", "function", "uuid", "UUID по MD5.", "uuid3(namespace, name)", "uuid3(NAMESPACE_DNS, 'x')", ["uuid"]),
    ("uuid-uuid4", "uuid4()", "function", "uuid", "Случайный UUID.", "uuid4()", "uuid4()", ["uuid"]),
    ("uuid-uuid5", "uuid5()", "function", "uuid", "UUID по SHA-1.", "uuid5(namespace, name)", "uuid5(NAMESPACE_DNS, 'x')", ["uuid"]),
    ("uuid-UUID", "UUID", "class", "uuid", "Объект UUID.", "UUID(hex)", "UUID('...')", ["uuid"]),

    # ---- socketserver ----
    ("socketserver-TCPServer", "TCPServer", "class", "socketserver", "TCP-сервер.", "TCPServer((h, p), handler)", "TCPServer(('', 8000), H)", ["socketserver"]),
    ("socketserver-UDPServer", "UDPServer", "class", "socketserver", "UDP-сервер.", "UDPServer((h, p), handler)", "UDPServer(('', 8000), H)", ["socketserver"]),
    ("socketserver-ThreadingMixIn", "ThreadingMixIn", "class", "socketserver", "Потоки.", "class S(ThreadingMixIn, TCPServer):", "...", ["socketserver"]),
    ("socketserver-ForkingMixIn", "ForkingMixIn", "class", "socketserver", "Процессы.", "class S(ForkingMixIn, TCPServer):", "...", ["socketserver"]),
    ("socketserver-BaseRequestHandler", "BaseRequestHandler", "class", "socketserver", "Базовый обработчик.", "class H(BaseRequestHandler):", "...", ["socketserver"]),
    ("socketserver-StreamRequestHandler", "StreamRequestHandler", "class", "socketserver", "Потоковый.", "class H(StreamRequestHandler):", "...", ["socketserver"]),

    # ---- xmlrpc ----
    ("xmlrpc-server", "xmlrpc.server", "module", "xmlrpc", "XML-RPC сервер.", "SimpleXMLRPCServer((h, p))", "...", ["xmlrpc"]),
    ("xmlrpc-client", "xmlrpc.client", "module", "xmlrpc", "XML-RPC клиент.", "ServerProxy(url)", "ServerProxy('http://...')", ["xmlrpc"]),

    # ---- wsgiref ----
    ("wsgiref-simple-server", "wsgiref.simple_server", "module", "wsgiref", "WSGI-сервер.", "make_server(h, p, app)", "make_server('', 8000, app)", ["wsgiref"]),

    # ---- cmd ----
    ("cmd-Cmd", "Cmd", "class", "cmd", "Командная строка.", "class C(Cmd):", "Cmd()", ["cmd"]),

    # ---- shlex ----
    ("shlex-split", "split()", "function", "shlex", "Разбор shell.", "split(s)", "split('a \"b c\"')", ["shlex"]),
    ("shlex-quote", "quote()", "function", "shlex", "Экранирование.", "quote(s)", "quote('a b')", ["shlex"]),
    ("shlex-join", "join()", "function", "shlex", "Сборка команды.", "join(args)", "join(['a', 'b c'])", ["shlex"]),

    # ---- filecmp ----
    ("filecmp-cmp", "cmp()", "function", "filecmp", "Сравнивает файлы.", "cmp(f1, f2)", "cmp('a', 'b')", ["filecmp"]),
    ("filecmp-dircmp", "dircmp", "class", "filecmp", "Сравнивает папки.", "dircmp(d1, d2)", "dircmp('a', 'b')", ["filecmp"]),

    # ---- stat ----
    ("stat-S-IRUSR", "S_IRUSR", "const", "stat", "Чтение для владельца.", "S_IRUSR", "S_IRUSR", ["stat"]),
    ("stat-S-IWUSR", "S_IWUSR", "const", "stat", "Запись для владельца.", "S_IWUSR", "S_IWUSR", ["stat"]),
    ("stat-S-IXUSR", "S_IXUSR", "const", "stat", "Выполнение для владельца.", "S_IXUSR", "S_IXUSR", ["stat"]),
    ("stat-filemode", "filemode()", "function", "stat", "Права как строка.", "filemode(mode)", "filemode(st.st_mode)", ["stat"]),
    ("stat-S-ISREG", "S_ISREG()", "function", "stat", "Это файл?", "S_ISREG(mode)", "S_ISREG(st.st_mode)", ["stat"]),
    ("stat-S-ISDIR", "S_ISDIR()", "function", "stat", "Это папка?", "S_ISDIR(mode)", "S_ISDIR(st.st_mode)", ["stat"]),

    # ---- pickle ----
    ("pickle-dump", "dump()", "function", "pickle", "Пишет в файл.", "dump(obj, f)", "dump(obj, f)", ["pickle"]),
    ("pickle-dumps", "dumps()", "function", "pickle", "Сериализует.", "dumps(obj)", "dumps(obj)", ["pickle"]),
    ("pickle-load", "load()", "function", "pickle", "Читает из файла.", "load(f)", "load(f)", ["pickle"]),
    ("pickle-loads", "loads()", "function", "pickle", "Десериализует.", "loads(b)", "loads(b)", ["pickle"]),

    # ---- shelve ----
    ("shelve-open", "open()", "function", "shelve", "Открывает shelve.", "open(name)", "shelve.open('db')", ["shelve"]),

    # ---- marshal ----
    ("marshal-dump", "dump()", "function", "marshal", "Пишет объект.", "dump(obj, f)", "dump(obj, f)", ["marshal"]),
    ("marshal-dumps", "dumps()", "function", "marshal", "Сериализует.", "dumps(obj)", "dumps(obj)", ["marshal"]),
    ("marshal-load", "load()", "function", "marshal", "Читает.", "load(f)", "load(f)", ["marshal"]),
    ("marshal-loads", "loads()", "function", "marshal", "Десериализует.", "loads(b)", "loads(b)", ["marshal"]),

    # ---- dbm ----
    ("dbm-open", "open()", "function", "dbm", "Открывает db.", "open(name, flag)", "dbm.open('db', 'c')", ["dbm"]),
    ("dbm-whichdb", "whichdb()", "function", "dbm", "Тип БД.", "whichdb(name)", "whichdb('db')", ["dbm"]),

    # ---- sqlite3 ----
    ("sqlite3-connect", "connect()", "function", "sqlite3", "Подключение.", "connect(database)", "connect('a.db')", ["sqlite3"]),
    ("sqlite3-Connection", "Connection", "class", "sqlite3", "Соединение.", "Connection(db)", "Connection('a.db')", ["sqlite3"]),
    ("sqlite3-Cursor", "Cursor", "class", "sqlite3", "Курсор.", "conn.cursor()", "conn.cursor()", ["sqlite3"]),
    ("sqlite3-Row", "Row", "class", "sqlite3", "Строка как dict.", "conn.row_factory = Row", "Row", ["sqlite3"]),
    ("sqlite3-OperationalError", "OperationalError", "exception", "sqlite3", "Ошибка операции.", "OperationalError", "OperationalError", ["sqlite3"]),
    ("sqlite3-IntegrityError", "IntegrityError", "exception", "sqlite3", "Нарушение целостности.", "IntegrityError", "IntegrityError", ["sqlite3"]),

    # ---- csv ----
    ("csv-reader", "reader()", "function", "csv", "Читает CSV.", "reader(f)", "reader(f)", ["csv"]),
    ("csv-writer", "writer()", "function", "csv", "Пишет CSV.", "writer(f)", "writer(f)", ["csv"]),
    ("csv-DictReader", "DictReader", "class", "csv", "Читает как dict.", "DictReader(f)", "DictReader(f)", ["csv"]),
    ("csv-DictWriter", "DictWriter", "class", "csv", "Пишет из dict.", "DictWriter(f, fieldnames)", "DictWriter(f, ['a'])", ["csv"]),

    # ---- json ----
    ("json-dump", "dump()", "function", "json", "Пишет JSON в файл.", "dump(obj, f)", "dump(obj, f)", ["json"]),
    ("json-dumps", "dumps()", "function", "json", "Сериализует.", "dumps(obj)", "dumps({'a': 1})", ["json"]),
    ("json-load", "load()", "function", "json", "Читает JSON из файла.", "load(f)", "load(f)", ["json"]),
    ("json-loads", "loads()", "function", "json", "Десериализует.", "loads(s)", "loads('{\"a\":1}')", ["json"]),

    # ---- tomllib ----
    ("tomllib-load", "load()", "function", "tomllib", "Читает TOML из файла.", "load(f)", "load(f)", ["tomllib"]),
    ("tomllib-loads", "loads()", "function", "tomllib", "Парсит TOML.", "loads(s)", "loads('[a]\\nb=1')", ["tomllib"]),

    # ---- plistlib ----
    ("plistlib-load", "load()", "function", "plistlib", "Читает plist.", "load(f)", "load(f)", ["plistlib"]),
    ("plistlib-loads", "loads()", "function", "plistlib", "Парсит plist.", "loads(b)", "loads(b)", ["plistlib"]),
    ("plistlib-dump", "dump()", "function", "plistlib", "Пишет plist.", "dump(obj, f)", "dump(obj, f)", ["plistlib"]),
    ("plistlib-dumps", "dumps()", "function", "plistlib", "Сериализует.", "dumps(obj)", "dumps(obj)", ["plistlib"]),
]


def default_returns(t):
    return {
        "method": "Зависит от метода.",
        "function": "Зависит от функции.",
        "class": "Объект класса.",
        "decorator": "Декоратор.",
        "contextmanager": "Контекстный менеджер.",
        "coroutine": "Корутина.",
        "attr": "Атрибут.",
        "const": "Константа.",
        "exception": "Объект исключения.",
        "module": "Модуль.",
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


def main():
    payload = None
    for p in INPUT_PATHS:
        if p.exists():
            payload = json.loads(p.read_text(encoding="utf-8"))
            break
    if payload is None:
        print("Сначала запусти build_all.py")
        return

    if isinstance(payload, list):
        payload = {"meta": {}, "entries": payload}

    entries = payload.get("entries", [])
    by_id = {e["id"]: e for e in entries if "id" in e}

    added = 0
    for item in NEW4:
        e = make_entry(item)
        if e["id"] not in by_id:
            by_id[e["id"]] = e
            added += 1

    prepared = list(by_id.values())
    prepared.sort(key=lambda x: (x.get("rank", CATEGORY_DEFAULT_RANK.get(x.get("category"), 10000)), x.get("name", "").lower()))
    payload["entries"] = prepared

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Added {added} entries. Total: {len(prepared)}")


if __name__ == "__main__":
    main()