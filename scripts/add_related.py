#!/usr/bin/env python3
import json
from pathlib import Path


INPUT_PATHS = [
    Path("data/entries.json"),
    Path("entries.json"),
]

OUTPUT_PATH = Path("data/entries.json")


def ext(name, syntax, note):
    """Внешняя альтернатива, которой нет в справочнике."""
    return {
        "name": name,
        "syntax": syntax,
        "note": note
    }


RELATED = {
    # ---------------- Циклы и условия ----------------
    "while": {
        "alternatives": [
            "for",
            ext("Рекурсия", "def f(): f()", "Иногда заменяет цикл, но дороже по памяти.")
        ],
        "complements": ["break", "continue", "else"],
        "seealso": ["for", "break", "continue"]
    },
    "for": {
        "alternatives": [
            "while",
            "map",
            ext("List comprehension", "[x for x in items]", "Создание списка в одну строку.")
        ],
        "complements": ["range", "enumerate", "zip"],
        "seealso": ["while", "break", "continue"]
    },
    "if": {
        "alternatives": [
            "match",
            ext("Тернарное выражение", "x if cond else y", "Короткое условие внутри выражения.")
        ],
        "complements": ["elif", "else"],
        "seealso": ["while", "match"]
    },
    "elif": {
        "alternatives": ["match", "if"],
        "complements": ["if", "else"],
        "seealso": ["if", "match"]
    },
    "else": {
        "alternatives": [
            ext("Тернарное выражение", "x if cond else y", "Короткая форма if/else.")
        ],
        "complements": ["if", "for", "while", "try"],
        "seealso": ["if", "elif"]
    },
    "break": {
        "alternatives": [
            "return",
            ext("Флаг-переменная", "stop = True", "Управляет циклом через условие.")
        ],
        "complements": ["for", "while"],
        "seealso": ["continue", "for", "while"]
    },
    "continue": {
        "alternatives": [
            ext("Обратное условие", "if not cond:", "Вместо continue можно инвертировать условие.")
        ],
        "complements": ["for", "while"],
        "seealso": ["break"]
    },
    "pass": {
        "alternatives": [
            ext("...", "...", "Современная заглушка вместо pass."),
            ext("Docstring", "\"\"\"text\"\"\"", "Строка документации как заглушка.")
        ],
        "complements": [],
        "seealso": ["def", "class"]
    },

    # ---------------- Функции и классы ----------------
    "def": {
        "alternatives": [
            "lambda",
            ext("Callable-класс", "class C:\n    def __call__(self): ...", "Объект, вызываемый как функция.")
        ],
        "complements": ["return"],
        "seealso": ["lambda", "class"]
    },
    "lambda": {
        "alternatives": [
            "def",
            "operator",
            ext("functools.partial", "from functools import partial", "Фиксирует часть аргументов функции.")
        ],
        "complements": ["map", "filter", "sorted", "min", "max"],
        "seealso": ["def", "functools"]
    },
    "class": {
        "alternatives": [
            "dataclasses",
            ext("namedtuple", "from collections import namedtuple", "Лёгкие неизменяемые структуры."),
            ext("TypedDict", "from typing import TypedDict", "Словари с аннотациями.")
        ],
        "complements": ["def", "super"],
        "seealso": ["def", "dataclasses"]
    },
    "return": {
        "alternatives": ["yield", "raise"],
        "complements": ["def"],
        "seealso": ["yield", "raise"]
    },
    "yield": {
        "alternatives": [
            "return",
            ext("Накопление списка", "result.append(x)", "Вместо генератора можно собирать список.")
        ],
        "complements": ["for", "iter", "next"],
        "seealso": ["return", "iter"]
    },
    "super": {
        "alternatives": [],
        "complements": ["class", "def"],
        "seealso": ["class"]
    },
    "property": {
        "alternatives": [
            ext("Getter/Setter", "def get_x / def set_x", "Явные методы доступа.")
        ],
        "complements": ["class"],
        "seealso": ["class", "classmethod"]
    },
    "classmethod": {
        "alternatives": ["staticmethod"],
        "complements": ["class"],
        "seealso": ["staticmethod", "class"]
    },
    "staticmethod": {
        "alternatives": [
            "classmethod",
            ext("Модульная функция", "def func(): ...", "Функция вне класса.")
        ],
        "complements": ["class"],
        "seealso": ["classmethod", "class"]
    },

    # ---------------- Импорт и области видимости ----------------
    "import": {
        "alternatives": [
            "from",
            ext("importlib", "import importlib", "Динамический импорт модулей.")
        ],
        "complements": ["as"],
        "seealso": ["from", "pip-install"]
    },
    "from": {
        "alternatives": ["import"],
        "complements": ["as", "import"],
        "seealso": ["import"]
    },
    "as": {
        "alternatives": [],
        "complements": ["import", "from", "with"],
        "seealso": ["import", "with"]
    },
    "global": {
        "alternatives": ["nonlocal"],
        "complements": [],
        "seealso": ["nonlocal"]
    },
    "nonlocal": {
        "alternatives": ["global"],
        "complements": [],
        "seealso": ["global"]
    },
    "assert": {
        "alternatives": [
            ext("if + raise", "if not cond: raise ...", "Явная проверка с исключением.")
        ],
        "complements": ["raise"],
        "seealso": ["raise", "pytest"]
    },
    "del": {
        "alternatives": [
            ext("list.pop()", "items.pop(0)", "Удаляет и возвращает элемент."),
            ext("dict.pop()", "data.pop('key')", "Удаляет ключ словаря.")
        ],
        "complements": [],
        "seealso": ["list", "dict"]
    },

    # ---------------- Логика и сравнение ----------------
    "not": {
        "alternatives": [
            ext("operator.not_", "import operator", "Функциональное отрицание.")
        ],
        "complements": ["and", "or"],
        "seealso": ["and", "or", "bool"]
    },
    "and": {
        "alternatives": ["all"],
        "complements": ["or", "not"],
        "seealso": ["or", "not", "all"]
    },
    "or": {
        "alternatives": ["any"],
        "complements": ["and", "not"],
        "seealso": ["and", "not", "any"]
    },
    "in": {
        "alternatives": [
            ext("str.find()", "text.find(sub)", "Ищет подстроку, возвращает индекс."),
            ext("dict.get()", "data.get(key)", "Безопасное чтение словаря.")
        ],
        "complements": ["for", "if"],
        "seealso": ["not", "list", "dict", "set"]
    },
    "is": {
        "alternatives": ["equals"],
        "complements": ["not"],
        "seealso": ["equals", "None"]
    },
    "equals": {
        "alternatives": [
            "is",
            ext("operator.eq", "import operator", "Функциональное сравнение.")
        ],
        "complements": ["not-equals"],
        "seealso": ["is", "not-equals"]
    },
    "not-equals": {
        "alternatives": ["equals"],
        "complements": ["equals"],
        "seealso": ["equals"]
    },
    "True": {
        "alternatives": [],
        "complements": [],
        "seealso": ["False", "bool", "not"]
    },
    "False": {
        "alternatives": [],
        "complements": [],
        "seealso": ["True", "bool", "not"]
    },
    "None": {
        "alternatives": [
            ext("Sentinel-объект", "_missing = object()", "Уникальный маркер отсутствия значения.")
        ],
        "complements": [],
        "seealso": ["is", "bool"]
    },

    # ---------------- Обработка ошибок ----------------
    "try": {
        "alternatives": [
            "with",
            ext("contextlib.suppress", "import contextlib", "Подавляет указанные исключения."),
            ext("Проверка заранее", "if value is not None:", "Иногда проще проверить данные до операции.")
        ],
        "complements": ["except", "finally", "raise", "else"],
        "seealso": ["ValueError", "TypeError", "FileNotFoundError", "logging"]
    },
    "except": {
        "alternatives": [],
        "complements": ["try", "finally", "raise"],
        "seealso": ["try", "ValueError", "TypeError"]
    },
    "finally": {
        "alternatives": ["with"],
        "complements": ["try", "except"],
        "seealso": ["try", "with"]
    },
    "raise": {
        "alternatives": [
            "assert",
            ext("sys.exit", "import sys", "Завершает программу с кодом.")
        ],
        "complements": ["try", "except"],
        "seealso": ["try", "ValueError", "TypeError"]
    },
    "with": {
        "alternatives": [
            "try",
            ext("try/finally", "try:\n    ...\nfinally:\n    ...", "Ручное освобождение ресурсов."),
            ext("contextlib", "import contextlib", "Свои контекстные менеджеры.")
        ],
        "complements": ["open", "try", "except"],
        "seealso": ["open", "try", "finally"]
    },

    # ---------------- Асинхронность ----------------
    "async": {
        "alternatives": [
            "threading",
            "multiprocessing",
            ext("concurrent.futures", "import concurrent.futures", "Пулы потоков и процессов.")
        ],
        "complements": ["await", "asyncio"],
        "seealso": ["await", "asyncio", "threading"]
    },
    "await": {
        "alternatives": [
            ext("asyncio.run", "asyncio.run(coro)", "Запуск корутины из синхронного кода.")
        ],
        "complements": ["async", "asyncio"],
        "seealso": ["async", "asyncio"]
    },
    "match": {
        "alternatives": [
            "if",
            "elif",
            ext("Словарная диспетчеризация", "handlers = {'a': f1}", "Словарь функций вместо match.")
        ],
        "complements": ["case"],
        "seealso": ["if", "elif", "case"]
    },
    "case": {
        "alternatives": [],
        "complements": ["match"],
        "seealso": ["match", "if", "elif"]
    },

    # ---------------- Встроенные функции ----------------
    "print": {
        "alternatives": [
            "logging",
            "pprint",
            ext("sys.stdout.write", "sys.stdout.write(text)", "Запись в stdout без перевода строки.")
        ],
        "complements": ["input", "format", "str"],
        "seealso": ["logging", "pprint", "input"]
    },
    "len": {
        "alternatives": [
            ext("obj.__len__()", "obj.__len__()", "Спецметод, который вызывает len()."),
            ext("operator.length_hint", "import operator", "Оценка длины для итераторов.")
        ],
        "complements": ["list", "dict", "str", "set", "tuple"],
        "seealso": ["range"]
    },
    "open": {
        "alternatives": [
            ext("Path.read_text", "Path('f.txt').read_text()", "Быстрое чтение через pathlib."),
            ext("Path.write_text", "Path('f.txt').write_text(t)", "Быстрая запись через pathlib."),
            ext("io.StringIO", "import io", "Файл в памяти для строк.")
        ],
        "complements": ["with", "csv", "json"],
        "seealso": ["with", "FileNotFoundError", "csv"]
    },
    "type": {
        "alternatives": [
            "isinstance",
            ext("obj.__class__", "obj.__class__", "Прямой доступ к классу объекта.")
        ],
        "complements": ["isinstance"],
        "seealso": ["isinstance", "bool"]
    },
    "input": {
        "alternatives": [
            "argparse",
            ext("sys.stdin", "import sys", "Чтение потока ввода.")
        ],
        "complements": ["print", "int", "str"],
        "seealso": ["print", "argparse"]
    },
    "range": {
        "alternatives": [
            "while",
            ext("numpy.arange", "import numpy", "Числовые последовательности в NumPy.")
        ],
        "complements": ["for", "len", "list"],
        "seealso": ["for", "enumerate"]
    },
    "enumerate": {
        "alternatives": [
            "zip",
            ext("Счётчик вручную", "i = 0; i += 1", "Ручной индекс в цикле.")
        ],
        "complements": ["for", "zip"],
        "seealso": ["zip", "for"]
    },
    "zip": {
        "alternatives": [
            "enumerate",
            ext("itertools.zip_longest", "import itertools", "Соединяет последовательности разной длины.")
        ],
        "complements": ["for", "enumerate"],
        "seealso": ["enumerate", "map"]
    },
    "sorted": {
        "alternatives": [
            ext("list.sort()", "items.sort()", "Сортировка списка на месте."),
            ext("heapq", "import heapq", "Эффективные минимумы/максимумы.")
        ],
        "complements": ["lambda", "reversed"],
        "seealso": ["min", "max", "reversed"]
    },
    "isinstance": {
        "alternatives": [
            "type",
            ext("hasattr", "hasattr(obj, 'attr')", "Проверка наличия атрибута.")
        ],
        "complements": ["type"],
        "seealso": ["type"]
    },
    "abs": {
        "alternatives": [
            ext("math.fabs", "import math", "Модуль для float."),
            ext("Условие", "x if x > 0 else -x", "Ручной модуль числа.")
        ],
        "complements": ["round"],
        "seealso": ["round", "math"]
    },
    "round": {
        "alternatives": [
            ext("math.floor / ceil", "import math", "Округление вниз/вверх."),
            ext("decimal.quantize", "import decimal", "Точное округление.")
        ],
        "complements": ["abs"],
        "seealso": ["abs", "decimal"]
    },
    "min": {
        "alternatives": [
            "sorted",
            ext("Цикл", "for x in items: ...", "Ручной поиск минимума.")
        ],
        "complements": ["max", "lambda"],
        "seealso": ["max", "sorted"]
    },
    "max": {
        "alternatives": [
            "sorted",
            ext("Цикл", "for x in items: ...", "Ручной поиск максимума.")
        ],
        "complements": ["min", "lambda"],
        "seealso": ["min", "sorted"]
    },
    "sum": {
        "alternatives": [
            "plus",
            ext("math.fsum", "import math", "Точная сумма float."),
            ext("functools.reduce", "import functools", "Свёртка последовательности.")
        ],
        "complements": ["len"],
        "seealso": ["any", "all", "math"]
    },
    "any": {
        "alternatives": [
            ext("Цикл с break", "for x in items: ...", "Ручная проверка.")
        ],
        "complements": ["all"],
        "seealso": ["all", "or"]
    },
    "all": {
        "alternatives": [
            ext("Цикл с break", "for x in items: ...", "Ручная проверка.")
        ],
        "complements": ["any"],
        "seealso": ["any", "and"]
    },
    "map": {
        "alternatives": [
            "for",
            ext("List comprehension", "[f(x) for x in items]", "Более читаемый вариант.")
        ],
        "complements": ["lambda", "filter"],
        "seealso": ["filter", "list"]
    },
    "filter": {
        "alternatives": [
            ext("List comprehension", "[x for x in items if cond]", "Фильтр в одну строку.")
        ],
        "complements": ["lambda", "map"],
        "seealso": ["map", "any"]
    },
    "reversed": {
        "alternatives": [
            ext("Срез [::-1]", "items[::-1]", "Разворот списка срезом.")
        ],
        "complements": ["list", "sorted"],
        "seealso": ["sorted", "list"]
    },
    "format": {
        "alternatives": [
            "repr",
            ext("f-string", "f'{value:.2f}'", "Современное форматирование."),
            ext("str.format", "'{}'.format(x)", "Метод форматирования строк.")
        ],
        "complements": ["str", "print"],
        "seealso": ["repr", "str"]
    },
    "repr": {
        "alternatives": ["str", "format", "pprint"],
        "complements": [],
        "seealso": ["str", "pprint"]
    },
    "callable": {
        "alternatives": [
            ext("hasattr __call__", "hasattr(obj, '__call__')", "Проверка вызываемости вручную.")
        ],
        "complements": [],
        "seealso": ["def", "lambda"]
    },
    "iter": {
        "alternatives": ["for"],
        "complements": ["next"],
        "seealso": ["next", "for"]
    },
    "next": {
        "alternatives": ["for"],
        "complements": ["iter"],
        "seealso": ["iter"]
    },
    "dir": {
        "alternatives": ["vars"],
        "complements": [],
        "seealso": ["vars"]
    },
    "vars": {
        "alternatives": ["dir"],
        "complements": [],
        "seealso": ["dir"]
    },

    # ---------------- Типы ----------------
    "int": {
        "alternatives": ["float", "decimal"],
        "complements": ["str", "ValueError"],
        "seealso": ["float", "round"]
    },
    "float": {
        "alternatives": ["int", "decimal"],
        "complements": ["round"],
        "seealso": ["int", "decimal"]
    },
    "bool": {
        "alternatives": [],
        "complements": ["not", "if"],
        "seealso": ["True", "False", "not"]
    },
    "str": {
        "alternatives": ["repr", "format"],
        "complements": ["print", "len"],
        "seealso": ["repr", "format"]
    },
    "list": {
        "alternatives": [
            "tuple",
            "set",
            ext("collections.deque", "from collections import deque", "Очередь с быстрыми концами."),
            ext("array", "import array", "Компактные числовые массивы.")
        ],
        "complements": ["len", "for", "sorted"],
        "seealso": ["tuple", "set", "dict"]
    },
    "tuple": {
        "alternatives": [
            "list",
            "dataclasses",
            ext("namedtuple", "from collections import namedtuple", "Именованный кортеж.")
        ],
        "complements": ["len"],
        "seealso": ["list", "set"]
    },
    "set": {
        "alternatives": [
            "list",
            ext("frozenset", "frozenset(items)", "Неизменяемое множество."),
            ext("dict.fromkeys", "dict.fromkeys(items)", "Удаление дубликатов с порядком.")
        ],
        "complements": ["len", "in"],
        "seealso": ["list", "dict"]
    },
    "dict": {
        "alternatives": [
            "dataclasses",
            ext("collections.defaultdict", "from collections import defaultdict", "Словарь со значением по умолчанию."),
            ext("collections.Counter", "from collections import Counter", "Подсчёт элементов.")
        ],
        "complements": ["json", "in", "KeyError"],
        "seealso": ["list", "set", "json"]
    },

    # ---------------- Операторы ----------------
    "plus": {
        "alternatives": [
            "sum",
            ext("str.join", "','.join(items)", "Объединение строк."),
            ext("operator.add", "import operator", "Функциональное сложение.")
        ],
        "complements": [],
        "seealso": ["sum", "minus"]
    },
    "minus": {
        "alternatives": [ext("operator.sub", "import operator", "Функциональное вычитание.")],
        "complements": [],
        "seealso": ["plus"]
    },
    "multiply": {
        "alternatives": [
            ext("math.prod", "import math", "Произведение последовательности."),
            ext("operator.mul", "import operator", "Функциональное умножение.")
        ],
        "complements": [],
        "seealso": ["divide", "sum"]
    },
    "divide": {
        "alternatives": [
            ext("Целочисленное //", "a // b", "Деление с отбросом остатка.")
        ],
        "complements": [],
        "seealso": ["ZeroDivisionError", "multiply"]
    },

    # ---------------- Исключения ----------------
    "ValueError": {
        "alternatives": ["TypeError"],
        "complements": ["try", "except", "raise"],
        "seealso": ["TypeError", "try"]
    },
    "TypeError": {
        "alternatives": ["ValueError"],
        "complements": ["try", "except", "isinstance"],
        "seealso": ["ValueError", "isinstance"]
    },
    "KeyError": {
        "alternatives": [
            ext("dict.get", "data.get(key)", "Не бросает исключение."),
            ext("in-проверка", "if key in data:", "Проверка перед доступом.")
        ],
        "complements": ["try", "except", "dict"],
        "seealso": ["dict", "IndexError"]
    },
    "IndexError": {
        "alternatives": [
            ext("len-проверка", "if i < len(items):", "Проверка границы."),
            ext("Срез", "items[i:i+1]", "Безопасный доступ срезом.")
        ],
        "complements": ["try", "except", "list"],
        "seealso": ["list", "KeyError"]
    },
    "FileNotFoundError": {
        "alternatives": [
            ext("os.path.exists", "import os.path", "Проверка существования файла."),
            ext("Path.exists", "Path('f').exists()", "Проверка через pathlib.")
        ],
        "complements": ["try", "except", "open"],
        "seealso": ["open", "os", "pathlib"]
    },
    "AttributeError": {
        "alternatives": [
            ext("hasattr", "hasattr(obj, 'a')", "Проверка атрибута."),
            ext("getattr", "getattr(obj, 'a', default)", "Безопасное чтение атрибута.")
        ],
        "complements": ["try", "except"],
        "seealso": ["type"]
    },
    "ZeroDivisionError": {
        "alternatives": [
            ext("Проверка if", "if b != 0:", "Проверка делителя заранее.")
        ],
        "complements": ["try", "except", "divide"],
        "seealso": ["divide", "try"]
    },

    # ---------------- Модули ----------------
    "os": {
        "alternatives": ["pathlib", "shutil", "subprocess"],
        "complements": ["sys", "pathlib"],
        "seealso": ["pathlib", "shutil", "subprocess"]
    },
    "sys": {
        "alternatives": ["os", "argparse"],
        "complements": ["os", "print"],
        "seealso": ["os", "argparse"]
    },
    "json": {
        "alternatives": [
            "csv",
            ext("pickle", "import pickle", "Сериализация Python-объектов."),
            ext("yaml", "import yaml", "Формат YAML (PyYAML).")
        ],
        "complements": ["dict", "open", "requests"],
        "seealso": ["dict", "csv"]
    },
    "pathlib": {
        "alternatives": ["os", "glob"],
        "complements": ["open", "shutil"],
        "seealso": ["os", "glob", "shutil"]
    },
    "math": {
        "alternatives": ["numpy", "statistics"],
        "complements": ["round", "abs"],
        "seealso": ["statistics", "decimal"]
    },
    "random": {
        "alternatives": [
            ext("secrets", "import secrets", "Криптостойкая случайность."),
            ext("numpy.random", "import numpy", "Случайные массивы.")
        ],
        "complements": [],
        "seealso": ["uuid", "time"]
    },
    "datetime": {
        "alternatives": [
            "time",
            ext("arrow", "import arrow", "Удобная работа с датами."),
            ext("pendulum", "import pendulum", "Расширенные даты.")
        ],
        "complements": [],
        "seealso": ["time"]
    },
    "re": {
        "alternatives": [
            "str",
            "glob",
            ext("fnmatch", "import fnmatch", "Простые шаблоны имён файлов.")
        ],
        "complements": ["str"],
        "seealso": ["str", "glob"]
    },
    "collections": {
        "alternatives": ["itertools"],
        "complements": ["itertools", "dict"],
        "seealso": ["itertools", "dict"]
    },
    "itertools": {
        "alternatives": ["for"],
        "complements": ["collections", "functools"],
        "seealso": ["collections", "functools"]
    },
    "time": {
        "alternatives": ["datetime"],
        "complements": ["datetime"],
        "seealso": ["datetime", "asyncio"]
    },
    "subprocess": {
        "alternatives": [
            "os",
            ext("os.system", "os.system('cmd')", "Простой, но небезопасный запуск.")
        ],
        "complements": ["os", "shutil"],
        "seealso": ["os", "git"]
    },
    "shutil": {
        "alternatives": ["os", "pathlib", "copy", "move"],
        "complements": ["os", "pathlib"],
        "seealso": ["os", "copy", "move"]
    },
    "logging": {
        "alternatives": [
            "print",
            ext("warnings", "import warnings", "Предупреждения для разработчиков.")
        ],
        "complements": ["try", "except"],
        "seealso": ["print", "pytest"]
    },
    "argparse": {
        "alternatives": [
            "sys",
            ext("click", "import click", "Удобный CLI-фреймворк."),
            ext("typer", "import typer", "CLI на основе аннотаций.")
        ],
        "complements": ["sys", "input"],
        "seealso": ["sys", "pip-install"]
    },
    "typing": {
        "alternatives": [],
        "complements": ["dataclasses"],
        "seealso": ["dataclasses"]
    },
    "dataclasses": {
        "alternatives": [
            "class",
            ext("namedtuple", "from collections import namedtuple", "Лёгкие структуры."),
            ext("pydantic", "import pydantic", "Классы с валидацией.")
        ],
        "complements": ["typing", "class"],
        "seealso": ["class", "typing"]
    },
    "asyncio": {
        "alternatives": [
            "threading",
            "multiprocessing",
            ext("trio", "import trio", "Альтернативная async-библиотека.")
        ],
        "complements": ["async", "await"],
        "seealso": ["async", "await", "threading"]
    },
    "csv": {
        "alternatives": ["pandas", "json"],
        "complements": ["open", "dict"],
        "seealso": ["json", "pandas"]
    },
    "sqlite3": {
        "alternatives": [
            "json",
            ext("SQLAlchemy", "import sqlalchemy", "ORM и работа с БД."),
            ext("peewee", "import peewee", "Лёгкая ORM.")
        ],
        "complements": [],
        "seealso": ["json", "pandas"]
    },
    "urllib-request": {
        "alternatives": ["requests", "curl", "wget"],
        "complements": ["json"],
        "seealso": ["requests", "curl"]
    },
    "socket": {
        "alternatives": ["asyncio"],
        "complements": ["threading"],
        "seealso": ["asyncio", "threading"]
    },
    "threading": {
        "alternatives": ["asyncio", "multiprocessing"],
        "complements": ["time"],
        "seealso": ["multiprocessing", "asyncio"]
    },
    "multiprocessing": {
        "alternatives": ["threading", "asyncio"],
        "complements": ["os", "subprocess"],
        "seealso": ["threading", "asyncio"]
    },
    "functools": {
        "alternatives": ["itertools"],
        "complements": ["itertools", "operator"],
        "seealso": ["itertools", "operator"]
    },
    "operator": {
        "alternatives": ["lambda"],
        "complements": ["functools", "sorted"],
        "seealso": ["lambda", "functools"]
    },
    "copy": {
        "alternatives": [
            ext("Срез", "items[:]", "Копия списка срезом."),
            ext("dict.copy", "data.copy()", "Копия словаря.")
        ],
        "complements": [],
        "seealso": ["list", "dict"]
    },
    "pprint": {
        "alternatives": ["print", "repr", "json"],
        "complements": ["dict", "list"],
        "seealso": ["print", "repr"]
    },
    "tempfile": {
        "alternatives": ["pathlib"],
        "complements": ["os", "shutil"],
        "seealso": ["os", "shutil"]
    },
    "glob": {
        "alternatives": ["pathlib", "os"],
        "complements": ["os", "pathlib"],
        "seealso": ["pathlib", "os"]
    },
    "hashlib": {
        "alternatives": [ext("secrets", "import secrets", "Токены и случайность.")],
        "complements": ["base64"],
        "seealso": ["base64", "uuid"]
    },
    "base64": {
        "alternatives": [],
        "complements": [],
        "seealso": ["hashlib"]
    },
    "uuid": {
        "alternatives": ["random"],
        "complements": [],
        "seealso": ["random", "hashlib"]
    },
    "decimal": {
        "alternatives": ["float"],
        "complements": ["round"],
        "seealso": ["float", "math"]
    },
    "statistics": {
        "alternatives": ["numpy", "math"],
        "complements": ["math"],
        "seealso": ["math", "numpy"]
    },

    # ---------------- Python CLI ----------------
    "python": {
        "alternatives": [
            ext("python3", "python3", "Команда Python 3 в Linux/macOS."),
            ext("py", "py", "Python Launcher в Windows."),
            ext("ipython", "ipython", "Улучшенная интерактивная консоль.")
        ],
        "complements": ["pip", "python-m-venv"],
        "seealso": ["pip", "python-script"]
    },
    "python-script": {
        "alternatives": [
            ext("python -c", "python -c 'code'", "Выполнение кода из строки.")
        ],
        "complements": ["python"],
        "seealso": ["python", "python-version"]
    },
    "python-version": {
        "alternatives": [ext("sys.version", "import sys", "Версия из кода.")],
        "complements": ["python"],
        "seealso": ["python", "sys"]
    },
    "pip": {
        "alternatives": [
            "python-m-pip",
            ext("uv", "uv pip install ...", "Очень быстрый менеджер пакетов."),
            ext("poetry", "poetry add ...", "Менеджер зависимостей и сборки."),
            ext("conda", "conda install ...", "Окружения Conda.")
        ],
        "complements": ["pip-install", "python-m-venv"],
        "seealso": ["pip-install", "pip-list"]
    },
    "pip-install": {
        "alternatives": [
            ext("pip install -r", "pip install -r req.txt", "Установка из файла.")
        ],
        "complements": ["pip", "pip-freeze"],
        "seealso": ["pip", "pip-freeze"]
    },
    "pip-list": {
        "alternatives": ["pip-freeze", "pip-show"],
        "complements": ["pip"],
        "seealso": ["pip-freeze", "pip-show"]
    },
    "pip-freeze": {
        "alternatives": [
            "pip-list",
            ext("poetry export", "poetry export", "Экспорт зависимостей Poetry."),
            ext("uv pip freeze", "uv pip freeze", "Аналог freeze в uv.")
        ],
        "complements": ["pip-install", "python-m-venv"],
        "seealso": ["pip-list", "pip-show"]
    },
    "pip-show": {
        "alternatives": [
            "pip-list",
            "pip-freeze",
            ext("importlib.metadata", "import importlib.metadata", "Метаданные пакетов из кода.")
        ],
        "complements": ["pip", "pip-install"],
        "seealso": ["pip-freeze", "pip-list"]
    },
    "python-m-pip": {
        "alternatives": ["pip"],
        "complements": ["pip-install", "pip-freeze", "pip-show", "pip-list"],
        "seealso": ["pip", "python"]
    },
    "python-m-venv": {
        "alternatives": [
            ext("virtualenv", "pip install virtualenv", "Классический инструмент окружений."),
            ext("conda", "conda create -n env", "Окружения Conda."),
            ext("uv venv", "uv venv", "Быстрое создание окружений.")
        ],
        "complements": ["pip-install", "pip-freeze"],
        "seealso": ["pip", "python"]
    },
    "python-m-http-server": {
        "alternatives": ["flask", "fastapi"],
        "complements": ["python"],
        "seealso": ["flask", "fastapi"]
    },

    # ---------------- Пакеты ----------------
    "requests": {
        "alternatives": [
            "urllib-request",
            "curl",
            ext("httpx", "import httpx", "Современный клиент с async."),
            ext("aiohttp", "import aiohttp", "Асинхронные HTTP-запросы.")
        ],
        "complements": ["json"],
        "seealso": ["json", "curl", "urllib-request"]
    },
    "pandas": {
        "alternatives": [
            "csv",
            "numpy",
            ext("polars", "import polars", "Быстрые табличные данные.")
        ],
        "complements": ["numpy", "csv"],
        "seealso": ["numpy", "csv"]
    },
    "django": {
        "alternatives": ["flask", "fastapi"],
        "complements": ["sqlite3", "pytest"],
        "seealso": ["flask", "fastapi"]
    },
    "numpy": {
        "alternatives": ["list", "pandas"],
        "complements": ["pandas", "math"],
        "seealso": ["pandas", "math"]
    },
    "flask": {
        "alternatives": ["fastapi", "django", "python-m-http-server"],
        "complements": ["pytest", "requests"],
        "seealso": ["fastapi", "django"]
    },
    "fastapi": {
        "alternatives": ["flask", "django"],
        "complements": ["pytest", "requests", "typing"],
        "seealso": ["flask", "django"]
    },
    "pytest": {
        "alternatives": [
            ext("unittest", "import unittest", "Встроенный фреймворк тестов.")
        ],
        "complements": ["assert", "logging"],
        "seealso": ["assert", "black"]
    },
    "black": {
        "alternatives": [
            ext("ruff", "ruff format", "Быстрый форматтер и линтер."),
            ext("autopep8", "autopep8", "Приведение к PEP8."),
            ext("yapf", "yapf", "Форматтер от Google.")
        ],
        "complements": ["pytest"],
        "seealso": ["pytest"]
    },

    # ---------------- Dev tools и сеть ----------------
    "git": {
        "alternatives": [
            ext("GitHub Desktop", "GUI", "Графический клиент GitHub."),
            ext("Mercurial", "hg", "Другая распределённая VCS."),
            ext("Subversion", "svn", "Централизованная VCS.")
        ],
        "complements": [],
        "seealso": ["subprocess"]
    },
    "curl": {
        "alternatives": [
            "wget",
            "requests",
            "urllib-request",
            ext("httpx", "httpx url", "Современная CLI-утилита."),
            ext("Invoke-WebRequest", "iwr url", "Аналог в PowerShell.")
        ],
        "complements": ["ping", "json"],
        "seealso": ["wget", "requests"]
    },
    "wget": {
        "alternatives": [
            "curl",
            "requests",
            ext("aria2c", "aria2c url", "Многопоточная загрузка.")
        ],
        "complements": ["curl"],
        "seealso": ["curl", "requests"]
    },

    # ---------------- OS команды ----------------
    "ipconfig": {
        "alternatives": [
            ext("ip addr", "ip addr", "Современная команда Linux."),
            ext("ifconfig", "ifconfig", "Классика Unix.")
        ],
        "complements": ["ping"],
        "seealso": ["ping", "curl"]
    },
    "ping": {
        "alternatives": [
            "curl",
            ext("traceroute", "traceroute host", "Показывает маршрут пакетов.")
        ],
        "complements": ["ipconfig"],
        "seealso": ["ipconfig", "curl"]
    },
    "cd": {
        "alternatives": [ext("pushd / popd", "pushd dir", "Стек папок.")],
        "complements": ["dir", "ls", "mkdir"],
        "seealso": ["dir", "ls"]
    },
    "dir": {
        "alternatives": ["ls", "glob"],
        "complements": ["cd"],
        "seealso": ["ls", "cd"]
    },
    "ls": {
        "alternatives": ["dir"],
        "complements": ["cd"],
        "seealso": ["dir", "cd"]
    },
    "mkdir": {
        "alternatives": [
            ext("os.makedirs", "import os", "Создание папок из кода."),
            ext("Path.mkdir", "Path('d').mkdir()", "Создание через pathlib.")
        ],
        "complements": ["cd", "rm"],
        "seealso": ["rm", "cd"]
    },
    "rm": {
        "alternatives": [
            "del",
            ext("shutil.rmtree", "import shutil", "Удаление папки с содержимым.")
        ],
        "complements": ["copy", "move"],
        "seealso": ["copy", "move"]
    },
    "copy": {
        "alternatives": ["move", "shutil"],
        "complements": ["move", "rm"],
        "seealso": ["move", "rm"]
    },
    "move": {
        "alternatives": ["copy", "shutil"],
        "complements": ["copy", "rm"],
        "seealso": ["copy", "rm"]
    },
    "echo": {
        "alternatives": ["print"],
        "complements": [],
        "seealso": ["print", "cls"]
    },
    "cls": {
        "alternatives": ["clear"],
        "complements": [],
        "seealso": ["clear", "echo"]
    },
    "clear": {
        "alternatives": ["cls"],
        "complements": [],
        "seealso": ["cls"]
    }
}


def related_key(item):
    if isinstance(item, str):
        return f"id:{item}"

    if isinstance(item, dict):
        if item.get("id"):
            return f"id:{item['id']}"
        return f"name:{item.get('name', '')}|syntax:{item.get('syntax', '')}"

    return f"raw:{str(item)}"


def merge_list(existing, extra, ids):
    existing = list(existing or [])
    keys = {related_key(item) for item in existing}

    for item in extra:
        # пропускаем строки, для которых нет карточки
        if isinstance(item, str) and item not in ids:
            continue

        key = related_key(item)

        if key not in keys:
            existing.append(item)
            keys.add(key)

    return existing


def main():
    payload = None
    source_path = None

    for path in INPUT_PATHS:
        if path.exists():
            payload = json.loads(path.read_text(encoding="utf-8"))
            source_path = path
            break

    if payload is None:
        print("Не найден entries.json. Сначала запусти build_entries.py и enhance_entries.py")
        return

    if isinstance(payload, list):
        payload = {"meta": {}, "entries": payload}

    entries = payload.get("entries", [])
    ids = {entry["id"] for entry in entries if "id" in entry}

    updated = 0

    for entry in entries:
        extra = RELATED.get(entry.get("id"))

        if not extra:
            continue

        related = entry.setdefault("related", {})

        if not isinstance(related, dict):
            related = {}
            entry["related"] = related

        for key in ["alternatives", "complements", "seealso"]:
            related[key] = merge_list(related.get(key, []), extra.get(key, []), ids)

        updated += 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Updated related for {updated} entries. Source: {source_path}")


if __name__ == "__main__":
    main()