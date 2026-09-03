#!/usr/bin/env python3
import json
from pathlib import Path


INPUT_PATHS = [
    Path("data/entries.json"),
    Path("entries.json"),
]

OUTPUT_PATH = Path("data/entries.json")


CHECKED_CATEGORIES = {
    "core",
    "builtin",
    "types",
    "operators",
    "exceptions",
    "stdlib",
}


CATEGORY_DEFAULT_RANK = {
    "core": 1500,
    "builtin": 2000,
    "types": 3000,
    "operators": 4000,
    "exceptions": 5000,
    "stdlib": 6000,
    "python-cli": 7000,
    "dev-tools": 7500,
    "packages": 8000,
    "os": 9000,
}


POPULARITY = {
    # Самые популярные
    "print": 10,
    "len": 20,
    "if": 30,
    "for": 40,
    "def": 50,
    "import": 60,
    "open": 70,
    "list": 80,
    "dict": 90,
    "str": 100,
    "int": 110,

    # Очень популярные конструкции
    "while": 115,
    "try": 120,
    "with": 125,
    "except": 126,
    "finally": 127,
    "input": 130,
    "break": 135,
    "continue": 136,
    "pass": 137,
    "raise": 138,
    "yield": 139,
    "range": 140,
    "from": 141,
    "as": 142,
    "not": 145,
    "enumerate": 150,
    "lambda": 155,
    "zip": 160,
    "async": 165,
    "await": 166,
    "sorted": 170,
    "asyncio": 180,
    "isinstance": 190,

    # Популярные встроенные функции
    "abs": 200,
    "min": 210,
    "max": 220,
    "sum": 230,
    "round": 240,
    "any": 250,
    "all": 260,
    "map": 270,
    "filter": 280,
    "reversed": 290,
    "format": 300,
    "repr": 310,
    "callable": 320,
    "iter": 330,
    "next": 340,
    "else": 350,
    "elif": 351,
    "dir": 360,
    "vars": 370,
    "super": 380,
    "property": 390,
    "classmethod": 400,
    "staticmethod": 410,

    # Python CLI
    "python": 540,
    "match": 520,
    "case": 521,
    "True": 560,
    "False": 570,
    "None": 580,
    "pip-install": 590,
    "pip": 600,
    "python-m-venv": 610,
    "time": 620,
    "subprocess": 630,
    "shutil": 640,
    "logging": 650,
    "argparse": 660,
    "typing": 670,
    "dataclasses": 680,
    "python-m-pip": 690,
    "pip-freeze": 720,
    "pip-show": 730,
    "python-m-http-server": 750,

    # Библиотеки
    "requests": 800,
    "pandas": 810,
    "django": 820,
    "numpy": 830,
    "flask": 840,
    "fastapi": 850,
    "pytest": 860,
    "black": 870,

    # Инструменты разработки и сети
    "git": 900,
    "curl": 910,
    "wget": 920,
    "ipconfig": 930,
    "ping": 940,
}


RELATED_EXTRA = {
    "print": {
        "alternatives": [
            {
                "name": "sys.stdout.write()",
                "syntax": "sys.stdout.write(text)",
                "note": "Пишет текст напрямую в stdout без автоматического перевода строки."
            },
            {
                "name": "logging",
                "syntax": "import logging; logging.info('message')",
                "note": "Лучше подходит для логов и уровней важности."
            },
            {
                "name": "pprint",
                "syntax": "from pprint import pprint; pprint(data)",
                "note": "Удобный вывод сложных структур данных."
            }
        ],
        "complements": ["sys", "open"],
        "seealso": ["input"]
    },
    "while": {
        "alternatives": [
            "for",
            {
                "name": "Рекурсия",
                "syntax": "def func(): func()",
                "note": "Иногда заменяет цикл, но обычно дороже по памяти."
            }
        ],
        "complements": ["break", "continue", "if"],
        "seealso": ["for"]
    },
    "try": {
        "alternatives": [
            {
                "name": "Проверка условий заранее",
                "syntax": "if value is not None:",
                "note": "Иногда проще проверить данные до операции."
            },
            "with"
        ],
        "complements": ["except", "finally", "raise"],
        "seealso": ["ValueError", "TypeError", "FileNotFoundError"]
    },
    "with": {
        "alternatives": [
            {
                "name": "try/finally",
                "syntax": "try:\n    ...\nfinally:\n    ...",
                "note": "Ручное освобождение ресурсов."
            },
            {
                "name": "contextlib",
                "syntax": "import contextlib",
                "note": "Создание собственных контекстных менеджеров."
            }
        ],
        "complements": ["open", "try"],
        "seealso": ["FileNotFoundError"]
    },
    "lambda": {
        "alternatives": [
            "def",
            {
                "name": "operator",
                "syntax": "import operator",
                "note": "Готовые функции для часто используемых операций."
            }
        ],
        "complements": ["map", "filter", "sorted"],
        "seealso": ["def"]
    },
    "async": {
        "alternatives": [
            "threading",
            "multiprocessing",
            "asyncio"
        ],
        "complements": ["await", "asyncio"],
        "seealso": ["with", "def"]
    },
    "await": {
        "alternatives": [],
        "complements": ["async", "asyncio"],
        "seealso": []
    },
    "match": {
        "alternatives": [
            "if",
            "elif",
            {
                "name": "Словарная диспетчеризация",
                "syntax": "handlers = {'start': start_func, 'stop': stop_func}",
                "note": "Иногда заменяет match/case через словарь функций."
            }
        ],
        "complements": ["case"],
        "seealso": ["if", "elif"]
    },
    "case": {
        "alternatives": [],
        "complements": ["match"],
        "seealso": ["if", "elif"]
    },
    "pip-freeze": {
        "alternatives": [
            "pip-list",
            "pip-show"
        ],
        "complements": [
            "pip-install",
            "python-m-venv"
        ],
        "seealso": ["pip"]
    },
    "pip-show": {
        "alternatives": [
            "pip-list",
            "pip-freeze"
        ],
        "complements": ["pip"],
        "seealso": ["pip-install"]
    },
    "python-m-pip": {
        "alternatives": [
            "pip"
        ],
        "complements": [
            "pip-install",
            "pip-list",
            "pip-freeze",
            "pip-show"
        ],
        "seealso": ["python"]
    },
    "git": {
        "alternatives": [
            {
                "name": "Mercurial",
                "syntax": "hg",
                "note": "Другая распределённая система контроля версий."
            },
            {
                "name": "Subversion",
                "syntax": "svn",
                "note": "Централизованная система контроля версий."
            }
        ],
        "complements": [],
        "seealso": ["curl", "wget"]
    },
    "curl": {
        "alternatives": [
            "wget",
            "requests",
            {
                "name": "urllib.request",
                "syntax": "import urllib.request",
                "note": "Встроенный Python-модуль для HTTP-запросов."
            }
        ],
        "complements": ["ping", "requests"],
        "seealso": ["wget"]
    },
    "wget": {
        "alternatives": [
            "curl",
            "requests"
        ],
        "complements": ["curl"],
        "seealso": ["requests"]
    }
}


PARAMS_EXTRA = {
    "input": [
        {
            "name": "prompt",
            "type": "str",
            "default": "''",
            "description": "Текст приглашения перед вводом."
        }
    ],
    "range": [
        {
            "name": "start",
            "type": "int",
            "default": "0",
            "description": "Начальное значение."
        },
        {
            "name": "stop",
            "type": "int",
            "description": "Конечное значение, не включая его."
        },
        {
            "name": "step",
            "type": "int",
            "default": "1",
            "description": "Шаг."
        }
    ],
    "enumerate": [
        {
            "name": "iterable",
            "description": "Итерируемый объект."
        },
        {
            "name": "start",
            "type": "int",
            "default": "0",
            "description": "Начальный индекс."
        }
    ],
    "zip": [
        {
            "name": "iterables",
            "description": "Одна или несколько последовательностей."
        }
    ],
    "sorted": [
        {
            "name": "iterable",
            "description": "Объект для сортировки."
        },
        {
            "name": "key",
            "default": "None",
            "description": "Функция для извлечения ключа сортировки."
        },
        {
            "name": "reverse",
            "type": "bool",
            "default": "False",
            "description": "Сортировать по убыванию."
        }
    ],
    "isinstance": [
        {
            "name": "obj",
            "description": "Проверяемый объект."
        },
        {
            "name": "classinfo",
            "description": "Тип или кортеж типов."
        }
    ],
    "float": [
        {
            "name": "value",
            "description": "Значение для преобразования в float."
        }
    ],
    "bool": [
        {
            "name": "value",
            "description": "Значение для преобразования в bool."
        }
    ],
    "tuple": [
        {
            "name": "iterable",
            "description": "Итерируемый объект для создания кортежа."
        }
    ],
    "set": [
        {
            "name": "iterable",
            "description": "Итерируемый объект для создания множества."
        }
    ],
    "abs": [
        {
            "name": "x",
            "description": "Число."
        }
    ],
    "round": [
        {
            "name": "number",
            "description": "Число для округления."
        },
        {
            "name": "ndigits",
            "default": "None",
            "description": "Количество знаков после запятой."
        }
    ],
    "min": [
        {
            "name": "iterable",
            "description": "Итерируемый объект или несколько аргументов."
        }
    ],
    "max": [
        {
            "name": "iterable",
            "description": "Итерируемый объект или несколько аргументов."
        }
    ],
    "sum": [
        {
            "name": "iterable",
            "description": "Числовая последовательность."
        },
        {
            "name": "start",
            "default": "0",
            "description": "Начальное значение."
        }
    ],
    "any": [
        {
            "name": "iterable",
            "description": "Итерируемый объект."
        }
    ],
    "all": [
        {
            "name": "iterable",
            "description": "Итерируемый объект."
        }
    ],
    "map": [
        {
            "name": "function",
            "description": "Функция для применения."
        },
        {
            "name": "iterables",
            "description": "Один или несколько итерируемых объектов."
        }
    ],
    "filter": [
        {
            "name": "function",
            "description": "Функция-фильтр."
        },
        {
            "name": "iterable",
            "description": "Итерируемый объект."
        }
    ],
    "reversed": [
        {
            "name": "seq",
            "description": "Последовательность."
        }
    ],
    "format": [
        {
            "name": "value",
            "description": "Значение для форматирования."
        },
        {
            "name": "format_spec",
            "default": "''",
            "description": "Спецификация формата."
        }
    ],
    "repr": [
        {
            "name": "obj",
            "description": "Объект для представления."
        }
    ],
    "callable": [
        {
            "name": "obj",
            "description": "Объект для проверки."
        }
    ],
    "iter": [
        {
            "name": "obj",
            "description": "Объект для получения итератора."
        }
    ],
    "next": [
        {
            "name": "iterator",
            "description": "Итератор."
        },
        {
            "name": "default",
            "description": "Значение по умолчанию при StopIteration."
        }
    ],
    "dir": [
        {
            "name": "obj",
            "description": "Объект для просмотра атрибутов."
        }
    ],
    "vars": [
        {
            "name": "obj",
            "description": "Объект с __dict__."
        }
    ],
    "while": [
        {
            "name": "condition",
            "type": "bool",
            "description": "Условие выполнения цикла."
        }
    ],
    "try": [
        {
            "name": "block",
            "description": "Код, который может вызвать исключение."
        }
    ],
    "with": [
        {
            "name": "context_manager",
            "description": "Контекстный менеджер."
        },
        {
            "name": "as",
            "description": "Необязательная переменная для ресурса."
        }
    ],
    "lambda": [
        {
            "name": "parameters",
            "description": "Аргументы лямбда-функции."
        },
        {
            "name": "expression",
            "description": "Выражение, которое возвращает лямбда."
        }
    ],
    "async": [
        {
            "name": "function",
            "description": "Имя асинхронной функции."
        }
    ],
    "await": [
        {
            "name": "awaitable",
            "description": "Объект, который можно ожидать."
        }
    ],
    "match": [
        {
            "name": "subject",
            "description": "Значение для сопоставления."
        }
    ],
    "case": [
        {
            "name": "pattern",
            "description": "Шаблон для сопоставления."
        }
    ]
}


RETURNS_EXTRA = {
    "input": "str",
    "range": "range object",
    "enumerate": "enumerate object",
    "zip": "zip object",
    "sorted": "list",
    "isinstance": "bool",
    "float": "float",
    "bool": "bool",
    "tuple": "tuple",
    "set": "set",
    "abs": "Число (модуль значения).",
    "round": "Округлённое число.",
    "min": "Минимальный элемент.",
    "max": "Максимальный элемент.",
    "sum": "Сумму элементов.",
    "any": "bool",
    "all": "bool",
    "map": "map object",
    "filter": "filter object",
    "reversed": "reversed iterator",
    "format": "str",
    "repr": "str",
    "callable": "bool",
    "iter": "Итератор.",
    "next": "Следующий элемент итератора.",
    "dir": "list",
    "vars": "dict"
}


ERRORS_EXTRA = {
    "input": [
        {
            "type": "EOFError",
            "when": "Если ввод недоступен."
        },
        {
            "type": "KeyboardInterrupt",
            "when": "Если пользователь прервал ввод."
        }
    ],
    "range": [
        {
            "type": "TypeError",
            "when": "Если аргументы не являются целыми числами."
        }
    ],
    "enumerate": [
        {
            "type": "TypeError",
            "when": "Если объект не является итерируемым."
        }
    ],
    "zip": [
        {
            "type": "TypeError",
            "when": "Если переданы не итерируемые объекты."
        }
    ],
    "sorted": [
        {
            "type": "TypeError",
            "when": "Если элементы нельзя сравнить."
        }
    ],
    "isinstance": [
        {
            "type": "TypeError",
            "when": "Если classinfo не является типом или кортежем типов."
        }
    ],
    "float": [
        {
            "type": "ValueError",
            "when": "Если строка не может быть преобразована в float."
        },
        {
            "type": "TypeError",
            "when": "Если передан объект недопустимого типа."
        }
    ],
    "bool": [
        {
            "type": "TypeError",
            "when": "Если объект не может быть преобразован в bool."
        }
    ],
    "tuple": [
        {
            "type": "TypeError",
            "when": "Если объект не является итерируемым."
        }
    ],
    "set": [
        {
            "type": "TypeError",
            "when": "Если объект не является итерируемым."
        }
    ],
    "abs": [
        {
            "type": "TypeError",
            "when": "Если объект не поддерживает abs()."
        }
    ],
    "round": [
        {
            "type": "TypeError",
            "when": "Если объект не поддерживает округление."
        }
    ],
    "min": [
        {
            "type": "ValueError",
            "when": "Если передана пустая последовательность."
        }
    ],
    "max": [
        {
            "type": "ValueError",
            "when": "Если передана пустая последовательность."
        }
    ],
    "sum": [
        {
            "type": "TypeError",
            "when": "Если элементы не поддерживают сложение."
        }
    ],
    "next": [
        {
            "type": "StopIteration",
            "when": "Если элементов больше нет и нет default."
        }
    ],
    "iter": [
        {
            "type": "TypeError",
            "when": "Если объект не поддерживает итерацию."
        }
    ],
    "divide": [
        {
            "type": "ZeroDivisionError",
            "when": "Если делить на ноль."
        },
        {
            "type": "TypeError",
            "when": "Если типы не поддерживают деление."
        }
    ]
}


NEW_ENTRIES = [
    {
        "id": "while",
        "name": "while",
        "type": "keyword",
        "category": "core",
        "summary": "Цикл, который выполняется, пока условие истинно.",
        "syntax": "while condition:",
        "params": PARAMS_EXTRA["while"],
        "returns": "Не возвращает значение.",
        "errors": [],
        "example": "while x > 0:\n    x -= 1",
        "version": {
            "since": None,
            "deprecated": None,
            "removed": None,
            "checked": "3.13"
        },
        "tags": ["цикл", "while"],
        "links": [
            "https://docs.python.org/3/reference/compound_stmts.html#while"
        ],
        "related": RELATED_EXTRA["while"]
    },
    {
        "id": "try",
        "name": "try",
        "type": "keyword",
        "category": "core",
        "summary": "Обрабатывает исключения и ошибки во время выполнения.",
        "syntax": "try:\n    ...\nexcept Exception as e:\n    ...\nelse:\n    ...\nfinally:\n    ...",
        "params": PARAMS_EXTRA["try"],
        "returns": "Не возвращает значение.",
        "errors": [],
        "example": "try:\n    x = int('a')\nexcept ValueError:\n    print('ValueError')",
        "version": {
            "since": None,
            "deprecated": None,
            "removed": None,
            "checked": "3.13"
        },
        "tags": ["исключения", "try", "ошибки"],
        "links": [
            "https://docs.python.org/3/reference/compound_stmts.html#try"
        ],
        "related": RELATED_EXTRA["try"]
    },
    {
        "id": "with",
        "name": "with",
        "type": "keyword",
        "category": "core",
        "summary": "Контекстный менеджер для безопасного открытия и закрытия ресурсов.",
        "syntax": "with context_manager as variable:",
        "params": PARAMS_EXTRA["with"],
        "returns": "Не возвращает значение.",
        "errors": [],
        "example": "with open('file.txt', encoding='utf-8') as f:\n    text = f.read()",
        "version": {
            "since": "3.0",
            "deprecated": None,
            "removed": None,
            "checked": "3.13"
        },
        "tags": ["with", "контекстный менеджер"],
        "links": [
            "https://docs.python.org/3/reference/compound_stmts.html#with"
        ],
        "related": RELATED_EXTRA["with"]
    },
    {
        "id": "lambda",
        "name": "lambda",
        "type": "keyword",
        "category": "core",
        "summary": "Короткая анонимная функция.",
        "syntax": "lambda parameters: expression",
        "params": PARAMS_EXTRA["lambda"],
        "returns": "Объект функции.",
        "errors": [],
        "example": "square = lambda x: x * x",
        "version": {
            "since": None,
            "deprecated": None,
            "removed": None,
            "checked": "3.13"
        },
        "tags": ["lambda", "функция"],
        "links": [
            "https://docs.python.org/3/reference/expressions.html#lambda"
        ],
        "related": RELATED_EXTRA["lambda"]
    },
    {
        "id": "async",
        "name": "async",
        "type": "keyword",
        "category": "core",
        "summary": "Объявляет асинхронную функцию.",
        "syntax": "async def name():",
        "params": PARAMS_EXTRA["async"],
        "returns": "Создаёт coroutine-функцию.",
        "errors": [],
        "example": "import asyncio\n\nasync def main():\n    await asyncio.sleep(1)\n\nasyncio.run(main())",
        "version": {
            "since": "3.5",
            "deprecated": None,
            "removed": None,
            "checked": "3.13"
        },
        "tags": ["async", "асинхронность"],
        "links": [
            "https://docs.python.org/3/reference/compound_stmts.html#async-def"
        ],
        "related": RELATED_EXTRA["async"]
    },
    {
        "id": "await",
        "name": "await",
        "type": "keyword",
        "category": "core",
        "summary": "Ожидает результат асинхронной операции.",
        "syntax": "await awaitable",
        "params": PARAMS_EXTRA["await"],
        "returns": "Результат awaitable-объекта.",
        "errors": [
            {
                "type": "SyntaxError",
                "when": "Если await используется вне async def."
            }
        ],
        "example": "await asyncio.sleep(1)",
        "version": {
            "since": "3.5",
            "deprecated": None,
            "removed": None,
            "checked": "3.13"
        },
        "tags": ["await", "асинхронность"],
        "links": [
            "https://docs.python.org/3/reference/expressions.html#await"
        ],
        "related": RELATED_EXTRA["await"]
    },
    {
        "id": "match",
        "name": "match",
        "type": "keyword",
        "category": "core",
        "summary": "Сопоставление значения с шаблонами.",
        "syntax": "match subject:\n    case pattern:\n        ...",
        "params": PARAMS_EXTRA["match"],
        "returns": "Не возвращает значение.",
        "errors": [],
        "example": "match command:\n    case 'quit':\n        print('exit')\n    case _:\n        print('unknown')",
        "version": {
            "since": "3.10",
            "deprecated": None,
            "removed": None,
            "checked": "3.13"
        },
        "tags": ["match", "pattern matching"],
        "links": [
            "https://docs.python.org/3/reference/compound_stmts.html#match"
        ],
        "related": RELATED_EXTRA["match"]
    },
    {
        "id": "case",
        "name": "case",
        "type": "keyword",
        "category": "core",
        "summary": "Ветка сопоставления внутри match.",
        "syntax": "case pattern:",
        "params": PARAMS_EXTRA["case"],
        "returns": "Не возвращает значение.",
        "errors": [],
        "example": "match x:\n    case 1:\n        print('one')",
        "version": {
            "since": "3.10",
            "deprecated": None,
            "removed": None,
            "checked": "3.13"
        },
        "tags": ["case", "pattern matching"],
        "links": [
            "https://docs.python.org/3/reference/compound_stmts.html#match"
        ],
        "related": RELATED_EXTRA["case"]
    },
    {
        "id": "pip-freeze",
        "name": "pip freeze",
        "type": "cli",
        "category": "python-cli",
        "summary": "Показывает установленные пакеты в формате requirements.txt.",
        "syntax": "pip freeze",
        "params": [],
        "returns": "Список пакетов с версиями.",
        "errors": [],
        "example": "pip freeze > requirements.txt",
        "version": {
            "since": None,
            "deprecated": None,
            "removed": None,
            "checked": None
        },
        "tags": ["pip", "freeze", "requirements"],
        "links": [
            "https://pip.pypa.io/en/stable/cli/pip_freeze/"
        ],
        "related": RELATED_EXTRA["pip-freeze"]
    },
    {
        "id": "pip-show",
        "name": "pip show",
        "type": "cli",
        "category": "python-cli",
        "summary": "Показывает информацию об установленном пакете.",
        "syntax": "pip show package",
        "params": [
            {
                "name": "package",
                "description": "Имя пакета."
            }
        ],
        "returns": "Информацию о пакете.",
        "errors": [],
        "example": "pip show requests",
        "version": {
            "since": None,
            "deprecated": None,
            "removed": None,
            "checked": None
        },
        "tags": ["pip", "show"],
        "links": [
            "https://pip.pypa.io/en/stable/cli/pip_show/"
        ],
        "related": RELATED_EXTRA["pip-show"]
    },
    {
        "id": "python-m-pip",
        "name": "python -m pip",
        "type": "cli",
        "category": "python-cli",
        "summary": "Запуск pip через конкретный интерпретатор Python.",
        "syntax": "python -m pip command",
        "params": [
            {
                "name": "command",
                "description": "Команда pip."
            }
        ],
        "returns": "Результат выполнения pip.",
        "errors": [],
        "example": "python -m pip install requests",
        "version": {
            "since": None,
            "deprecated": None,
            "removed": None,
            "checked": None
        },
        "tags": ["python", "pip"],
        "links": [
            "https://pip.pypa.io/"
        ],
        "related": RELATED_EXTRA["python-m-pip"]
    },
    {
        "id": "git",
        "name": "git",
        "type": "cli",
        "category": "dev-tools",
        "summary": "Система контроля версий.",
        "syntax": "git command",
        "params": [
            {
                "name": "command",
                "description": "Команда git: init, clone, add, commit, push, pull."
            }
        ],
        "returns": "Зависит от команды.",
        "errors": [],
        "example": "git --help",
        "version": {
            "since": None,
            "deprecated": None,
            "removed": None,
            "checked": None
        },
        "tags": ["git", "vcs"],
        "links": [
            "https://git-scm.com/"
        ],
        "related": RELATED_EXTRA["git"]
    },
    {
        "id": "wget",
        "name": "wget",
        "type": "cli",
        "category": "dev-tools",
        "summary": "Загружает файлы по сети из командной строки.",
        "syntax": "wget url",
        "params": [
            {
                "name": "url",
                "description": "Адрес файла или ресурса."
            }
        ],
        "returns": "Загруженный файл.",
        "errors": [],
        "example": "wget https://example.com",
        "version": {
            "since": None,
            "deprecated": None,
            "removed": None,
            "checked": None
        },
        "tags": ["wget", "сеть"],
        "links": [
            "https://www.gnu.org/software/wget/"
        ],
        "related": RELATED_EXTRA["wget"]
    },
    {
        "id": "curl",
        "name": "curl",
        "type": "os-command",
        "category": "dev-tools",
        "summary": "Загружает данные по URL из командной строки.",
        "syntax": "curl url",
        "params": [
            {
                "name": "url",
                "description": "Адрес запроса."
            },
            {
                "name": "-o file",
                "description": "Сохранить результат в файл."
            },
            {
                "name": "-I",
                "description": "Показать только заголовки."
            }
        ],
        "returns": "Загруженные данные или заголовки.",
        "errors": [],
        "example": "curl https://example.com",
        "version": {
            "since": None,
            "deprecated": None,
            "removed": None,
            "checked": None
        },
        "tags": ["curl", "сеть", "http"],
        "links": [
            "https://curl.se/"
        ],
        "related": RELATED_EXTRA["curl"]
    }
]


EXTRA_SIMPLE = [
    ("except", "except", "keyword", "core", "Обрабатывает исключения.", "except Exception as e:", "try:\n    pass\nexcept Exception as e:\n    print(e)", ["исключения", "except"]),
    ("finally", "finally", "keyword", "core", "Блок, который выполняется всегда после try/except.", "finally:", "try:\n    pass\nfinally:\n    print('done')", ["исключения", "finally"]),
    ("else", "else", "keyword", "core", "Ветка иначе для if, for, while, try.", "else:", "if x > 0:\n    print('positive')\nelse:\n    print('non-positive')", ["условие", "else"]),
    ("elif", "elif", "keyword", "core", "Дополнительное условие после if.", "elif condition:", "if x > 0:\n    print('positive')\nelif x == 0:\n    print('zero')", ["условие", "elif"]),
    ("break", "break", "keyword", "core", "Прерывает цикл.", "break", "for i in range(5):\n    if i == 2:\n        break", ["цикл", "break"]),
    ("continue", "continue", "keyword", "core", "Пропускает текущую итерацию цикла.", "continue", "for i in range(5):\n    if i == 2:\n        continue", ["цикл", "continue"]),
    ("pass", "pass", "keyword", "core", "Ничего не делает. Используется как заглушка.", "pass", "def todo():\n    pass", ["заглушка", "pass"]),
    ("raise", "raise", "keyword", "core", "Вызывает исключение.", "raise Exception('message')", "raise ValueError('bad')", ["исключения", "raise"]),
    ("yield", "yield", "keyword", "core", "Возвращает значение из генератора.", "yield value", "def counter():\n    yield 1", ["генератор", "yield"]),
    ("from", "from", "keyword", "core", "Импортирует объекты из модуля.", "from module import name", "from os import getcwd", ["импорт", "from"]),
    ("as", "as", "keyword", "core", "Даёт импортированному объекту или контексту псевдоним.", "import module as alias", "import os as operating_system", ["импорт", "as"]),
    ("global", "global", "keyword", "core", "Объявляет переменную глобальной.", "global name", "global x", ["область видимости", "global"]),
    ("nonlocal", "nonlocal", "keyword", "core", "Объявляет переменную из внешней функции.", "nonlocal name", "def outer():\n    x = 1\n    def inner():\n        nonlocal x", ["область видимости", "nonlocal"]),
    ("assert", "assert", "keyword", "core", "Проверяет условие и вызывает AssertionError, если оно ложно.", "assert condition", "assert x > 0", ["проверка", "assert"]),
    ("del", "del", "keyword", "core", "Удаляет объект или имя.", "del name", "del items[0]", ["удаление", "del"]),
    ("not", "not", "keyword", "core", "Логическое отрицание.", "not x", "not flag", ["логика", "not"]),
    ("True", "True", "keyword", "core", "Логическая константа истины.", "True", "flag = True", ["bool", "True"]),
    ("False", "False", "keyword", "core", "Логическая константа лжи.", "False", "flag = False", ["bool", "False"]),
    ("None", "None", "keyword", "core", "Константа отсутствия значения.", "None", "value = None", ["None"]),

    ("abs", "abs()", "builtin-function", "builtin", "Возвращает модуль числа.", "abs(x)", "abs(-5)", ["числа", "abs"]),
    ("round", "round()", "builtin-function", "builtin", "Округляет число.", "round(number, ndigits=None)", "round(3.1415, 2)", ["числа", "round"]),
    ("min", "min()", "builtin-function", "builtin", "Возвращает минимальный элемент.", "min(iterable)", "min([3, 1, 2])", ["min"]),
    ("max", "max()", "builtin-function", "builtin", "Возвращает максимальный элемент.", "max(iterable)", "max([3, 1, 2])", ["max"]),
    ("sum", "sum()", "builtin-function", "builtin", "Суммирует элементы.", "sum(iterable, start=0)", "sum([1, 2, 3])", ["sum"]),
    ("any", "any()", "builtin-function", "builtin", "Возвращает True, если хотя бы один элемент истинен.", "any(iterable)", "any([False, True])", ["any"]),
    ("all", "all()", "builtin-function", "builtin", "Возвращает True, если все элементы истинны.", "all(iterable)", "all([True, True])", ["all"]),
    ("map", "map()", "builtin-function", "builtin", "Применяет функцию к элементам.", "map(function, iterable)", "list(map(str, [1, 2]))", ["map"]),
    ("filter", "filter()", "builtin-function", "builtin", "Отфильтровывает элементы по функции.", "filter(function, iterable)", "list(filter(bool, [0, 1]))", ["filter"]),
    ("reversed", "reversed()", "builtin-function", "builtin", "Возвращает обратный итератор.", "reversed(seq)", "list(reversed([1, 2]))", ["reversed"]),
    ("format", "format()", "builtin-function", "builtin", "Форматирует значение.", "format(value, format_spec)", "format(3.1415, '.2f')", ["format"]),
    ("repr", "repr()", "builtin-function", "builtin", "Возвращает строковое представление объекта для отладки.", "repr(obj)", "repr('a')", ["repr"]),
    ("callable", "callable()", "builtin-function", "builtin", "Проверяет, можно ли вызвать объект.", "callable(obj)", "callable(print)", ["callable"]),
    ("iter", "iter()", "builtin-function", "builtin", "Возвращает итератор.", "iter(obj)", "iter([1, 2])", ["iter"]),
    ("next", "next()", "builtin-function", "builtin", "Возвращает следующий элемент итератора.", "next(iterator, default=None)", "next(iter([1]))", ["next"]),
    ("dir", "dir()", "builtin-function", "builtin", "Показывает имена в объекте или области видимости.", "dir(obj)", "dir(str)", ["dir"]),
    ("vars", "vars()", "builtin-function", "builtin", "Возвращает словарь атрибутов объекта.", "vars(obj)", "vars()", ["vars"]),
    ("super", "super()", "builtin-function", "builtin", "Даёт доступ к родительскому классу.", "super()", "super().__init__()", ["super", "ООП"]),
    ("property", "property()", "builtin-function", "builtin", "Создаёт управляемый атрибут класса.", "property(fget=None)", "property(get_name)", ["property", "ООП"]),
    ("classmethod", "classmethod()", "builtin-function", "builtin", "Создаёт метод класса.", "classmethod(func)", "classmethod(cls)", ["classmethod", "ООП"]),
    ("staticmethod", "staticmethod()", "builtin-function", "builtin", "Создаёт статический метод.", "staticmethod(func)", "staticmethod(func)", ["staticmethod", "ООП"]),

    ("time", "time", "module", "stdlib", "Работа со временем.", "import time", "import time; time.sleep(1)", ["время", "time"]),
    ("subprocess", "subprocess", "module", "stdlib", "Запуск внешних процессов.", "import subprocess", "import subprocess; subprocess.run(['python', '--version'])", ["процессы", "subprocess"]),
    ("shutil", "shutil", "module", "stdlib", "Операции с файлами и папками высокого уровня.", "import shutil", "import shutil; shutil.copy('a.txt', 'b.txt')", ["файлы", "shutil"]),
    ("logging", "logging", "module", "stdlib", "Логирование.", "import logging", "import logging; logging.info('hello')", ["логи", "logging"]),
    ("argparse", "argparse", "module", "stdlib", "Разбор аргументов командной строки.", "import argparse", "import argparse; parser = argparse.ArgumentParser()", ["cli", "argparse"]),
    ("typing", "typing", "module", "stdlib", "Аннотации типов.", "import typing", "from typing import List", ["typing", "аннотации"]),
    ("dataclasses", "dataclasses", "module", "stdlib", "Удобные классы для данных.", "from dataclasses import dataclass", "from dataclasses import dataclass", ["dataclass", "ООП"]),
    ("asyncio", "asyncio", "module", "stdlib", "Асинхронный ввод-вывод.", "import asyncio", "import asyncio; asyncio.run(main())", ["async", "asyncio"]),
    ("csv", "csv", "module", "stdlib", "Работа с CSV-файлами.", "import csv", "import csv", ["csv", "файлы"]),
    ("sqlite3", "sqlite3", "module", "stdlib", "Работа с базой SQLite.", "import sqlite3", "import sqlite3", ["база", "sqlite"]),
    ("urllib-request", "urllib.request", "module", "stdlib", "HTTP-запросы встроенными средствами.", "import urllib.request", "import urllib.request; urllib.request.urlopen('https://example.com')", ["http", "urllib"]),
    ("socket", "socket", "module", "stdlib", "Сетевые сокеты.", "import socket", "import socket", ["сеть", "socket"]),
    ("threading", "threading", "module", "stdlib", "Потоки.", "import threading", "import threading", ["потоки", "threading"]),
    ("multiprocessing", "multiprocessing", "module", "stdlib", "Процессы.", "import multiprocessing", "import multiprocessing", ["процессы", "multiprocessing"]),
    ("functools", "functools", "module", "stdlib", "Функции высшего порядка и утилиты.", "import functools", "import functools", ["functools"]),
    ("operator", "operator", "module", "stdlib", "Стандартные операции как функции.", "import operator", "import operator", ["operator"]),
    ("copy", "copy", "module", "stdlib", "Копирование объектов.", "import copy", "import copy; copy.copy([])", ["copy"]),
    ("pprint", "pprint", "module", "stdlib", "Красивый вывод структур данных.", "from pprint import pprint", "from pprint import pprint", ["pprint", "вывод"]),
    ("tempfile", "tempfile", "module", "stdlib", "Временные файлы и папки.", "import tempfile", "import tempfile", ["tempfile"]),
    ("glob", "glob", "module", "stdlib", "Поиск файлов по шаблонам.", "import glob", "import glob; glob.glob('*.py')", ["glob", "файлы"]),
    ("hashlib", "hashlib", "module", "stdlib", "Хэширование.", "import hashlib", "import hashlib", ["hash", "hashlib"]),
    ("base64", "base64", "module", "stdlib", "Кодирование Base64.", "import base64", "import base64", ["base64"]),
    ("uuid", "uuid", "module", "stdlib", "Генерация UUID.", "import uuid", "import uuid; uuid.uuid4()", ["uuid"]),
    ("decimal", "decimal", "module", "stdlib", "Точные десятичные вычисления.", "import decimal", "from decimal import Decimal", ["decimal", "числа"]),
    ("statistics", "statistics", "module", "stdlib", "Статистические функции.", "import statistics", "import statistics; statistics.mean([1, 2, 3])", ["statistics"])
]


def load_payload():
    for path in INPUT_PATHS:
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))

            if isinstance(data, list):
                return {
                    "meta": {},
                    "entries": data
                }

            return {
                "meta": data.get("meta", {}),
                "entries": data.get("entries", [])
            }

    return {
        "meta": {},
        "entries": []
    }


def related_key(item):
    if isinstance(item, str):
        return f"id:{item}"

    if isinstance(item, dict):
        if item.get("id"):
            return f"id:{item['id']}"

        return f"name:{item.get('name', '')}|syntax:{item.get('syntax', '')}"

    return f"raw:{str(item)}"


def merge_related_list(existing, extra):
    existing = list(existing or [])
    extra = list(extra or [])

    keys = {related_key(item) for item in existing}

    for item in extra:
        key = related_key(item)

        if key not in keys:
            existing.append(item)
            keys.add(key)

    return existing


def merge_related(entry, related):
    if not related:
        return

    entry_related = entry.setdefault("related", {})

    if not isinstance(entry_related, dict):
        entry_related = {
            "alternatives": [],
            "complements": [],
            "seealso": []
        }

    for key in ["alternatives", "complements", "seealso"]:
        entry_related[key] = merge_related_list(
            entry_related.get(key, []),
            related.get(key, [])
        )

    entry["related"] = entry_related


def default_returns(entry):
    entry_type = entry.get("type")

    if entry_type == "keyword":
        return "Не возвращает значение."

    if entry_type == "builtin-function":
        return "Зависит от функции."

    if entry_type == "builtin-type":
        return "Объект типа."

    if entry_type == "operator":
        return "Зависит от операции."

    if entry_type == "exception":
        return "Объект исключения."

    if entry_type == "module":
        return "Модуль."

    if entry_type == "cli":
        return "Результат выполнения команды."

    if entry_type == "library":
        return "Зависит от библиотеки."

    if entry_type == "os-command":
        return "Текстовый вывод или код завершения."

    return ""


def auto_example(entry):
    if entry.get("example"):
        return entry["example"]

    syntax = entry.get("syntax", "")

    if entry.get("type") == "module":
        if entry["id"] == "urllib-request":
            return "import urllib.request; urllib.request.urlopen('https://example.com')"

        return f"import {entry['id']}"

    if entry.get("type") in {"cli", "os-command"}:
        return syntax

    return syntax


def ensure_params(entry):
    if entry.get("params"):
        return

    entry_id = entry.get("id")
    entry_type = entry.get("type")

    if entry_id in PARAMS_EXTRA:
        entry["params"] = PARAMS_EXTRA[entry_id]
        return

    if entry_type == "operator":
        entry["params"] = [
            {
                "name": "a",
                "description": "Левый операнд."
            },
            {
                "name": "b",
                "description": "Правый операнд."
            }
        ]
        return

    if entry_type == "exception":
        entry["params"] = [
            {
                "name": "message",
                "description": "Текст ошибки."
            }
        ]
        return

    if entry_type == "builtin-type":
        if entry_id in {"list", "tuple", "set"}:
            entry["params"] = [
                {
                    "name": "iterable",
                    "description": "Итерируемый объект."
                }
            ]
        else:
            entry["params"] = [
                {
                    "name": "value",
                    "description": "Значение для преобразования."
                }
            ]
        return

    if entry_type == "builtin-function":
        entry["params"] = [
            {
                "name": "object",
                "description": "Входной объект."
            }
        ]
        return

    if entry_type in {"cli", "os-command"}:
        entry["params"] = [
            {
                "name": "arguments",
                "description": "Аргументы команды."
            }
        ]
        return

    entry["params"] = []


def ensure_errors(entry):
    if entry.get("errors"):
        return

    entry_id = entry.get("id")

    if entry_id in ERRORS_EXTRA:
        entry["errors"] = ERRORS_EXTRA[entry_id]
        return

    entry["errors"] = []


def ensure_returns(entry):
    if entry.get("returns"):
        return

    entry_id = entry.get("id")

    if entry_id in RETURNS_EXTRA:
        entry["returns"] = RETURNS_EXTRA[entry_id]
        return

    entry["returns"] = default_returns(entry)


def ensure_version(entry):
    version = entry.get("version")

    if not isinstance(version, dict):
        version = {}

    version.setdefault("since", None)
    version.setdefault("deprecated", None)
    version.setdefault("removed", None)
    version.setdefault("checked", None)

    if entry.get("category") in CHECKED_CATEGORIES and not version.get("checked"):
        version["checked"] = "3.13"

    entry["version"] = version


def ensure_examples(entry):
    if not entry.get("example") and not entry.get("examples"):
        entry["example"] = auto_example(entry)

    if not entry.get("examples"):
        entry["examples"] = [
            {
                "title": "Пример",
                "code": entry.get("example", "")
            }
        ]


def make_extra_entry(item):
    entry_id, name, entry_type, category, summary, syntax, example, tags = item

    entry = {
        "id": entry_id,
        "name": name,
        "type": entry_type,
        "category": category,
        "summary": summary,
        "syntax": syntax,
        "params": [],
        "returns": "",
        "errors": [],
        "example": example,
        "version": {},
        "tags": tags,
        "links": [],
        "related": {
            "alternatives": [],
            "complements": [],
            "seealso": []
        }
    }

    ensure_params(entry)
    ensure_errors(entry)
    ensure_returns(entry)
    ensure_version(entry)
    ensure_examples(entry)

    return entry


def add_new_entries(entries_by_id):
    for entry in NEW_ENTRIES:
        entry_id = entry["id"]

        if entry_id in entries_by_id:
            existing = entries_by_id[entry_id]
            new_related = entry.pop("related", None)

            existing.update(entry)

            if new_related:
                merge_related(existing, new_related)
        else:
            entries_by_id[entry_id] = entry

    for item in EXTRA_SIMPLE:
        entry = make_extra_entry(item)

        if entry["id"] not in entries_by_id:
            entries_by_id[entry["id"]] = entry


def apply_extra_related(entries_by_id):
    for entry_id, related in RELATED_EXTRA.items():
        if entry_id in entries_by_id:
            merge_related(entries_by_id[entry_id], related)


def assign_rank(entry):
    entry_id = entry.get("id")
    category = entry.get("category")

    entry["rank"] = POPULARITY.get(
        entry_id,
        CATEGORY_DEFAULT_RANK.get(category, 10000)
    )


def main():
    payload = load_payload()
    entries = payload.get("entries", [])

    entries_by_id = {entry["id"]: entry for entry in entries if "id" in entry}

    add_new_entries(entries_by_id)
    apply_extra_related(entries_by_id)

    prepared = []

    for entry in entries_by_id.values():
        ensure_params(entry)
        ensure_errors(entry)
        ensure_returns(entry)
        ensure_version(entry)
        ensure_examples(entry)
        assign_rank(entry)
        prepared.append(entry)

    prepared.sort(key=lambda item: (item.get("rank", 10000), item.get("name", "").lower()))

    payload["entries"] = prepared

    if "meta" not in payload:
        payload["meta"] = {}

    payload["meta"].setdefault("pythonVersions", [])
    payload["meta"].setdefault("news", [])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Saved {len(payload['entries'])} entries to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()