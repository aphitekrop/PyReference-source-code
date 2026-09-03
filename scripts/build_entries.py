#!/usr/bin/env python3
import json
from pathlib import Path


PYTHON_VERSIONS = [
    {
        "version": "3.13",
        "status": "latest",
        "released": "2024-10",
        "url": "https://www.python.org/downloads/"
    },
    {
        "version": "3.12",
        "status": "stable",
        "released": "2023-10"
    },
    {
        "version": "3.11",
        "status": "stable",
        "released": "2022-10"
    }
]


RAW = [
    ("if", "if", "keyword", "core", "Условный оператор. Выполняет блок кода, если условие истинно.", "if condition:", "if x > 0: print('positive')", ["условие", "if"]),
    ("for", "for", "keyword", "core", "Цикл для перебора элементов итерируемого объекта.", "for item in iterable:", "for i in range(3): print(i)", ["цикл", "for"]),
    ("def", "def", "keyword", "core", "Объявляет функцию.", "def name(parameters):", "def hello(): return 'hi'", ["функция", "def"]),
    ("class", "class", "keyword", "core", "Объявляет класс.", "class Name:", "class User: pass", ["класс", "ООП"]),
    ("import", "import", "keyword", "core", "Импортирует модуль или объект из модуля.", "import module", "import os", ["импорт", "модуль"]),
    ("return", "return", "keyword", "core", "Возвращает значение из функции.", "return value", "def f(): return 42", ["функция", "return"]),
    ("print", "print()", "builtin-function", "builtin", "Выводит объекты в стандартный поток вывода.", "print(*objects, sep=' ', end='\\n')", "print('Hello, Python')", ["вывод", "консоль", "print"]),
    ("len", "len()", "builtin-function", "builtin", "Возвращает количество элементов объекта.", "len(obj)", "print(len([1, 2, 3]))", ["длина", "len"]),
    ("open", "open()", "builtin-function", "builtin", "Открывает файл и возвращает файловый объект.", "open(file, mode='r', encoding=None)", "file = open('app.py', encoding='utf-8')", ["файл", "open"]),
    ("type", "type()", "builtin-function", "builtin", "Возвращает тип объекта или создаёт новый тип.", "type(obj)", "print(type(123))", ["тип", "type"]),
    ("input", "input()", "builtin-function", "builtin", "Читает строку из стандартного ввода.", "input(prompt='')", "name = input('Имя: ')", ["ввод", "input"]),
    ("range", "range()", "builtin-function", "builtin", "Создаёт неизменяемую последовательность чисел.", "range(start, stop, step)", "for i in range(5): print(i)", ["диапазон", "цикл", "range"]),
    ("enumerate", "enumerate()", "builtin-function", "builtin", "Возвращает пары индекс-значение для итерируемого объекта.", "enumerate(iterable, start=0)", "for i, value in enumerate(['a', 'b']): print(i, value)", ["индекс", "enumerate"]),
    ("zip", "zip()", "builtin-function", "builtin", "Объединяет несколько итерируемых объектов в кортежи.", "zip(*iterables)", "list(zip([1, 2], ['a', 'b']))", ["zip", "итерация"]),
    ("sorted", "sorted()", "builtin-function", "builtin", "Возвращает отсортированный список из элементов итерируемого объекта.", "sorted(iterable, key=None, reverse=False)", "sorted([3, 1, 2])", ["сортировка", "sorted"]),
    ("isinstance", "isinstance()", "builtin-function", "builtin", "Проверяет, является ли объект экземпляром типа или кортежа типов.", "isinstance(obj, classinfo)", "isinstance('a', str)", ["тип", "проверка", "isinstance"]),
    ("int", "int", "builtin-type", "types", "Целочисленный тип данных.", "int(value=0)", "x = int('42')", ["число", "int"]),
    ("str", "str", "builtin-type", "types", "Строковый тип данных.", "str(object='')", "text = str('hello')", ["строка", "str"]),
    ("list", "list", "builtin-type", "types", "Изменяемый упорядоченный список.", "list(iterable=())", "items = list([1, 2, 3])", ["список", "list"]),
    ("dict", "dict", "builtin-type", "types", "Словарь: коллекция пар ключ-значение.", "dict(**kwargs)", "data = dict(name='Alice', age=30)", ["словарь", "dict"]),
    ("float", "float", "builtin-type", "types", "Число с плавающей точкой.", "float(value=0.0)", "pi = float('3.14')", ["число", "float"]),
    ("bool", "bool", "builtin-type", "types", "Логический тип: True или False.", "bool(value)", "flag = bool(1)", ["bool", "логика"]),
    ("tuple", "tuple", "builtin-type", "types", "Неизменяемый упорядоченный кортеж.", "tuple(iterable=())", "point = tuple((1, 2))", ["кортеж", "tuple"]),
    ("set", "set", "builtin-type", "types", "Множество уникальных элементов.", "set(iterable=())", "unique = set([1, 1, 2])", ["множество", "set"]),
    ("plus", "+", "operator", "operators", "Сложение чисел или объединение последовательностей.", "a + b", "2 + 2", ["сложение", "оператор"]),
    ("minus", "-", "operator", "operators", "Вычитание чисел.", "a - b", "5 - 2", ["вычитание", "оператор"]),
    ("multiply", "*", "operator", "operators", "Умножение чисел или повторение последовательностей.", "a * b", "3 * 4", ["умножение", "оператор"]),
    ("divide", "/", "operator", "operators", "Деление чисел, всегда возвращает float.", "a / b", "10 / 2", ["деление", "оператор"]),
    ("equals", "==", "operator", "operators", "Проверяет равенство значений.", "a == b", "1 == 1", ["равенство", "сравнение"]),
    ("not-equals", "!=", "operator", "operators", "Проверяет неравенство значений.", "a != b", "1 != 2", ["неравенство", "сравнение"]),
    ("in", "in", "operator", "operators", "Проверяет наличие элемента в коллекции.", "item in collection", "'a' in ['a', 'b']", ["in", "проверка"]),
    ("is", "is", "operator", "operators", "Проверяет, указывают ли объекты на один и тот же объект.", "a is b", "None is None", ["is", "идентичность"]),
    ("and", "and", "operator", "operators", "Логическое И.", "a and b", "x > 0 and x < 10", ["логика", "and"]),
    ("or", "or", "operator", "operators", "Логическое ИЛИ.", "a or b", "x < 0 or x > 10", ["логика", "or"]),
    ("ValueError", "ValueError", "exception", "exceptions", "Ошибка, когда функция получает аргумент правильного типа, но недопустимого значения.", "raise ValueError('message')", "int('abc')", ["ошибка", "значение"]),
    ("TypeError", "TypeError", "exception", "exceptions", "Ошибка операции над объектом неподходящего типа.", "raise TypeError('message')", "len(5)", ["ошибка", "тип"]),
    ("KeyError", "KeyError", "exception", "exceptions", "Ошибка доступа к несуществующему ключу словаря.", "raise KeyError('message')", "{}['missing']", ["ошибка", "словарь"]),
    ("IndexError", "IndexError", "exception", "exceptions", "Ошибка обращения к несуществующему индексу последовательности.", "raise IndexError('message')", "[1, 2][5]", ["ошибка", "индекс"]),
    ("FileNotFoundError", "FileNotFoundError", "exception", "exceptions", "Файл или папка не найдены.", "raise FileNotFoundError('message')", "open('missing.txt')", ["ошибка", "файл"]),
    ("AttributeError", "AttributeError", "exception", "exceptions", "Ошибка доступа к несуществующему атрибуту объекта.", "raise AttributeError('message')", "'abc'.missing()", ["ошибка", "атрибут"]),
    ("ZeroDivisionError", "ZeroDivisionError", "exception", "exceptions", "Деление на ноль.", "raise ZeroDivisionError('message')", "1 / 0", ["ошибка", "деление"]),
    ("os", "os", "module", "stdlib", "Модуль для работы с операционной системой: файлы, папки, окружение.", "import os", "import os; os.getcwd()", ["os", "система"]),
    ("sys", "sys", "module", "stdlib", "Модуль для работы с интерпретатором Python: аргументы, пути, версии.", "import sys", "import sys; sys.version", ["sys", "интерпретатор"]),
    ("json", "json", "module", "stdlib", "Модуль для работы с JSON.", "import json", "import json; json.dumps({'a': 1})", ["json", "данные"]),
    ("pathlib", "pathlib", "module", "stdlib", "Объектная работа с путями файловой системы.", "from pathlib import Path", "from pathlib import Path; Path('data').mkdir(exist_ok=True)", ["путь", "файлы", "pathlib"]),
    ("math", "math", "module", "stdlib", "Математические функции.", "import math", "import math; math.sqrt(16)", ["математика", "math"]),
    ("random", "random", "module", "stdlib", "Генерация псевдослучайных чисел.", "import random", "import random; random.randint(1, 10)", ["random", "случайно"]),
    ("datetime", "datetime", "module", "stdlib", "Работа с датой и временем.", "import datetime", "import datetime; datetime.datetime.now()", ["дата", "время"]),
    ("re", "re", "module", "stdlib", "Регулярные выражения.", "import re", "import re; re.findall(r'\\d+', 'a1 b2')", ["regex", "re"]),
    ("collections", "collections", "module", "stdlib", "Специализированные контейнеры: Counter, deque, namedtuple и другие.", "import collections", "import collections; collections.Counter(['a', 'a', 'b'])", ["коллекции", "Counter"]),
    ("itertools", "itertools", "module", "stdlib", "Эффективные итераторы и комбинаторные функции.", "import itertools", "import itertools; itertools.product([0, 1], repeat=2)", ["итераторы", "itertools"]),
    ("python", "python", "cli", "python-cli", "Запуск интерпретатора Python. В некоторых системах используется python3.", "python", "python", ["python", "cli"]),
    ("python-script", "python script.py", "cli", "python-cli", "Запуск Python-скрипта.", "python script.py", "python main.py", ["запуск", "скрипт"]),
    ("python-version", "python --version", "cli", "python-cli", "Показывает версию Python.", "python --version", "python --version", ["версия", "cli"]),
    ("pip", "pip", "cli", "python-cli", "Пакетный менеджер Python для установки библиотек.", "pip command", "pip --help", ["pip", "пакеты"]),
    ("pip-install", "pip install", "cli", "python-cli", "Устанавливает пакет из PyPI.", "pip install package", "pip install requests", ["установка", "pip"]),
    ("pip-list", "pip list", "cli", "python-cli", "Показывает установленные пакеты.", "pip list", "pip list", ["пакеты", "список"]),
    ("python-m-venv", "python -m venv", "cli", "python-cli", "Создаёт виртуальное окружение Python.", "python -m venv .venv", "python -m venv .venv", ["venv", "окружение"]),
    ("python-m-http-server", "python -m http.server", "cli", "python-cli", "Запускает простой локальный HTTP-сервер.", "python -m http.server 8000", "python -m http.server 8000", ["сервер", "http"]),
    ("requests", "requests", "library", "packages", "Популярная библиотека для HTTP-запросов.", "pip install requests", "import requests; requests.get('https://example.com')", ["http", "requests"]),
    ("pandas", "pandas", "library", "packages", "Библиотека для анализа данных и таблиц.", "pip install pandas", "import pandas; pandas.read_csv('data.csv')", ["данные", "pandas"]),
    ("django", "Django", "library", "packages", "Фреймворк для веб-приложений.", "pip install django", "django-admin startproject mysite", ["web", "django"]),
    ("numpy", "NumPy", "library", "packages", "Библиотека для числовых вычислений и массивов.", "pip install numpy", "import numpy; numpy.array([1, 2, 3])", ["числа", "numpy"]),
    ("flask", "Flask", "library", "packages", "Минималистичный веб-фреймворк.", "pip install flask", "from flask import Flask", ["web", "flask"]),
    ("fastapi", "FastAPI", "library", "packages", "Современный фреймворк для API.", "pip install fastapi", "from fastapi import FastAPI", ["api", "fastapi"]),
    ("pytest", "pytest", "library", "packages", "Фреймворк для тестирования.", "pip install pytest", "pytest tests/", ["тесты", "pytest"]),
    ("black", "black", "library", "packages", "Форматировщик кода Python.", "pip install black", "black .", ["форматирование", "black"]),
    ("ipconfig", "ipconfig", "os-command", "os", "Сетевые настройки Windows. Аналог в Linux: ip addr или ifconfig.", "ipconfig", "ipconfig /all", ["сеть", "windows"]),
    ("ping", "ping", "os-command", "os", "Проверяет доступность узла по сети.", "ping host", "ping example.com", ["сеть", "ping"]),
    ("cd", "cd", "os-command", "os", "Сменяет текущую папку.", "cd path", "cd projects", ["папка", "cd"]),
    ("dir", "dir", "os-command", "os", "Показывает содержимое папки в Windows. Аналог в Linux/macOS: ls.", "dir", "dir", ["файлы", "windows"]),
    ("ls", "ls", "os-command", "os", "Показывает содержимое папки в Linux/macOS.", "ls", "ls -la", ["файлы", "linux"]),
    ("mkdir", "mkdir", "os-command", "os", "Создаёт папку.", "mkdir folder", "mkdir my_project", ["папка", "создать"]),
    ("rm", "rm", "os-command", "os", "Удаляет файлы или папки в Unix-системах. Используй осторожно.", "rm file", "rm temp.txt", ["удалить", "linux"]),
    ("copy", "copy", "os-command", "os", "Копирует файлы в Windows. Аналог в Unix: cp.", "copy source destination", "copy a.txt b.txt", ["копировать", "windows"]),
    ("move", "move", "os-command", "os", "Перемещает файлы в Windows. Аналог в Unix: mv.", "move source destination", "move a.txt backup.txt", ["переместить", "windows"]),
    ("echo", "echo", "os-command", "os", "Выводит текст в консоль.", "echo text", "echo Hello", ["вывод", "echo"]),
    ("cls", "cls", "os-command", "os", "Очищает консоль в Windows.", "cls", "cls", ["очистить", "windows"]),
    ("clear", "clear", "os-command", "os", "Очищает терминал в Linux/macOS.", "clear", "clear", ["очистить", "linux"]),
    ("curl", "curl", "os-command", "os", "Загружает данные по URL из командной строки.", "curl url", "curl https://example.com", ["сеть", "curl"])
]


RELATED = {
    "print": {
        "alternatives": [
            {
                "name": "sys.stdout.write()",
                "syntax": "sys.stdout.write(text)",
                "note": "Записывает текст напрямую в стандартный вывод без автоматического перевода строки."
            },
            {
                "name": "logging",
                "syntax": "import logging; logging.info('message')",
                "note": "Подходит для логов, уровней важности и записи в файл."
            },
            {
                "name": "pprint",
                "syntax": "from pprint import pprint; pprint(data)",
                "note": "Удобный вывод сложных структур данных."
            }
        ],
        "complements": [
            "sys",
            "open"
        ],
        "seealso": [
            "input"
        ]
    },
    "len": {
        "alternatives": [
            {
                "name": "obj.__len__()",
                "syntax": "obj.__len__()",
                "note": "Специальный метод, который обычно вызывает len()."
            },
            {
                "name": "operator.length_hint()",
                "syntax": "operator.length_hint(obj)",
                "note": "Полезно для итераторов, где точная длина заранее неизвестна."
            }
        ],
        "complements": [
            "list",
            "dict",
            "str"
        ],
        "seealso": []
    },
    "open": {
        "alternatives": [
            {
                "name": "Path.read_text()",
                "syntax": "Path('file.txt').read_text(encoding='utf-8')",
                "note": "Быстрое чтение текстового файла через pathlib."
            },
            {
                "name": "Path.write_text()",
                "syntax": "Path('file.txt').write_text(text, encoding='utf-8')",
                "note": "Быстрая запись текста через pathlib."
            },
            {
                "name": "io.StringIO",
                "syntax": "import io; buffer = io.StringIO()",
                "note": "Файлоподобный объект для работы со строками в памяти."
            }
        ],
        "complements": [
            "pathlib",
            "os"
        ],
        "seealso": [
            "FileNotFoundError"
        ]
    },
    "type": {
        "alternatives": [
            "isinstance",
            {
                "name": "types",
                "syntax": "import types",
                "note": "Модуль с типами для более тонких проверок."
            }
        ],
        "complements": [
            "int",
            "str",
            "list",
            "dict"
        ],
        "seealso": []
    },
    "if": {
        "alternatives": [
            {
                "name": "Тернарное выражение",
                "syntax": "x if condition else y",
                "note": "Короткое условие внутри выражения."
            },
            {
                "name": "match",
                "syntax": "match value:\n    case ...:",
                "note": "Конструкция match/case для сложного сопоставления."
            }
        ],
        "complements": [],
        "seealso": [
            "for",
            "while"
        ]
    },
    "for": {
        "alternatives": [
            {
                "name": "while",
                "syntax": "while condition:",
                "note": "Цикл с условием, а не перебором элементов."
            },
            {
                "name": "list comprehension",
                "syntax": "[x * 2 for x in items]",
                "note": "Создание списка на основе итерации."
            },
            {
                "name": "map()",
                "syntax": "map(func, iterable)",
                "note": "Применяет функцию к элементам."
            }
        ],
        "complements": [
            "range",
            "enumerate",
            "zip"
        ],
        "seealso": []
    },
    "def": {
        "alternatives": [
            {
                "name": "lambda",
                "syntax": "lambda x: x + 1",
                "note": "Короткая анонимная функция."
            },
            {
                "name": "Callable class",
                "syntax": "class Handler:\n    def __call__(self):\n        ...",
                "note": "Объект, который можно вызывать как функцию."
            }
        ],
        "complements": [
            "return"
        ],
        "seealso": [
            "class"
        ]
    },
    "class": {
        "alternatives": [
            {
                "name": "dataclasses",
                "syntax": "from dataclasses import dataclass",
                "note": "Удобное создание классов для хранения данных."
            },
            {
                "name": "namedtuple",
                "syntax": "from collections import namedtuple",
                "note": "Лёгкие неизменяемые структуры данных."
            }
        ],
        "complements": [
            "def"
        ],
        "seealso": []
    },
    "import": {
        "alternatives": [
            {
                "name": "from ... import ...",
                "syntax": "from module import name",
                "note": "Импортирует конкретный объект из модуля."
            },
            {
                "name": "importlib",
                "syntax": "import importlib",
                "note": "Динамический импорт модулей."
            }
        ],
        "complements": [
            "os",
            "sys",
            "json",
            "pathlib"
        ],
        "seealso": []
    },
    "return": {
        "alternatives": [
            {
                "name": "yield",
                "syntax": "yield value",
                "note": "Используется в генераторах."
            },
            {
                "name": "raise",
                "syntax": "raise Exception('message')",
                "note": "Прерывает выполнение через исключение."
            }
        ],
        "complements": [
            "def"
        ],
        "seealso": []
    },
    "int": {
        "alternatives": [
            "float",
            {
                "name": "decimal.Decimal",
                "syntax": "from decimal import Decimal",
                "note": "Точные десятичные вычисления."
            }
        ],
        "complements": [
            "str",
            "ValueError"
        ],
        "seealso": []
    },
    "str": {
        "alternatives": [
            {
                "name": "f-string",
                "syntax": "f'Hello, {name}'",
                "note": "Удобное форматирование строк."
            },
            {
                "name": "repr()",
                "syntax": "repr(obj)",
                "note": "Строковое представление объекта, удобное для отладки."
            }
        ],
        "complements": [
            "print"
        ],
        "seealso": []
    },
    "list": {
        "alternatives": [
            "tuple",
            "set",
            {
                "name": "collections.deque",
                "syntax": "from collections import deque",
                "note": "Двусторонняя очередь, эффективная для добавления и удаления с концов."
            },
            {
                "name": "array",
                "syntax": "import array",
                "note": "Компактные массивы числовых данных."
            }
        ],
        "complements": [
            "len",
            "enumerate"
        ],
        "seealso": []
    },
    "dict": {
        "alternatives": [
            {
                "name": "collections.defaultdict",
                "syntax": "from collections import defaultdict",
                "note": "Словарь со значением по умолчанию для отсутствующих ключей."
            },
            {
                "name": "collections.Counter",
                "syntax": "from collections import Counter",
                "note": "Словарь для подсчёта элементов."
            },
            {
                "name": "collections.OrderedDict",
                "syntax": "from collections import OrderedDict",
                "note": "Словарь с гарантированным порядком ключей в старых версиях Python."
            }
        ],
        "complements": [
            "json",
            "KeyError"
        ],
        "seealso": []
    },
    "plus": {
        "alternatives": [
            {
                "name": "sum()",
                "syntax": "sum([1, 2, 3])",
                "note": "Суммирование элементов."
            },
            {
                "name": "str.join()",
                "syntax": "', '.join(['a', 'b'])",
                "note": "Объединение строк с разделителем."
            }
        ],
        "complements": [
            "TypeError"
        ],
        "seealso": []
    },
    "equals": {
        "alternatives": [
            "is",
            {
                "name": "operator.eq()",
                "syntax": "operator.eq(a, b)",
                "note": "Функциональный вариант сравнения."
            }
        ],
        "complements": [
            "not-equals"
        ],
        "seealso": []
    },
    "in": {
        "alternatives": [
            {
                "name": "str.find()",
                "syntax": "text.find(sub)",
                "note": "Ищет подстроку и возвращает индекс."
            },
            {
                "name": "dict.get()",
                "syntax": "data.get(key)",
                "note": "Безопасное получение значения из словаря."
            }
        ],
        "complements": [
            "list",
            "dict",
            "set"
        ],
        "seealso": []
    },
    "is": {
        "alternatives": [
            "equals",
            {
                "name": "id()",
                "syntax": "id(obj)",
                "note": "Возвращает уникальный идентификатор объекта."
            }
        ],
        "complements": [],
        "seealso": []
    },
    "ValueError": {
        "alternatives": [
            "TypeError"
        ],
        "complements": [
            "int",
            "float"
        ],
        "seealso": []
    },
    "TypeError": {
        "alternatives": [
            "ValueError"
        ],
        "complements": [
            "len",
            "type"
        ],
        "seealso": []
    },
    "os": {
        "alternatives": [
            "pathlib",
            {
                "name": "shutil",
                "syntax": "import shutil",
                "note": "Операции копирования и перемещения файлов."
            }
        ],
        "complements": [
            "sys"
        ],
        "seealso": []
    },
    "sys": {
        "alternatives": [
            "os"
        ],
        "complements": [
            "print"
        ],
        "seealso": []
    },
    "json": {
        "alternatives": [
            {
                "name": "pickle",
                "syntax": "import pickle",
                "note": "Сериализация Python-объектов, не только JSON."
            },
            {
                "name": "yaml",
                "syntax": "import yaml",
                "note": "Формат YAML, требует установки PyYAML."
            }
        ],
        "complements": [
            "dict"
        ],
        "seealso": []
    },
    "pathlib": {
        "alternatives": [
            {
                "name": "os.path",
                "syntax": "import os.path",
                "note": "Старый функциональный способ работы с путями."
            }
        ],
        "complements": [
            "open",
            "os"
        ],
        "seealso": []
    },
    "python": {
        "alternatives": [
            {
                "name": "python3",
                "syntax": "python3",
                "note": "Команда для Python 3 в Linux/macOS."
            },
            {
                "name": "py",
                "syntax": "py",
                "note": "Python Launcher в Windows."
            }
        ],
        "complements": [
            "pip",
            "python-m-venv"
        ],
        "seealso": []
    },
    "pip": {
        "alternatives": [
            {
                "name": "poetry",
                "syntax": "poetry add package",
                "note": "Менеджер зависимостей и сборки проектов."
            },
            {
                "name": "uv",
                "syntax": "uv pip install package",
                "note": "Быстрый менеджер пакетов."
            }
        ],
        "complements": [
            "python",
            "python-m-venv"
        ],
        "seealso": []
    },
    "python-m-venv": {
        "alternatives": [
            {
                "name": "virtualenv",
                "syntax": "pip install virtualenv",
                "note": "Старый популярный инструмент для виртуальных окружений."
            },
            {
                "name": "conda",
                "syntax": "conda create --name env",
                "note": "Окружения в экосистеме Conda."
            }
        ],
        "complements": [
            "pip",
            "pip-install"
        ],
        "seealso": []
    },
    "requests": {
        "alternatives": [
            {
                "name": "urllib.request",
                "syntax": "import urllib.request",
                "note": "Встроенный модуль для HTTP-запросов."
            },
            {
                "name": "httpx",
                "syntax": "pip install httpx",
                "note": "Современная библиотека с поддержкой async."
            }
        ],
        "complements": [
            "json"
        ],
        "seealso": []
    },
    "pandas": {
        "alternatives": [
            {
                "name": "polars",
                "syntax": "pip install polars",
                "note": "Быстрая библиотека для табличных данных."
            },
            {
                "name": "csv",
                "syntax": "import csv",
                "note": "Встроенный модуль для CSV-файлов."
            }
        ],
        "complements": [
            "numpy"
        ],
        "seealso": []
    },
    "django": {
        "alternatives": [
            "flask",
            "fastapi"
        ],
        "complements": [
            "pytest"
        ],
        "seealso": []
    },
    "ipconfig": {
        "alternatives": [
            {
                "name": "ip addr",
                "syntax": "ip addr",
                "note": "Современная команда для Linux."
            },
            {
                "name": "ifconfig",
                "syntax": "ifconfig",
                "note": "Классическая команда в Unix-системах."
            }
        ],
        "complements": [
            "ping",
            "curl"
        ],
        "seealso": []
    }
}


PARAMS_OVERRIDES = {
    "if": [
        {
            "name": "condition",
            "type": "bool",
            "description": "Выражение, которое проверяется на истинность."
        }
    ],
    "for": [
        {
            "name": "item",
            "description": "Переменная для текущего элемента."
        },
        {
            "name": "iterable",
            "description": "Объект, элементы которого перебираются."
        }
    ],
    "def": [
        {
            "name": "name",
            "description": "Имя функции."
        },
        {
            "name": "parameters",
            "description": "Параметры функции."
        }
    ],
    "class": [
        {
            "name": "Name",
            "description": "Имя класса."
        }
    ],
    "import": [
        {
            "name": "module",
            "description": "Имя модуля."
        }
    ],
    "return": [
        {
            "name": "value",
            "description": "Значение, которое возвращает функция."
        }
    ],
    "print": [
        {
            "name": "objects",
            "type": "tuple",
            "description": "Объекты для вывода."
        },
        {
            "name": "sep",
            "type": "str",
            "default": "' '",
            "description": "Разделитель между объектами."
        },
        {
            "name": "end",
            "type": "str",
            "default": "'\\n'",
            "description": "Строка, добавляемая после вывода."
        },
        {
            "name": "file",
            "type": "file",
            "default": "sys.stdout",
            "description": "Куда выводить данные."
        },
        {
            "name": "flush",
            "type": "bool",
            "default": "False",
            "description": "Принудительно сбросить буфер."
        }
    ],
    "len": [
        {
            "name": "obj",
            "description": "Объект, длину которого нужно получить."
        }
    ],
    "open": [
        {
            "name": "file",
            "type": "str | PathLike",
            "description": "Путь к файлу."
        },
        {
            "name": "mode",
            "type": "str",
            "default": "'r'",
            "description": "Режим открытия: чтение, запись, добавление и т.д."
        },
        {
            "name": "encoding",
            "type": "str",
            "default": "None",
            "description": "Кодировка файла."
        }
    ],
    "type": [
        {
            "name": "obj",
            "description": "Объект, тип которого нужно получить."
        }
    ],
    "int": [
        {
            "name": "value",
            "description": "Значение для преобразования в целое число."
        }
    ],
    "str": [
        {
            "name": "object",
            "description": "Объект для преобразования в строку."
        }
    ],
    "list": [
        {
            "name": "iterable",
            "description": "Итерируемый объект для создания списка."
        }
    ],
    "dict": [
        {
            "name": "kwargs",
            "description": "Пары ключ-значение."
        }
    ],
    "plus": [
        {
            "name": "a",
            "description": "Левый операнд."
        },
        {
            "name": "b",
            "description": "Правый операнд."
        }
    ],
    "equals": [
        {
            "name": "a",
            "description": "Левый операнд."
        },
        {
            "name": "b",
            "description": "Правый операнд."
        }
    ],
    "in": [
        {
            "name": "item",
            "description": "Искомый элемент."
        },
        {
            "name": "collection",
            "description": "Коллекция или итерируемый объект."
        }
    ],
    "is": [
        {
            "name": "a",
            "description": "Левый операнд."
        },
        {
            "name": "b",
            "description": "Правый операнд."
        }
    ],
    "ValueError": [
        {
            "name": "message",
            "description": "Текст ошибки."
        }
    ],
    "TypeError": [
        {
            "name": "message",
            "description": "Текст ошибки."
        }
    ],
    "python-m-venv": [
        {
            "name": "path",
            "default": ".venv",
            "description": "Папка виртуального окружения."
        }
    ],
    "ipconfig": [
        {
            "name": "/all",
            "description": "Показать подробную информацию о сети."
        }
    ]
}


RETURNS_OVERRIDES = {
    "if": "Не возвращает значение.",
    "for": "Не возвращает значение.",
    "def": "Создаёт объект функции.",
    "class": "Создаёт объект класса.",
    "import": "Даёт доступ к импортированному модулю.",
    "return": "Передаёт значение обратно вызывающему коду.",
    "print": "None",
    "len": "int",
    "open": "Файловый объект.",
    "type": "Тип объекта.",
    "input": "str",
    "range": "range object",
    "enumerate": "enumerate object",
    "zip": "zip object",
    "sorted": "list",
    "isinstance": "bool",
    "int": "int",
    "str": "str",
    "list": "list",
    "dict": "dict",
    "float": "float",
    "bool": "bool",
    "tuple": "tuple",
    "set": "set",
    "plus": "Результат сложения.",
    "minus": "Результат вычитания.",
    "multiply": "Результат умножения.",
    "divide": "float",
    "equals": "bool",
    "not-equals": "bool",
    "in": "bool",
    "is": "bool",
    "and": "Зависит от операндов.",
    "or": "Зависит от операндов.",
    "ValueError": "Объект исключения.",
    "TypeError": "Объект исключения.",
    "KeyError": "Объект исключения.",
    "IndexError": "Объект исключения.",
    "FileNotFoundError": "Объект исключения.",
    "AttributeError": "Объект исключения.",
    "ZeroDivisionError": "Объект исключения.",
    "os": "Модуль os.",
    "sys": "Модуль sys.",
    "json": "Модуль json.",
    "pathlib": "Модуль pathlib.",
    "math": "Модуль math.",
    "random": "Модуль random.",
    "datetime": "Модуль datetime.",
    "re": "Модуль re.",
    "collections": "Модуль collections.",
    "itertools": "Модуль itertools.",
    "python": "Интерактивный интерпретатор или код завершения.",
    "python-script": "Код завершения процесса.",
    "python-version": "Текст версии Python.",
    "pip": "Результат выполнения команды.",
    "pip-install": "Установленный пакет.",
    "pip-list": "Список установленных пакетов.",
    "python-m-venv": "Созданное виртуальное окружение.",
    "python-m-http-server": "Запущенный HTTP-сервер.",
    "requests": "Зависит от используемого метода.",
    "pandas": "Зависит от используемого метода.",
    "django": "Зависит от команды.",
    "numpy": "Зависит от используемого метода.",
    "flask": "Зависит от используемого кода.",
    "fastapi": "Зависит от используемого кода.",
    "pytest": "Результаты тестов.",
    "black": "Отформатированные файлы.",
    "ipconfig": "Текстовую информацию о сетевых адаптерах.",
    "ping": "Статистику доступности узла.",
    "cd": "Ничего, но меняет текущую папку.",
    "dir": "Список файлов и папок.",
    "ls": "Список файлов и папок.",
    "mkdir": "Созданную папку.",
    "rm": "Удалённые файлы.",
    "copy": "Скопированные файлы.",
    "move": "Перемещённые файлы.",
    "echo": "Текст в консоли.",
    "cls": "Очищает консоль.",
    "clear": "Очищает терминал.",
    "curl": "Загруженные данные."
}


ERRORS_OVERRIDES = {
    "print": [
        {
            "type": "TypeError",
            "when": "Если переданы аргументы недопустимого типа."
        }
    ],
    "len": [
        {
            "type": "TypeError",
            "when": "Если объект не поддерживает len()."
        }
    ],
    "open": [
        {
            "type": "FileNotFoundError",
            "when": "Если файл не найден."
        },
        {
            "type": "PermissionError",
            "when": "Если нет прав доступа."
        },
        {
            "type": "TypeError",
            "when": "Если переданы аргументы недопустимого типа."
        }
    ],
    "int": [
        {
            "type": "ValueError",
            "when": "Если строка не может быть преобразована в число."
        },
        {
            "type": "TypeError",
            "when": "Если передан объект недопустимого типа."
        }
    ],
    "str": [
        {
            "type": "TypeError",
            "when": "Если объект не может быть преобразован в строку."
        }
    ],
    "list": [
        {
            "type": "TypeError",
            "when": "Если переданный объект не является итерируемым."
        }
    ],
    "dict": [
        {
            "type": "TypeError",
            "when": "Если переданы аргументы недопустимого типа."
        }
    ],
    "plus": [
        {
            "type": "TypeError",
            "when": "Если типы операндов не поддерживают сложение."
        }
    ],
    "in": [
        {
            "type": "TypeError",
            "when": "Если объект не поддерживает проверку вхождения."
        }
    ],
    "import": [
        {
            "type": "ModuleNotFoundError",
            "when": "Если модуль не найден."
        }
    ]
}


VERSION_OVERRIDES = {
    "print": {
        "since": "3.0"
    },
    "pathlib": {
        "since": "3.4"
    },
    "python-m-venv": {
        "since": "3.3"
    }
}


CHECKED_CATEGORIES = {
    "core",
    "builtin",
    "types",
    "operators",
    "exceptions",
    "stdlib"
}


DEFAULT_RETURNS = {
    "keyword": "Не возвращает значение.",
    "builtin-function": "Зависит от функции.",
    "builtin-type": "Возвращает объект типа.",
    "operator": "Зависит от операции.",
    "exception": "Объект исключения.",
    "module": "Модуль.",
    "cli": "Код завершения.",
    "library": "Зависит от библиотеки.",
    "os-command": "Текстовый вывод или код завершения."
}


def make_version(entry_id, category):
    version = {
        "since": None,
        "deprecated": None,
        "removed": None,
        "checked": None
    }

    if category in CHECKED_CATEGORIES:
        version["checked"] = "3.13"

    override = VERSION_OVERRIDES.get(entry_id, {})
    version.update(override)

    return version


def make_related(entry_id):
    related = RELATED.get(entry_id, {})

    return {
        "alternatives": related.get("alternatives", []),
        "complements": related.get("complements", []),
        "seealso": related.get("seealso", [])
    }


def build_entries():
    entries = []

    for item in RAW:
        entry_id, name, entry_type, category, summary, syntax, example, tags = item

        entries.append({
            "id": entry_id,
            "name": name,
            "type": entry_type,
            "category": category,
            "summary": summary,
            "syntax": syntax,
            "params": PARAMS_OVERRIDES.get(entry_id, []),
            "returns": RETURNS_OVERRIDES.get(entry_id, DEFAULT_RETURNS.get(entry_type, "")),
            "errors": ERRORS_OVERRIDES.get(entry_id, []),
            "example": example,
            "version": make_version(entry_id, category),
            "tags": tags,
            "links": [],
            "related": make_related(entry_id)
        })

    return entries


def main():
    payload = {
        "meta": {
            "pythonVersions": PYTHON_VERSIONS,
            "news": []
        },
        "entries": build_entries()
    }

    out_path = Path(__file__).resolve().parent.parent / "data" / "entries.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Saved {len(payload['entries'])} entries to {out_path}")


if __name__ == "__main__":
    main()