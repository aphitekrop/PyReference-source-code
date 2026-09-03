#!/usr/bin/env python3
import json
from pathlib import Path


INPUT_PATHS = [Path("data/entries.json"), Path("entries.json")]
OUTPUT_PATH = Path("data/entries.json")


CHECKED_CATEGORIES = {"core", "builtin", "types", "operators", "exceptions", "stdlib",
                      "string", "list", "dict", "set"}


CATEGORY_DEFAULT_RANK = {
    "core": 1500, "builtin": 2000, "string": 2500, "list": 2600, "dict": 2700,
    "set": 2800, "types": 3000, "operators": 4000, "exceptions": 5000,
    "stdlib": 6000, "python-cli": 7000, "dev-tools": 7500, "packages": 8000, "os": 9000,
}


POPULARITY = {
    "str-split": 2501, "str-join": 2502, "str-strip": 2503, "str-replace": 2504,
    "str-find": 2505, "str-lower": 2506, "str-upper": 2507, "str-startswith": 2508,
    "list-append": 2601, "list-pop": 2602, "list-sort": 2603,
    "dict-get": 2701, "dict-items": 2702, "dict-update": 2703,
    "Exception": 5001, "NameError": 5002, "ModuleNotFoundError": 5003,
    "KeyboardInterrupt": 5004, "PermissionError": 5005, "TimeoutError": 5006,
    "floor-div": 4001, "modulo": 4002, "power": 4003, "fstring": 1501, "listcomp": 1502,
    "pip-uninstall": 7001, "git-clone": 7501, "git-push": 7502, "git-pull": 7503,
    "grep": 9001, "cat": 9002, "touch": 9003,
    "httpx": 8001, "pydantic": 8002, "rich": 8003, "mypy": 8004, "ruff": 8005,
}


# (id, name, type, category, summary, syntax, example, tags)
NEW = [
    # ---- встроенные функции ----
    ("hash", "hash()", "builtin-function", "builtin", "Возвращает хэш объекта.", "hash(obj)", "hash('a')", ["hash"]),
    ("id", "id()", "builtin-function", "builtin", "Уникальный идентификатор объекта.", "id(obj)", "id(x)", ["id"]),
    ("help", "help()", "builtin-function", "builtin", "Встроенная справка.", "help(obj)", "help(len)", ["help"]),
    ("hex", "hex()", "builtin-function", "builtin", "Число в шестнадцатеричную строку.", "hex(x)", "hex(255)", ["hex"]),
    ("oct", "oct()", "builtin-function", "builtin", "Число в восьмеричную строку.", "oct(x)", "oct(8)", ["oct"]),
    ("bin", "bin()", "builtin-function", "builtin", "Число в двоичную строку.", "bin(x)", "bin(5)", ["bin"]),
    ("ord", "ord()", "builtin-function", "builtin", "Код символа.", "ord(c)", "ord('a')", ["ord"]),
    ("chr", "chr()", "builtin-function", "builtin", "Символ по коду.", "chr(i)", "chr(97)", ["chr"]),
    ("pow", "pow()", "builtin-function", "builtin", "Возведение в степень.", "pow(base, exp)", "pow(2, 3)", ["pow"]),
    ("divmod", "divmod()", "builtin-function", "builtin", "Пара: частное и остаток.", "divmod(a, b)", "divmod(7, 2)", ["divmod"]),
    ("globals", "globals()", "builtin-function", "builtin", "Словарь глобальных имён.", "globals()", "globals()", ["globals"]),
    ("locals", "locals()", "builtin-function", "builtin", "Словарь локальных имён.", "locals()", "locals()", ["locals"]),
    ("eval", "eval()", "builtin-function", "builtin", "Выполняет выражение из строки.", "eval(expr)", "eval('2 + 2')", ["eval"]),
    ("exec", "exec()", "builtin-function", "builtin", "Выполняет код из строки.", "exec(code)", "exec('x = 1')", ["exec"]),
    ("compile", "compile()", "builtin-function", "builtin", "Компилирует код в объект.", "compile(source, name, mode)", "compile('x=1', '<s>', 'exec')", ["compile"]),
    ("getattr", "getattr()", "builtin-function", "builtin", "Читает атрибут с дефолтом.", "getattr(obj, name, default)", "getattr(obj, 'x', 0)", ["getattr"]),
    ("setattr", "setattr()", "builtin-function", "builtin", "Устанавливает атрибут.", "setattr(obj, name, value)", "setattr(obj, 'x', 1)", ["setattr"]),
    ("hasattr", "hasattr()", "builtin-function", "builtin", "Проверяет наличие атрибута.", "hasattr(obj, name)", "hasattr(obj, 'x')", ["hasattr"]),
    ("delattr", "delattr()", "builtin-function", "builtin", "Удаляет атрибут.", "delattr(obj, name)", "delattr(obj, 'x')", ["delattr"]),
    ("issubclass", "issubclass()", "builtin-function", "builtin", "Проверяет наследование.", "issubclass(cls, info)", "issubclass(bool, int)", ["issubclass"]),
    ("frozenset", "frozenset", "builtin-type", "types", "Неизменяемое множество.", "frozenset(iterable)", "frozenset([1, 2])", ["frozenset"]),
    ("bytes", "bytes", "builtin-type", "types", "Неизменяемые байты.", "bytes(source)", "bytes('пр', 'utf-8')", ["bytes"]),
    ("bytearray", "bytearray", "builtin-type", "types", "Изменяемые байты.", "bytearray(source)", "bytearray(4)", ["bytearray"]),
    ("memoryview", "memoryview", "builtin-type", "types", "Представление памяти.", "memoryview(obj)", "memoryview(b'ab')", ["memoryview"]),
    ("object", "object", "builtin-type", "types", "Базовый тип всех объектов.", "object()", "object()", ["object"]),
    ("complex", "complex", "builtin-type", "types", "Комплексное число.", "complex(real, imag)", "complex(1, 2)", ["complex"]),
    ("slice", "slice", "builtin-type", "types", "Объект среза.", "slice(start, stop, step)", "slice(0, 5)", ["slice"]),

    # ---- методы строк ----
    ("str-split", "str.split()", "method", "string", "Разбивает строку в список.", "str.split(sep)", "'a,b'.split(',')", ["split"]),
    ("str-join", "str.join()", "method", "string", "Собирает список в строку.", "sep.join(iterable)", "', '.join(['a', 'b'])", ["join"]),
    ("str-strip", "str.strip()", "method", "string", "Убирает пробелы по краям.", "str.strip()", "' x '.strip()", ["strip"]),
    ("str-replace", "str.replace()", "method", "string", "Заменяет подстроки.", "str.replace(old, new)", "'a'.replace('a', 'b')", ["replace"]),
    ("str-find", "str.find()", "method", "string", "Ищет подстроку, возвращает индекс.", "str.find(sub)", "'abc'.find('b')", ["find"]),
    ("str-lower", "str.lower()", "method", "string", "В нижний регистр.", "str.lower()", "'ABC'.lower()", ["lower"]),
    ("str-upper", "str.upper()", "method", "string", "В верхний регистр.", "str.upper()", "'abc'.upper()", ["upper"]),
    ("str-startswith", "str.startswith()", "method", "string", "Проверяет начало строки.", "str.startswith(p)", "'abc'.startswith('a')", ["startswith"]),
    ("str-endswith", "str.endswith()", "method", "string", "Проверяет конец строки.", "str.endswith(s)", "'abc'.endswith('c')", ["endswith"]),
    ("str-isdigit", "str.isdigit()", "method", "string", "Строка из цифр?", "str.isdigit()", "'123'.isdigit()", ["isdigit"]),
    ("str-format", "str.format()", "method", "string", "Форматирование строки.", "str.format(...)", "'{} {}'.format('a', 'b')", ["format"]),
    ("str-count", "str.count()", "method", "string", "Считает вхождения.", "str.count(sub)", "'aaa'.count('a')", ["count"]),
    ("str-title", "str.title()", "method", "string", "Слова с заглавной.", "str.title()", "'hi wo'.title()", ["title"]),
    ("str-removeprefix", "str.removeprefix()", "method", "string", "Убирает префикс.", "str.removeprefix(p)", "'x1'.removeprefix('x')", ["removeprefix"]),
    ("str-removesuffix", "str.removesuffix()", "method", "string", "Убирает суффикс.", "str.removesuffix(s)", "'x1'.removesuffix('1')", ["removesuffix"]),

    # ---- методы списков ----
    ("list-append", "list.append()", "method", "list", "Добавляет элемент в конец.", "list.append(x)", "items.append(1)", ["append"]),
    ("list-extend", "list.extend()", "method", "list", "Добавляет несколько элементов.", "list.extend(it)", "items.extend([2, 3])", ["extend"]),
    ("list-insert", "list.insert()", "method", "list", "Вставляет по индексу.", "list.insert(i, x)", "items.insert(0, 1)", ["insert"]),
    ("list-remove", "list.remove()", "method", "list", "Удаляет первый найденный.", "list.remove(x)", "items.remove(1)", ["remove"]),
    ("list-pop", "list.pop()", "method", "list", "Удаляет и возвращает элемент.", "list.pop(i)", "items.pop()", ["pop"]),
    ("list-clear", "list.clear()", "method", "list", "Очищает список.", "list.clear()", "items.clear()", ["clear"]),
    ("list-index", "list.index()", "method", "list", "Индекс первого вхождения.", "list.index(x)", "items.index(1)", ["index"]),
    ("list-count", "list.count()", "method", "list", "Считает вхождения элемента.", "list.count(x)", "items.count(1)", ["count"]),
    ("list-sort", "list.sort()", "method", "list", "Сортирует на месте.", "list.sort(key, reverse)", "items.sort()", ["sort"]),
    ("list-reverse", "list.reverse()", "method", "list", "Разворачивает на месте.", "list.reverse()", "items.reverse()", ["reverse"]),
    ("list-copy", "list.copy()", "method", "list", "Поверхностная копия.", "list.copy()", "items.copy()", ["copy"]),

    # ---- методы словарей ----
    ("dict-get", "dict.get()", "method", "dict", "Безопасное чтение по ключу.", "dict.get(key, default)", "data.get('a', 0)", ["get"]),
    ("dict-keys", "dict.keys()", "method", "dict", "Ключи словаря.", "dict.keys()", "data.keys()", ["keys"]),
    ("dict-values", "dict.values()", "method", "dict", "Значения словаря.", "dict.values()", "data.values()", ["values"]),
    ("dict-items", "dict.items()", "method", "dict", "Пары ключ-значение.", "dict.items()", "data.items()", ["items"]),
    ("dict-update", "dict.update()", "method", "dict", "Обновляет словарь.", "dict.update(other)", "data.update({'b': 2})", ["update"]),
    ("dict-pop", "dict.pop()", "method", "dict", "Удаляет ключ, возвращает значение.", "dict.pop(key)", "data.pop('a')", ["pop"]),
    ("dict-setdefault", "dict.setdefault()", "method", "dict", "Значение по умолчанию.", "dict.setdefault(k, d)", "data.setdefault('a', 1)", ["setdefault"]),
    ("dict-clear", "dict.clear()", "method", "dict", "Очищает словарь.", "dict.clear()", "data.clear()", ["clear"]),
    ("dict-copy", "dict.copy()", "method", "dict", "Поверхностная копия.", "dict.copy()", "data.copy()", ["copy"]),
    ("dict-fromkeys", "dict.fromkeys()", "method", "dict", "Словарь из ключей.", "dict.fromkeys(seq, v)", "dict.fromkeys(['a'], 1)", ["fromkeys"]),

    # ---- методы множеств ----
    ("set-add", "set.add()", "method", "set", "Добавляет элемент.", "set.add(x)", "s.add(1)", ["add"]),
    ("set-remove", "set.remove()", "method", "set", "Удаляет (ошибка если нет).", "set.remove(x)", "s.remove(1)", ["remove"]),
    ("set-discard", "set.discard()", "method", "set", "Удаляет без ошибки.", "set.discard(x)", "s.discard(1)", ["discard"]),
    ("set-union", "set.union()", "method", "set", "Объединение.", "set.union(other)", "s | t", ["union"]),
    ("set-intersection", "set.intersection()", "method", "set", "Пересечение.", "set.intersection(other)", "s & t", ["intersection"]),
    ("set-difference", "set.difference()", "method", "set", "Разность.", "set.difference(other)", "s - t", ["difference"]),

    # ---- модули ----
    ("warnings", "warnings", "module", "stdlib", "Предупреждения.", "import warnings", "warnings.warn('x')", ["warnings"]),
    ("contextlib", "contextlib", "module", "stdlib", "Контекстные менеджеры.", "import contextlib", "contextlib.suppress(FileNotFoundError)", ["contextlib"]),
    ("enum", "enum", "module", "stdlib", "Перечисления.", "from enum import Enum", "class Color(Enum): RED = 1", ["enum"]),
    ("io", "io", "module", "stdlib", "Потоки ввода-вывода.", "import io", "io.StringIO()", ["io"]),
    ("pickle", "pickle", "module", "stdlib", "Сериализация объектов.", "import pickle", "pickle.dump(obj, f)", ["pickle"]),
    ("secrets", "secrets", "module", "stdlib", "Криптостойкая случайность.", "import secrets", "secrets.token_hex(8)", ["secrets"]),
    ("platform", "platform", "module", "stdlib", "Информация о системе.", "import platform", "platform.system()", ["platform"]),
    ("zipfile", "zipfile", "module", "stdlib", "Работа с ZIP.", "import zipfile", "zipfile.ZipFile('a.zip')", ["zipfile"]),
    ("configparser", "configparser", "module", "stdlib", "Чтение INI.", "import configparser", "configparser.ConfigParser()", ["configparser"]),
    ("tomllib", "tomllib", "module", "stdlib", "Чтение TOML.", "import tomllib", "tomllib.load(f)", ["tomllib"]),
    ("string", "string", "module", "stdlib", "Строковые константы.", "import string", "string.ascii_letters", ["string"]),
    ("textwrap", "textwrap", "module", "stdlib", "Перенос текста.", "import textwrap", "textwrap.shorten(t, 20)", ["textwrap"]),
    ("difflib", "difflib", "module", "stdlib", "Сравнение последовательностей.", "import difflib", "difflib.get_close_matches('a', ['a1'])", ["difflib"]),
    ("fnmatch", "fnmatch", "module", "stdlib", "Шаблоны имён файлов.", "import fnmatch", "fnmatch.fnmatch('a.txt', '*.txt')", ["fnmatch"]),
    ("shlex", "shlex", "module", "stdlib", "Разбор командных строк.", "import shlex", "shlex.split('a \"b c\"')", ["shlex"]),
    ("struct", "struct", "module", "stdlib", "Бинарные структуры.", "import struct", "struct.pack('i', 1)", ["struct"]),
    ("bisect", "bisect", "module", "stdlib", "Бинарный поиск.", "import bisect", "bisect.bisect_left([1, 3], 2)", ["bisect"]),
    ("heapq", "heapq", "module", "stdlib", "Куча и приоритетные очереди.", "import heapq", "heapq.heappush(h, 1)", ["heapq"]),
    ("array", "array", "module", "stdlib", "Компактные числовые массивы.", "import array", "array.array('i', [1, 2])", ["array"]),
    ("types", "types", "module", "stdlib", "Типы и утилиты.", "import types", "types.SimpleNamespace(a=1)", ["types"]),
    ("inspect", "inspect", "module", "stdlib", "Инспекция объектов.", "import inspect", "inspect.signature(f)", ["inspect"]),
    ("traceback", "traceback", "module", "stdlib", "Форматирование ошибок.", "import traceback", "traceback.print_exc()", ["traceback"]),
    ("unittest", "unittest", "module", "stdlib", "Встроенные тесты.", "import unittest", "unittest.main()", ["unittest"]),
    ("pdb", "pdb", "module", "stdlib", "Отладчик.", "import pdb", "pdb.set_trace()", ["pdb"]),
    ("timeit", "timeit", "module", "stdlib", "Замер времени кода.", "import timeit", "timeit.timeit('sum(range(10))')", ["timeit"]),
    ("queue", "queue", "module", "stdlib", "Очереди для потоков.", "import queue", "queue.Queue()", ["queue"]),
    ("concurrent", "concurrent.futures", "module", "stdlib", "Пулы потоков и процессов.", "import concurrent.futures", "concurrent.futures.ThreadPoolExecutor()", ["concurrent"]),
    ("codecs", "codecs", "module", "stdlib", "Кодировки.", "import codecs", "codecs.open('f', encoding='utf-8')", ["codecs"]),
    ("getpass", "getpass", "module", "stdlib", "Скрытый ввод пароля.", "import getpass", "getpass.getpass()", ["getpass"]),
    ("webbrowser", "webbrowser", "module", "stdlib", "Открытие браузера.", "import webbrowser", "webbrowser.open('https://...')", ["webbrowser"]),

    # ---- исключения ----
    ("Exception", "Exception", "exception", "exceptions", "База большинства ошибок.", "raise Exception('msg')", "except Exception as e:", ["Exception"]),
    ("StopIteration", "StopIteration", "exception", "exceptions", "Итератор исчерпан.", "raise StopIteration", "next(it)", ["StopIteration"]),
    ("ArithmeticError", "ArithmeticError", "exception", "exceptions", "База арифметических ошибок.", "raise ArithmeticError", "1 / 0", ["ArithmeticError"]),
    ("LookupError", "LookupError", "exception", "exceptions", "База KeyError и IndexError.", "raise LookupError", "d['x']", ["LookupError"]),
    ("NotImplementedError", "NotImplementedError", "exception", "exceptions", "Метод не реализован.", "raise NotImplementedError", "...", ["NotImplementedError"]),
    ("RecursionError", "RecursionError", "exception", "exceptions", "Слишком глубокая рекурсия.", "raise RecursionError", "def f(): f()", ["RecursionError"]),
    ("OverflowError", "OverflowError", "exception", "exceptions", "Число слишком большое.", "raise OverflowError", "...", ["OverflowError"]),
    ("MemoryError", "MemoryError", "exception", "exceptions", "Не хватает памяти.", "raise MemoryError", "...", ["MemoryError"]),
    ("NameError", "NameError", "exception", "exceptions", "Имя не найдено.", "raise NameError", "unknown_var", ["NameError"]),
    ("UnboundLocalError", "UnboundLocalError", "exception", "exceptions", "Локальная переменная не присвоена.", "raise UnboundLocalError", "...", ["UnboundLocalError"]),
    ("ImportError", "ImportError", "exception", "exceptions", "Ошибка импорта.", "raise ImportError", "import missing", ["ImportError"]),
    ("ModuleNotFoundError", "ModuleNotFoundError", "exception", "exceptions", "Модуль не найден.", "raise ModuleNotFoundError", "import missing", ["ModuleNotFoundError"]),
    ("OSError", "OSError", "exception", "exceptions", "Ошибка ОС.", "raise OSError", "...", ["OSError"]),
    ("PermissionError", "PermissionError", "exception", "exceptions", "Нет прав доступа.", "raise PermissionError", "open('/root')", ["PermissionError"]),
    ("TimeoutError", "TimeoutError", "exception", "exceptions", "Операция не успела.", "raise TimeoutError", "...", ["TimeoutError"]),
    ("ConnectionError", "ConnectionError", "exception", "exceptions", "Ошибка соединения.", "raise ConnectionError", "...", ["ConnectionError"]),
    ("KeyboardInterrupt", "KeyboardInterrupt", "exception", "exceptions", "Прерывание Ctrl+C.", "raise KeyboardInterrupt", "Ctrl+C", ["KeyboardInterrupt"]),
    ("EOFError", "EOFError", "exception", "exceptions", "Конец ввода.", "raise EOFError", "input()", ["EOFError"]),
    ("UnicodeDecodeError", "UnicodeDecodeError", "exception", "exceptions", "Ошибка декодирования.", "raise UnicodeDecodeError", "b'\\xff'.decode()", ["UnicodeDecodeError"]),
    ("RuntimeError", "RuntimeError", "exception", "exceptions", "Общая ошибка выполнения.", "raise RuntimeError", "...", ["RuntimeError"]),
    ("AssertionError", "AssertionError", "exception", "exceptions", "assert не прошёл.", "raise AssertionError", "assert False", ["AssertionError"]),

    # ---- синтаксис ----
    ("floor-div", "//", "syntax", "core", "Целочисленное деление.", "a // b", "7 // 2", ["деление"]),
    ("modulo", "%", "syntax", "core", "Остаток от деления.", "a % b", "7 % 3", ["остаток"]),
    ("power", "**", "syntax", "core", "Возведение в степень.", "a ** b", "2 ** 3", ["степень"]),
    ("walrus", ":=", "syntax", "core", "Присваивание внутри выражения.", "if (n := len(x)) > 5:", "...", ["walrus"]),
    ("augmented", "+=", "syntax", "core", "Сокращённое присваивание.", "a += b", "x += 1", ["присваивание"]),
    ("args", "*args", "syntax", "core", "Переменные позиционные аргументы.", "def f(*args):", "f(1, 2, 3)", ["args"]),
    ("kwargs", "**kwargs", "syntax", "core", "Переменные именованные аргументы.", "def f(**kwargs):", "f(a=1)", ["kwargs"]),
    ("decorator", "@", "syntax", "core", "Декоратор.", "@decorator", "@staticmethod", ["decorator"]),
    ("fstring", "f-string", "syntax", "core", "Строка с подстановкой.", "f'{value}'", "f'x={x}'", ["f-string"]),
    ("listcomp", "list comprehension", "syntax", "core", "Список в одну строку.", "[e for x in items]", "[x * 2 for x in range(3)]", ["comprehension"]),
    ("dictcomp", "dict comprehension", "syntax", "core", "Словарь в одну строку.", "{k: v for ...}", "{x: x * 2 for x in range(3)}", ["comprehension"]),
    ("genexpr", "generator expression", "syntax", "core", "Генератор в одну строку.", "(e for x in items)", "sum(x for x in range(3))", ["comprehension"]),
    ("slicing", "[::]", "syntax", "core", "Срезы последовательностей.", "seq[start:stop:step]", "items[::-1]", ["slice"]),
    ("ellipsis", "...", "syntax", "core", "Заглушка.", "...", "def f(): ...", ["ellipsis"]),
    ("underscore", "_", "syntax", "core", "Игнорируемая переменная.", "for _ in range(3):", "...", ["_"]),
    ("annotation", "->", "syntax", "core", "Аннотация возвращаемого типа.", "def f() -> int:", "...", ["typing"]),

    # ---- CLI / git ----
    ("pip-uninstall", "pip uninstall", "cli", "python-cli", "Удаляет пакет.", "pip uninstall pkg", "pip uninstall requests", ["pip"]),
    ("pip-check", "pip check", "cli", "python-cli", "Проверяет конфликты зависимостей.", "pip check", "pip check", ["pip"]),
    ("python-c", "python -c", "cli", "python-cli", "Выполняет код из строки.", "python -c 'code'", "python -c \"print(1)\"", ["python"]),
    ("git-init", "git init", "cli", "dev-tools", "Создаёт репозиторий.", "git init", "git init", ["git"]),
    ("git-clone", "git clone", "cli", "dev-tools", "Копирует репозиторий.", "git clone url", "git clone https://github.com/u/r", ["git"]),
    ("git-add", "git add", "cli", "dev-tools", "Добавляет изменения в индекс.", "git add .", "git add .", ["git"]),
    ("git-status", "git status", "cli", "dev-tools", "Показывает состояние.", "git status", "git status", ["git"]),
    ("git-push", "git push", "cli", "dev-tools", "Отправляет коммиты.", "git push", "git push", ["git"]),
    ("git-pull", "git pull", "cli", "dev-tools", "Забирает и сливает изменения.", "git pull", "git pull", ["git"]),
    ("git-branch", "git branch", "cli", "dev-tools", "Ветки.", "git branch", "git branch", ["git"]),
    ("git-log", "git log", "cli", "dev-tools", "История коммитов.", "git log", "git log --oneline", ["git"]),
    ("git-switch", "git switch", "cli", "dev-tools", "Переключение веток.", "git switch b", "git switch main", ["git"]),

    # ---- OS ----
    ("touch", "touch", "os-command", "os", "Создаёт пустой файл.", "touch file", "touch a.txt", ["touch"]),
    ("cat", "cat", "os-command", "os", "Выводит файл.", "cat file", "cat a.txt", ["cat"]),
    ("grep", "grep", "os-command", "os", "Ищет текст в файлах.", "grep p file", "grep 'err' log.txt", ["grep"]),
    ("find", "find", "os-command", "os", "Ищет файлы.", "find p -name m", "find . -name '*.py'", ["find"]),
    ("chmod", "chmod", "os-command", "os", "Меняет права доступа.", "chmod m file", "chmod +x run.sh", ["chmod"]),
    ("sudo", "sudo", "os-command", "os", "Команда с правами админа.", "sudo cmd", "sudo apt update", ["sudo"]),
    ("which", "which", "os-command", "os", "Путь к команде (Unix).", "which cmd", "which python", ["which"]),
    ("where", "where", "os-command", "os", "Путь к команде (Windows).", "where cmd", "where python", ["where"]),
    ("tree", "tree", "os-command", "os", "Дерево папок.", "tree", "tree", ["tree"]),
    ("hostname", "hostname", "os-command", "os", "Имя компьютера.", "hostname", "hostname", ["hostname"]),
    ("whoami", "whoami", "os-command", "os", "Текущий пользователь.", "whoami", "whoami", ["whoami"]),
    ("tasklist", "tasklist", "os-command", "os", "Процессы Windows.", "tasklist", "tasklist", ["tasklist"]),
    ("taskkill", "taskkill", "os-command", "os", "Завершает процесс Windows.", "taskkill /PID id", "taskkill /IM app.exe", ["taskkill"]),
    ("ps", "ps", "os-command", "os", "Процессы Unix.", "ps", "ps aux", ["ps"]),
    ("kill", "kill", "os-command", "os", "Завершает процесс Unix.", "kill pid", "kill 1234", ["kill"]),
    ("ssh", "ssh", "os-command", "os", "Удалённое подключение.", "ssh u@host", "ssh user@example.com", ["ssh"]),
    ("scp", "scp", "os-command", "os", "Копирование по сети.", "scp src dst", "scp a.txt u@h:~", ["scp"]),
    ("netstat", "netstat", "os-command", "os", "Сетевые соединения.", "netstat", "netstat -an", ["netstat"]),
    ("tracert", "tracert", "os-command", "os", "Маршрут пакетов Windows.", "tracert host", "tracert example.com", ["tracert"]),
    ("nslookup", "nslookup", "os-command", "os", "DNS-записи.", "nslookup host", "nslookup example.com", ["nslookup"]),
    ("uname", "uname", "os-command", "os", "Информация о системе Unix.", "uname", "uname -a", ["uname"]),
    ("head", "head", "os-command", "os", "Первые строки файла.", "head file", "head -n 5 a.txt", ["head"]),
    ("tail", "tail", "os-command", "os", "Последние строки файла.", "tail file", "tail -n 5 a.txt", ["tail"]),
    ("wc", "wc", "os-command", "os", "Считает строки/слова.", "wc file", "wc -l a.txt", ["wc"]),
    ("tar", "tar", "os-command", "os", "Архивы tar.", "tar -czf a.tgz d", "tar -xzf a.tgz", ["tar"]),
    ("unzip", "unzip", "os-command", "os", "Распаковка ZIP.", "unzip file", "unzip a.zip", ["unzip"]),

    # ---- пакеты ----
    ("httpx", "httpx", "library", "packages", "Современный HTTP-клиент с async.", "pip install httpx", "httpx.get('https://...')", ["httpx"]),
    ("aiohttp", "aiohttp", "library", "packages", "Асинхронный HTTP.", "pip install aiohttp", "aiohttp.ClientSession()", ["aiohttp"]),
    ("beautifulsoup4", "BeautifulSoup", "library", "packages", "Парсинг HTML.", "pip install beautifulsoup4", "BeautifulSoup(html, 'html.parser')", ["bs4"]),
    ("selenium", "Selenium", "library", "packages", "Автоматизация браузера.", "pip install selenium", "webdriver.Chrome()", ["selenium"]),
    ("playwright", "Playwright", "library", "packages", "Автоматизация браузера.", "pip install playwright", "playwright install", ["playwright"]),
    ("sqlalchemy", "SQLAlchemy", "library", "packages", "ORM и работа с БД.", "pip install sqlalchemy", "create_engine('sqlite:///a.db')", ["sqlalchemy"]),
    ("pydantic", "pydantic", "library", "packages", "Валидация данных.", "pip install pydantic", "class M(BaseModel): ...", ["pydantic"]),
    ("rich", "rich", "library", "packages", "Красивый вывод в терминал.", "pip install rich", "rich.print(...)", ["rich"]),
    ("click", "click", "library", "packages", "CLI-фреймворк.", "pip install click", "@click.command()", ["click"]),
    ("typer", "typer", "library", "packages", "CLI на аннотациях.", "pip install typer", "typer.run(main)", ["typer"]),
    ("python-dotenv", "python-dotenv", "library", "packages", "Переменные из .env.", "pip install python-dotenv", "load_dotenv()", ["dotenv"]),
    ("pillow", "Pillow", "library", "packages", "Обработка изображений.", "pip install pillow", "Image.open('a.png')", ["PIL"]),
    ("matplotlib", "Matplotlib", "library", "packages", "Графики.", "pip install matplotlib", "plt.plot([1, 2])", ["matplotlib"]),
    ("scikit-learn", "scikit-learn", "library", "packages", "Машинное обучение.", "pip install scikit-learn", "from sklearn import ...", ["sklearn"]),
    ("scipy", "SciPy", "library", "packages", "Научные вычисления.", "pip install scipy", "...", ["scipy"]),
    ("sympy", "SymPy", "library", "packages", "Символьная математика.", "pip install sympy", "sympy.symbols('x')", ["sympy"]),
    ("jupyter", "Jupyter", "library", "packages", "Интерактивные ноутбуки.", "pip install jupyter", "jupyter notebook", ["jupyter"]),
    ("ipython", "IPython", "library", "packages", "Улучшенная консоль.", "pip install ipython", "ipython", ["ipython"]),
    ("mypy", "mypy", "library", "packages", "Проверка типов.", "pip install mypy", "mypy app.py", ["mypy"]),
    ("ruff", "ruff", "library", "packages", "Быстрый линтер и форматтер.", "pip install ruff", "ruff check .", ["ruff"]),
    ("flake8", "flake8", "library", "packages", "Линтер.", "pip install flake8", "flake8 .", ["flake8"]),
    ("isort", "isort", "library", "packages", "Сортировка импортов.", "pip install isort", "isort .", ["isort"]),
    ("virtualenv", "virtualenv", "library", "packages", "Виртуальные окружения.", "pip install virtualenv", "virtualenv venv", ["virtualenv"]),
    ("poetry", "poetry", "library", "packages", "Менеджер зависимостей.", "pip install poetry", "poetry init", ["poetry"]),
    ("uv", "uv", "library", "packages", "Быстрый менеджер пакетов.", "pip install uv", "uv venv", ["uv"]),
    ("pyyaml", "PyYAML", "library", "packages", "Работа с YAML.", "pip install pyyaml", "yaml.safe_load(f)", ["yaml"]),
    ("python-telegram-bot", "python-telegram-bot", "library", "packages", "Telegram-боты (async).", "pip install python-telegram-bot", "Application.builder()", ["telegram"]),
    ("aiogram", "aiogram", "library", "packages", "Telegram-боты (async).", "pip install aiogram", "Bot(token)", ["telegram"]),
]


RELATED = {
    "str-split": {"alternatives": ["re", "str-find"], "complements": ["str-join", "str"], "seealso": ["str"]},
    "str-join": {"alternatives": ["plus", "fstring"], "complements": ["str-split", "str"], "seealso": ["str"]},
    "str-strip": {"alternatives": ["str-replace"], "complements": ["str"], "seealso": ["str"]},
    "str-replace": {"alternatives": ["re", "str-strip"], "complements": ["str"], "seealso": ["re"]},
    "str-find": {"alternatives": ["in", "str-count"], "complements": ["str"], "seealso": ["in"]},
    "str-lower": {"alternatives": ["str-upper"], "complements": ["str"], "seealso": ["str-upper"]},
    "str-upper": {"alternatives": ["str-lower"], "complements": ["str"], "seealso": ["str-lower"]},
    "list-append": {"alternatives": ["list-extend", "list-insert"], "complements": ["list", "list-pop"], "seealso": ["list"]},
    "list-pop": {"alternatives": ["list-remove", "del"], "complements": ["list", "list-append"], "seealso": ["list"]},
    "list-sort": {"alternatives": ["sorted"], "complements": ["list", "list-reverse"], "seealso": ["sorted"]},
    "dict-get": {"alternatives": ["in", "dict-setdefault"], "complements": ["dict"], "seealso": ["KeyError"]},
    "dict-items": {"alternatives": ["dict-keys", "dict-values"], "complements": ["dict", "for"], "seealso": ["dict"]},
    "set-union": {"alternatives": ["set-intersection"], "complements": ["set"], "seealso": ["set"]},
    "hash": {"alternatives": ["hashlib"], "complements": ["dict"], "seealso": ["hashlib"]},
    "getattr": {"alternatives": ["hasattr", "setattr"], "complements": ["setattr", "hasattr"], "seealso": ["AttributeError"]},
    "hasattr": {"alternatives": ["getattr"], "complements": ["getattr"], "seealso": ["AttributeError"]},
    "eval": {"alternatives": ["exec", "ast? нет"], "complements": ["exec"], "seealso": ["exec"]},
    "exec": {"alternatives": ["eval", "compile"], "complements": ["compile"], "seealso": ["eval"]},
    "frozenset": {"alternatives": ["set"], "complements": ["set"], "seealso": ["set"]},
    "bytes": {"alternatives": ["bytearray", "str"], "complements": ["codecs"], "seealso": ["bytearray"]},
    "Exception": {"alternatives": ["ValueError", "TypeError"], "complements": ["try", "except", "raise"], "seealso": ["try"]},
    "NameError": {"alternatives": ["UnboundLocalError"], "complements": ["try"], "seealso": ["UnboundLocalError"]},
    "ModuleNotFoundError": {"alternatives": ["ImportError"], "complements": ["try", "pip-install"], "seealso": ["ImportError"]},
    "KeyboardInterrupt": {"alternatives": [], "complements": ["try"], "seealso": ["EOFError"]},
    "PermissionError": {"alternatives": ["FileNotFoundError"], "complements": ["try", "open"], "seealso": ["OSError"]},
    "floor-div": {"alternatives": ["divide", "modulo"], "complements": ["modulo"], "seealso": ["divide"]},
    "modulo": {"alternatives": ["floor-div"], "complements": ["floor-div"], "seealso": ["divide"]},
    "power": {"alternatives": ["pow", "math"], "complements": [], "seealso": ["pow"]},
    "fstring": {"alternatives": ["format", "str-format"], "complements": ["str"], "seealso": ["format"]},
    "listcomp": {"alternatives": ["map", "for"], "complements": ["list"], "seealso": ["map", "filter"]},
    "pip-uninstall": {"alternatives": ["pip-check"], "complements": ["pip"], "seealso": ["pip-install"]},
    "git-clone": {"alternatives": ["git-init"], "complements": ["git"], "seealso": ["git"]},
    "git-push": {"alternatives": [], "complements": ["git-add", "git-commit? нет"], "seealso": ["git-pull"]},
    "git-pull": {"alternatives": [], "complements": ["git"], "seealso": ["git-push"]},
    "grep": {"alternatives": ["find", "str-find"], "complements": ["cat"], "seealso": ["cat"]},
    "cat": {"alternatives": ["head", "tail"], "complements": ["grep"], "seealso": ["head", "tail"]},
    "touch": {"alternatives": ["echo", "open"], "complements": ["cat"], "seealso": ["rm"]},
    "httpx": {"alternatives": ["requests", "aiohttp", "curl"], "complements": ["json"], "seealso": ["requests"]},
    "aiohttp": {"alternatives": ["httpx", "asyncio"], "complements": ["asyncio"], "seealso": ["httpx"]},
    "beautifulsoup4": {"alternatives": ["selenium", "playwright"], "complements": ["requests"], "seealso": ["requests"]},
    "sqlalchemy": {"alternatives": ["sqlite3", "pydantic? нет"], "complements": ["sqlite3"], "seealso": ["sqlite3"]},
    "pydantic": {"alternatives": ["dataclasses", "typing"], "complements": ["fastapi"], "seealso": ["dataclasses"]},
    "rich": {"alternatives": ["pprint", "print"], "complements": ["print"], "seealso": ["pprint"]},
    "mypy": {"alternatives": ["typing"], "complements": ["typing"], "seealso": ["ruff"]},
    "ruff": {"alternatives": ["black", "flake8", "isort"], "complements": ["black"], "seealso": ["black"]},
    "poetry": {"alternatives": ["pip", "uv", "virtualenv"], "complements": [], "seealso": ["pip"]},
    "uv": {"alternatives": ["pip", "poetry"], "complements": [], "seealso": ["pip"]},
}


CATEGORY_ALT = {
    "string": ["re", "format", "fstring"],
    "list": ["sorted", "reversed", "filter"],
    "dict": ["collections", "json"],
    "set": ["frozenset", "list"],
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
        "keyword": "Не возвращает значение.",
        "builtin-function": "Зависит от функции.",
        "builtin-type": "Объект типа.",
        "method": "Зависит от метода.",
        "operator": "Зависит от операции.",
        "syntax": "Зависит от выражения.",
        "exception": "Объект исключения.",
        "module": "Модуль.",
        "cli": "Результат команды.",
        "library": "Зависит от библиотеки.",
        "os-command": "Текст или код завершения.",
    }.get(t, "")


def make_entry(item):
    eid, name, etype, category, summary, syntax, example, tags = item
    return {
        "id": eid, "name": name, "type": etype, "category": category,
        "summary": summary, "syntax": syntax, "params": [],
        "returns": default_returns(etype), "errors": [], "example": example,
        "version": {"since": None, "deprecated": None, "removed": None,
                    "checked": "3.13" if category in CHECKED_CATEGORIES else None},
        "tags": tags, "links": [],
        "related": {"alternatives": [], "complements": [], "seealso": []},
    }


def main():
    payload = None
    for path in INPUT_PATHS:
        if path.exists():
            payload = json.loads(path.read_text(encoding="utf-8"))
            break
    if payload is None:
        print("Сначала запусти build_entries.py")
        return
    if isinstance(payload, list):
        payload = {"meta": {}, "entries": payload}

    entries = payload.get("entries", [])
    by_id = {e["id"]: e for e in entries if "id" in e}

    # добавить новые
    for item in NEW:
        e = make_entry(item)
        if e["id"] not in by_id:
            by_id[e["id"]] = e

    ids = set(by_id)

    # проставить related (явные + авто для методов)
    for e in by_id.values():
        rel = e.setdefault("related", {"alternatives": [], "complements": [], "seealso": []})

        extra = RELATED.get(e["id"])
        if extra:
            for k in ["alternatives", "complements", "seealso"]:
                rel[k] = merge_list(rel.get(k, []), extra.get(k, []), ids)

        if e.get("type") == "method":
            parent = e["id"].split("-")[0]
            pool = [a for a in CATEGORY_ALT.get(e.get("category"), []) if a != e["id"]]
            rel["alternatives"] = merge_list(rel.get("alternatives", []), pool, ids)
            rel["complements"] = merge_list(rel.get("complements", []), [parent], ids)
            rel["seealso"] = merge_list(rel.get("seealso", []), [parent], ids)

        if e.get("type") == "exception":
            rel["complements"] = merge_list(rel.get("complements", []), ["try", "except", "raise"], ids)
            rel["seealso"] = merge_list(rel.get("seealso", []), ["try"], ids)

    # ограничить альтернативы тремя и посчитать rank
    prepared = []
    for e in by_id.values():
        e["related"]["alternatives"] = e["related"]["alternatives"][:3]
        e["rank"] = POPULARITY.get(e["id"], CATEGORY_DEFAULT_RANK.get(e.get("category"), 10000))
        prepared.append(e)

    prepared.sort(key=lambda x: (x.get("rank", 10000), x.get("name", "").lower()))
    payload["entries"] = prepared

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {len(prepared)} entries to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()