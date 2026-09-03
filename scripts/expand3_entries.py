#!/usr/bin/env python3
import json
from pathlib import Path


INPUT_PATHS = [Path("data/entries.json"), Path("entries.json")]
OUTPUT_PATH = Path("data/entries.json")


CATEGORY_DEFAULT_RANK = {
    "core": 1500, "builtin": 2000, "file": 2400, "string": 2500, "list": 2600,
    "dict": 2700, "set": 2800, "types": 3000, "operators": 4000, "exceptions": 5000,
    "stdlib": 6000, "python-cli": 7000, "dev-tools": 7500, "packages": 8000, "os": 9000,
    "special": 3500,
}


# (id, name, type, category, summary, syntax, example, tags)
NEW3 = [
    # ---- Специальные методы ----
    ("__init__", "__init__()", "method", "special", "Инициализатор объекта.", "def __init__(self):", "def __init__(self): pass", ["init"]),
    ("__str__", "__str__()", "method", "special", "Строковое представление.", "def __str__(self):", "def __str__(self): return 'x'", ["str"]),
    ("__repr__", "__repr__()", "method", "special", "Представление для отладки.", "def __repr__(self):", "def __repr__(self): return 'X()'", ["repr"]),
    ("__len__", "__len__()", "method", "special", "Длина объекта.", "def __len__(self):", "def __len__(self): return 0", ["len"]),
    ("__getitem__", "__getitem__()", "method", "special", "Доступ по индексу.", "def __getitem__(self, key):", "obj[0]", ["getitem"]),
    ("__setitem__", "__setitem__()", "method", "special", "Установка по индексу.", "def __setitem__(self, key, val):", "obj[0] = 1", ["setitem"]),
    ("__delitem__", "__delitem__()", "method", "special", "Удаление по индексу.", "def __delitem__(self, key):", "del obj[0]", ["delitem"]),
    ("__iter__", "__iter__()", "method", "special", "Возвращает итератор.", "def __iter__(self):", "for x in obj:", ["iter"]),
    ("__next__", "__next__()", "method", "special", "Следующий элемент.", "def __next__(self):", "next(it)", ["next"]),
    ("__contains__", "__contains__()", "method", "special", "Проверка вхождения.", "def __contains__(self, item):", "item in obj", ["contains"]),
    ("__call__", "__call__()", "method", "special", "Вызов как функции.", "def __call__(self):", "obj()", ["call"]),
    ("__enter__", "__enter__()", "method", "special", "Вход в контекст.", "def __enter__(self):", "with obj:", ["enter"]),
    ("__exit__", "__exit__()", "method", "special", "Выход из контекста.", "def __exit__(self, *args):", "with obj:", ["exit"]),
    ("__add__", "__add__()", "method", "special", "Сложение.", "def __add__(self, other):", "obj + other", ["add"]),
    ("__sub__", "__sub__()", "method", "special", "Вычитание.", "def __sub__(self, other):", "obj - other", ["sub"]),
    ("__mul__", "__mul__()", "method", "special", "Умножение.", "def __mul__(self, other):", "obj * other", ["mul"]),
    ("__truediv__", "__truediv__()", "method", "special", "Деление.", "def __truediv__(self, other):", "obj / other", ["div"]),
    ("__floordiv__", "__floordiv__()", "method", "special", "Целочисленное деление.", "def __floordiv__(self, other):", "obj // other", ["floordiv"]),
    ("__mod__", "__mod__()", "method", "special", "Остаток.", "def __mod__(self, other):", "obj % other", ["mod"]),
    ("__pow__", "__pow__()", "method", "special", "Степень.", "def __pow__(self, other):", "obj ** other", ["pow"]),
    ("__eq__", "__eq__()", "method", "special", "Равенство.", "def __eq__(self, other):", "obj == other", ["eq"]),
    ("__ne__", "__ne__()", "method", "special", "Неравенство.", "def __ne__(self, other):", "obj != other", ["ne"]),
    ("__lt__", "__lt__()", "method", "special", "Меньше.", "def __lt__(self, other):", "obj < other", ["lt"]),
    ("__le__", "__le__()", "method", "special", "Меньше или равно.", "def __le__(self, other):", "obj <= other", ["le"]),
    ("__gt__", "__gt__()", "method", "special", "Больше.", "def __gt__(self, other):", "obj > other", ["gt"]),
    ("__ge__", "__ge__()", "method", "special", "Больше или равно.", "def __ge__(self, other):", "obj >= other", ["ge"]),
    ("__hash__", "__hash__()", "method", "special", "Хэш объекта.", "def __hash__(self):", "hash(obj)", ["hash"]),
    ("__bool__", "__bool__()", "method", "special", "Булево значение.", "def __bool__(self):", "bool(obj)", ["bool"]),
    ("__new__", "__new__()", "method", "special", "Создание объекта.", "def __new__(cls):", "object.__new__(cls)", ["new"]),
    ("__del__", "__del__()", "method", "special", "Удаление объекта.", "def __del__(self):", "del obj", ["del"]),
    ("__getattr__", "__getattr__()", "method", "special", "Получение атрибута.", "def __getattr__(self, name):", "obj.attr", ["getattr"]),
    ("__setattr__", "__setattr__()", "method", "special", "Установка атрибута.", "def __setattr__(self, name, val):", "obj.attr = val", ["setattr"]),
    ("__delattr__", "__delattr__()", "method", "special", "Удаление атрибута.", "def __delattr__(self, name):", "del obj.attr", ["delattr"]),
    ("__dir__", "__dir__()", "method", "special", "Список атрибутов.", "def __dir__(self):", "dir(obj)", ["dir"]),
    ("__class__", "__class__", "method", "special", "Класс объекта.", "obj.__class__", "obj.__class__", ["class"]),
    ("__dict__", "__dict__", "method", "special", "Словарь атрибутов.", "obj.__dict__", "obj.__dict__", ["dict"]),
    ("__doc__", "__doc__", "method", "special", "Документация.", "obj.__doc__", "func.__doc__", ["doc"]),
    ("__name__", "__name__", "method", "special", "Имя объекта.", "obj.__name__", "func.__name__", ["name"]),
    ("__module__", "__module__", "method", "special", "Модуль объекта.", "obj.__module__", "func.__module__", ["module"]),
    ("__annotations__", "__annotations__", "method", "special", "Аннотации типов.", "obj.__annotations__", "func.__annotations__", ["annotations"]),
    ("__bases__", "__bases__", "method", "special", "Базовые классы.", "cls.__bases__", "MyClass.__bases__", ["bases"]),
    ("__mro__", "__mro__", "method", "special", "Порядок разрешения методов.", "cls.__mro__", "MyClass.__mro__", ["mro"]),
    ("__subclasses__", "__subclasses__()", "method", "special", "Подклассы.", "cls.__subclasses__()", "MyClass.__subclasses__()", ["subclasses"]),

    # ---- Методы строк (дополнительные) ----
    ("str-maketrans", "str.maketrans()", "method", "string", "Создаёт таблицу трансляции.", "str.maketrans(x, y)", "str.maketrans('a', 'b')", ["maketrans"]),
    ("str-translate", "str.translate()", "method", "string", "Применяет таблицу трансляции.", "str.translate(table)", "'abc'.translate(table)", ["translate"]),
    ("str-expandtabs", "str.expandtabs()", "method", "string", "Раскрывает табуляцию.", "str.expandtabs(tabsize)", "'a\\tb'.expandtabs(4)", ["expandtabs"]),
    ("str-capitalize", "str.capitalize()", "method", "string", "Первая буква заглавная.", "str.capitalize()", "'abc'.capitalize()", ["capitalize"]),
    ("str-isidentifier", "str.isidentifier()", "method", "string", "Валидный идентификатор?", "str.isidentifier()", "'var1'.isidentifier()", ["isidentifier"]),
    ("str-isprintable", "str.isprintable()", "method", "string", "Печатаемые символы?", "str.isprintable()", "'abc'.isprintable()", ["isprintable"]),
    ("str-isdecimal", "str.isdecimal()", "method", "string", "Десятичные цифры?", "str.isdecimal()", "'123'.isdecimal()", ["isdecimal"]),
    ("str-isnumeric", "str.isnumeric()", "method", "string", "Числовые символы?", "str.isnumeric()", "'123'.isnumeric()", ["isnumeric"]),

    # ---- Методы списков (дополнительные) ----
    ("list-comprehension", "list comprehension", "syntax", "list", "Создание списка в одну строку.", "[expr for x in iter]", "[x*2 for x in range(3)]", ["comprehension"]),

    # ---- Методы словарей (дополнительные) ----
    ("dict-popitem", "dict.popitem()", "method", "dict", "Удаляет и возвращает пару.", "dict.popitem()", "data.popitem()", ["popitem"]),
    ("dict-reversed", "reversed(dict)", "method", "dict", "Обратный итератор ключей.", "reversed(d)", "list(reversed(data))", ["reversed"]),

    # ---- Методы множеств (дополнительные) ----
    ("set-symmetric-difference", "set.symmetric_difference()", "method", "set", "Симметрическая разность.", "set.symmetric_difference(other)", "s ^ t", ["symmetric_difference"]),
    ("set-issubset", "set.issubset()", "method", "set", "Является подмножеством?", "set.issubset(other)", "s <= t", ["issubset"]),
    ("set-issuperset", "set.issuperset()", "method", "set", "Является надмножеством?", "set.issuperset(other)", "s >= t", ["issuperset"]),
    ("set-isdisjoint", "set.isdisjoint()", "method", "set", "Нет общих элементов?", "set.isdisjoint(other)", "s.isdisjoint(t)", ["isdisjoint"]),
    ("set-update", "set.update()", "method", "set", "Добавляет элементы.", "set.update(iter)", "s.update([1, 2])", ["update"]),
    ("set-intersection-update", "set.intersection_update()", "method", "set", "Оставляет пересечение.", "set.intersection_update(other)", "s &= t", ["intersection_update"]),
    ("set-difference-update", "set.difference_update()", "method", "set", "Оставляет разность.", "set.difference_update(other)", "s -= t", ["difference_update"]),
    ("set-symmetric-difference-update", "set.symmetric_difference_update()", "method", "set", "Оставляет симм. разность.", "set.symmetric_difference_update(other)", "s ^= t", ["symmetric_difference_update"]),
    ("set-pop", "set.pop()", "method", "set", "Удаляет и возвращает элемент.", "set.pop()", "s.pop()", ["pop"]),
    ("set-clear", "set.clear()", "method", "set", "Очищает множество.", "set.clear()", "s.clear()", ["clear"]),
    ("set-copy", "set.copy()", "method", "set", "Поверхностная копия.", "set.copy()", "s.copy()", ["copy"]),

    # ---- Методы bytes/bytearray ----
    ("bytes-fromhex", "bytes.fromhex()", "method", "types", "Байты из hex-строки.", "bytes.fromhex(string)", "bytes.fromhex('ff')", ["fromhex"]),
    ("bytes-hex", "bytes.hex()", "method", "types", "Байты в hex-строку.", "bytes.hex()", "b'\\xff'.hex()", ["hex"]),
    ("bytearray-append", "bytearray.append()", "method", "types", "Добавляет байт.", "bytearray.append(x)", "ba.append(65)", ["append"]),
    ("bytearray-extend", "bytearray.extend()", "method", "types", "Добавляет байты.", "bytearray.extend(it)", "ba.extend(b'ab')", ["extend"]),

    # ---- Модули стандартной библиотеки ----
    ("email", "email", "module", "stdlib", "Работа с email.", "import email", "email.message.EmailMessage()", ["email"]),
    ("html", "html", "module", "stdlib", "Работа с HTML.", "import html", "html.escape('<')", ["html"]),
    ("http", "http", "module", "stdlib", "HTTP-протокол.", "import http", "http.HTTPStatus.OK", ["http"]),
    ("xml", "xml", "module", "stdlib", "Работа с XML.", "import xml.etree.ElementTree", "xml.etree.ElementTree.parse('f.xml')", ["xml"]),
    ("tkinter", "tkinter", "module", "stdlib", "GUI-библиотека.", "import tkinter", "tkinter.Tk()", ["tkinter"]),
    ("turtle", "turtle", "module", "stdlib", "Графика черепахи.", "import turtle", "turtle.Turtle()", ["turtle"]),
    ("ctypes", "ctypes", "module", "stdlib", "Вызов C-функций.", "import ctypes", "ctypes.CDLL('lib.so')", ["ctypes"]),
    ("multiprocessing", "multiprocessing", "module", "stdlib", "Многопроцессорность.", "import multiprocessing", "multiprocessing.Process()", ["multiprocessing"]),
    ("concurrent-futures", "concurrent.futures", "module", "stdlib", "Пулы потоков/процессов.", "import concurrent.futures", "concurrent.futures.ThreadPoolExecutor()", ["concurrent"]),
    ("queue", "queue", "module", "stdlib", "Очереди для потоков.", "import queue", "queue.Queue()", ["queue"]),
    ("sched", "sched", "module", "stdlib", "Планировщик событий.", "import sched", "sched.scheduler()", ["sched"]),
    ("signal", "signal", "module", "stdlib", "Обработка сигналов.", "import signal", "signal.signal(signal.SIGINT, handler)", ["signal"]),
    ("mmap", "mmap", "module", "stdlib", "Отображение файлов в память.", "import mmap", "mmap.mmap(f.fileno(), 0)", ["mmap"]),
    ("select", "select", "module", "stdlib", "Мультиплексирование ввода-вывода.", "import select", "select.select([sock], [], [])", ["select"]),
    ("selectors", "selectors", "module", "stdlib", "Высокоуровневый select.", "import selectors", "selectors.DefaultSelector()", ["selectors"]),
    ("asyncore", "asyncore", "module", "stdlib", "Асинхронный ввод-вывод (устарел).", "import asyncore", "asyncore.loop()", ["asyncore"]),
    ("asynchat", "asynchat", "module", "stdlib", "Асинхронный чат (устарел).", "import asynchat", "asynchat.async_chat()", ["asynchat"]),
    ("wsgiref", "wsgiref", "module", "stdlib", "WSGI-сервер.", "import wsgiref.simple_server", "wsgiref.simple_server.make_server()", ["wsgiref"]),
    ("xmlrpc", "xmlrpc", "module", "stdlib", "XML-RPC.", "import xmlrpc.server", "xmlrpc.server.SimpleXMLRPCServer()", ["xmlrpc"]),
    ("ftplib", "ftplib", "module", "stdlib", "FTP-клиент.", "import ftplib", "ftplib.FTP('host')", ["ftplib"]),
    ("poplib", "poplib", "module", "stdlib", "POP3-клиент.", "import poplib", "poplib.POP3('host')", ["poplib"]),
    ("imaplib", "imaplib", "module", "stdlib", "IMAP-клиент.", "import imaplib", "imaplib.IMAP4('host')", ["imaplib"]),
    ("smtplib", "smtplib", "module", "stdlib", "SMTP-клиент.", "import smtplib", "smtplib.SMTP('host')", ["smtplib"]),
    ("nntplib", "nntplib", "module", "stdlib", "NNTP-клиент.", "import nntplib", "nntplib.NNTP('host')", ["nntplib"]),
    ("telnetlib", "telnetlib", "module", "stdlib", "Telnet-клиент.", "import telnetlib", "telnetlib.Telnet('host')", ["telnetlib"]),
    ("cmd", "cmd", "module", "stdlib", "Командная строка.", "import cmd", "cmd.Cmd()", ["cmd"]),
    ("shlex", "shlex", "module", "stdlib", "Разбор shell-строк.", "import shlex", "shlex.split('a \"b c\"')", ["shlex"]),
    ("curses", "curses", "module", "stdlib", "Терминальный UI.", "import curses", "curses.wrapper(main)", ["curses"]),
    ("readline", "readline", "module", "stdlib", "GNU readline.", "import readline", "readline.parse_and_bind()", ["readline"]),
    ("rlcompleter", "rlcompleter", "module", "stdlib", "Автодополнение.", "import rlcompleter", "rlcompleter.Completer()", ["rlcompleter"]),
    ("tokenize", "tokenize", "module", "stdlib", "Токенизация Python.", "import tokenize", "tokenize.tokenize(f.readline)", ["tokenize"]),
    ("keyword", "keyword", "module", "stdlib", "Ключевые слова Python.", "import keyword", "keyword.kwlist", ["keyword"]),
    ("token", "token", "module", "stdlib", "Токены Python.", "import token", "token.NUMBER", ["token"]),
    ("tabnanny", "tabnanny", "module", "stdlib", "Проверка отступов.", "import tabnanny", "tabnanny.check('file.py')", ["tabnanny"]),
    ("pyclbr", "pyclbr", "module", "stdlib", "Чтение классов Python.", "import pyclbr", "pyclbr.readmodule('mod')", ["pyclbr"]),
    ("py_compile", "py_compile", "module", "stdlib", "Компиляция в .pyc.", "import py_compile", "py_compile.compile('file.py')", ["py_compile"]),
    ("compileall", "compileall", "module", "stdlib", "Компиляция всех файлов.", "import compileall", "compileall.compile_dir('dir')", ["compileall"]),
    ("dis", "dis", "module", "stdlib", "Дизассемблер байткода.", "import dis", "dis.dis(func)", ["dis"]),
    ("distutils", "distutils", "module", "stdlib", "Сборка пакетов (устарел).", "import distutils", "distutils.core.setup()", ["distutils"]),
    ("ensurepip", "ensurepip", "module", "stdlib", "Установка pip.", "import ensurepip", "ensurepip.bootstrap()", ["ensurepip"]),
    ("venv", "venv", "module", "stdlib", "Виртуальные окружения.", "import venv", "venv.EnvBuilder()", ["venv"]),
    ("zipapp", "zipapp", "module", "stdlib", "Создание zip-приложений.", "import zipapp", "zipapp.create_archive()", ["zipapp"]),
    ("test", "test", "module", "stdlib", "Тесты Python.", "import test", "test.support", ["test"]),
    ("doctest", "doctest", "module", "stdlib", "Тесты в docstring.", "import doctest", "doctest.testmod()", ["doctest"]),
    ("bdb", "bdb", "module", "stdlib", "Отладчик.", "import bdb", "bdb.Bdb()", ["bdb"]),
    ("faulthandler", "faulthandler", "module", "stdlib", "Обработчик сбоев.", "import faulthandler", "faulthandler.enable()", ["faulthandler"]),
    ("tracemalloc", "tracemalloc", "module", "stdlib", "Трассировка памяти.", "import tracemalloc", "tracemalloc.start()", ["tracemalloc"]),
    ("gc", "gc", "module", "stdlib", "Сборщик мусора.", "import gc", "gc.collect()", ["gc"]),
    ("weakref", "weakref", "module", "stdlib", "Слабые ссылки.", "import weakref", "weakref.ref(obj)", ["weakref"]),
    ("atexit", "atexit", "module", "stdlib", "Действия при выходе.", "import atexit", "atexit.register(func)", ["atexit"]),
    ("builtins", "builtins", "module", "stdlib", "Встроенные функции.", "import builtins", "builtins.print()", ["builtins"]),
    ("__future__", "__future__", "module", "stdlib", "Будущие возможности.", "from __future__ import annotations", "from __future__ import annotations", ["future"]),
    ("__main__", "__main__", "module", "stdlib", "Главный модуль.", "if __name__ == '__main__':", "if __name__ == '__main__':", ["main"]),

    # ---- Git команды ----
    ("git-merge", "git merge", "cli", "dev-tools", "Сливает ветки.", "git merge branch", "git merge main", ["git"]),
    ("git-rebase", "git rebase", "cli", "dev-tools", "Переносит коммиты.", "git rebase branch", "git rebase main", ["git"]),
    ("git-reset", "git reset", "cli", "dev-tools", "Сбрасывает изменения.", "git reset commit", "git reset HEAD", ["git"]),
    ("git-revert", "git revert", "cli", "dev-tools", "Отменяет коммит.", "git revert commit", "git revert HEAD", ["git"]),
    ("git-stash", "git stash", "cli", "dev-tools", "Временно сохраняет изменения.", "git stash", "git stash pop", ["git"]),
    ("git-tag", "git tag", "cli", "dev-tools", "Создаёт теги.", "git tag name", "git tag v1.0", ["git"]),
    ("git-fetch", "git fetch", "cli", "dev-tools", "Забирает изменения без слияния.", "git fetch", "git fetch origin", ["git"]),
    ("git-diff", "git diff", "cli", "dev-tools", "Показывает изменения.", "git diff", "git diff HEAD", ["git"]),
    ("git-show", "git show", "cli", "dev-tools", "Показывает коммит.", "git show commit", "git show HEAD", ["git"]),
    ("git-blame", "git blame", "cli", "dev-tools", "Кто изменил строку.", "git blame file", "git blame file.py", ["git"]),
    ("git-remote", "git remote", "cli", "dev-tools", "Удалённые репозитории.", "git remote", "git remote -v", ["git"]),
    ("git-config", "git config", "cli", "dev-tools", "Настройки Git.", "git config key value", "git config user.name 'Name'", ["git"]),

    # ---- OS команды ----
    ("awk", "awk", "os-command", "os", "Обработка текста.", "awk pattern file", "awk '{print $1}' file", ["awk"]),
    ("sed", "sed", "os-command", "os", "Редактор потока.", "sed cmd file", "sed 's/a/b/' file", ["sed"]),
    ("xargs", "xargs", "os-command", "os", "Передача аргументов.", "cmd | xargs cmd2", "find . | xargs rm", ["xargs"]),
    ("du", "du", "os-command", "os", "Размер файлов/папок.", "du path", "du -sh dir", ["du"]),
    ("df", "df", "os-command", "os", "Свободное место.", "df", "df -h", ["df"]),
    ("mount", "mount", "os-command", "os", "Монтирование файловых систем.", "mount device dir", "mount /dev/sda1 /mnt", ["mount"]),
    ("umount", "umount", "os-command", "os", "Размонтирование.", "umount dir", "umount /mnt", ["umount"]),
    ("ln", "ln", "os-command", "os", "Создаёт ссылки.", "ln target link", "ln -s target link", ["ln"]),
    ("diff", "diff", "os-command", "os", "Сравнивает файлы.", "diff file1 file2", "diff a.txt b.txt", ["diff"]),
    ("patch", "patch", "os-command", "os", "Применяет патчи.", "patch file patch", "patch < diff.patch", ["patch"]),
    ("make", "make", "os-command", "os", "Сборка проектов.", "make target", "make", ["make"]),
    ("cmake", "cmake", "os-command", "os", "Генератор сборки.", "cmake dir", "cmake .", ["cmake"]),
    ("gcc", "gcc", "os-command", "os", "Компилятор C.", "gcc file.c", "gcc main.c -o main", ["gcc"]),
    ("g++", "g++", "os-command", "os", "Компилятор C++.", "g++ file.cpp", "g++ main.cpp -o main", ["g++"]),
    ("java", "java", "os-command", "os", "Запуск Java.", "java Class", "java Main", ["java"]),
    ("javac", "javac", "os-command", "os", "Компилятор Java.", "javac file.java", "javac Main.java", ["javac"]),
    ("node", "node", "os-command", "os", "Запуск Node.js.", "node script.js", "node app.js", ["node"]),
    ("npm", "npm", "os-command", "os", "Менеджер пакетов Node.", "npm command", "npm install", ["npm"]),
    ("docker", "docker", "os-command", "os", "Контейнеры.", "docker command", "docker run image", ["docker"]),
    ("docker-compose", "docker-compose", "os-command", "os", "Оркестрация контейнеров.", "docker-compose command", "docker-compose up", ["docker"]),
    ("kubectl", "kubectl", "os-command", "os", "Управление Kubernetes.", "kubectl command", "kubectl get pods", ["kubectl"]),
    ("systemctl", "systemctl", "os-command", "os", "Управление службами.", "systemctl command service", "systemctl start nginx", ["systemctl"]),
    ("journalctl", "journalctl", "os-command", "os", "Просмотр логов.", "journalctl", "journalctl -u service", ["journalctl"]),
    ("apt", "apt", "os-command", "os", "Менеджер пакетов Debian/Ubuntu.", "apt command", "apt install pkg", ["apt"]),
    ("yum", "yum", "os-command", "os", "Менеджер пакетов RHEL/CentOS.", "yum command", "yum install pkg", ["yum"]),
    ("dnf", "dnf", "os-command", "os", "Менеджер пакетов Fedora.", "dnf command", "dnf install pkg", ["dnf"]),
    ("pacman", "pacman", "os-command", "os", "Менеджер пакетов Arch.", "pacman command", "pacman -S pkg", ["pacman"]),
    ("brew", "brew", "os-command", "os", "Менеджер пакетов macOS.", "brew command", "brew install pkg", ["brew"]),
    ("choco", "choco", "os-command", "os", "Менеджер пакетов Windows.", "choco command", "choco install pkg", ["choco"]),

    # ---- Сторонние библиотеки ----
    ("aiofiles", "aiofiles", "library", "packages", "Асинхронная работа с файлами.", "pip install aiofiles", "async with aiofiles.open('f') as f:", ["aiofiles"]),
    ("boto3", "boto3", "library", "packages", "AWS SDK для Python.", "pip install boto3", "boto3.client('s3')", ["boto3"]),
    ("celery", "Celery", "library", "packages", "Очереди задач.", "pip install celery", "celery -A tasks worker", ["celery"]),
    ("dramatiq", "dramatiq", "library", "packages", "Очереди задач (альтернатива Celery).", "pip install dramatiq", "dramatiq.actor", ["dramatiq"]),
    ("faker", "Faker", "library", "packages", "Генерация фейковых данных.", "pip install faker", "Faker().name()", ["faker"]),
    ("hypothesis", "Hypothesis", "library", "packages", "Property-based тестирование.", "pip install hypothesis", "@given(st.integers())", ["hypothesis"]),
    ("locust", "Locust", "library", "packages", "Нагрузочное тестирование.", "pip install locust", "locust -f locustfile.py", ["locust"]),
    ("pytest-asyncio", "pytest-asyncio", "library", "packages", "Async тесты для pytest.", "pip install pytest-asyncio", "@pytest.mark.asyncio", ["pytest"]),
    ("pytest-cov", "pytest-cov", "library", "packages", "Покрытие кода для pytest.", "pip install pytest-cov", "pytest --cov=app", ["pytest"]),
    ("redis", "redis", "library", "packages", "Redis клиент.", "pip install redis", "redis.Redis()", ["redis"]),
    ("rq", "rq", "library", "packages", "Очереди задач на Redis.", "pip install rq", "rq.Queue()", ["rq"]),
    ("aiohttp", "aiohttp", "library", "packages", "Асинхронный HTTP.", "pip install aiohttp", "aiohttp.ClientSession()", ["aiohttp"]),
    ("httpx", "httpx", "library", "packages", "Современный HTTP-клиент.", "pip install httpx", "httpx.get('url')", ["httpx"]),
    ("starlette", "Starlette", "library", "packages", "ASGI-фреймворк.", "pip install starlette", "starlette.applications.Starlette()", ["starlette"]),
    ("uvicorn", "uvicorn", "library", "packages", "ASGI-сервер.", "pip install uvicorn", "uvicorn main:app", ["uvicorn"]),
    ("gunicorn", "gunicorn", "library", "packages", "WSGI-сервер.", "pip install gunicorn", "gunicorn app:app", ["gunicorn"]),
    ("psycopg2", "psycopg2", "library", "packages", "PostgreSQL драйвер.", "pip install psycopg2", "psycopg2.connect()", ["psycopg2"]),
    ("pymysql", "PyMySQL", "library", "packages", "MySQL драйвер.", "pip install pymysql", "pymysql.connect()", ["pymysql"]),
    ("motor", "motor", "library", "packages", "Async MongoDB драйвер.", "pip install motor", "motor.motor_asyncio.AsyncIOMotorClient()", ["motor"]),
    ("pymongo", "pymongo", "library", "packages", "MongoDB драйвер.", "pip install pymongo", "pymongo.MongoClient()", ["pymongo"]),
    ("elasticsearch", "elasticsearch", "library", "packages", "Elasticsearch клиент.", "pip install elasticsearch", "elasticsearch.Elasticsearch()", ["elasticsearch"]),
    ("kafka-python", "kafka-python", "library", "packages", "Kafka клиент.", "pip install kafka-python", "kafka.KafkaProducer()", ["kafka"]),
    ("pika", "pika", "library", "packages", "RabbitMQ клиент.", "pip install pika", "pika.BlockingConnection()", ["pika"]),
    ("grpcio", "grpcio", "library", "packages", "gRPC для Python.", "pip install grpcio", "grpc.insecure_channel()", ["grpc"]),
    ("protobuf", "protobuf", "library", "packages", "Protocol Buffers.", "pip install protobuf", "protobuf.message.Message()", ["protobuf"]),
    ("marshmallow", "marshmallow", "library", "packages", "Сериализация/валидация.", "pip install marshmallow", "marshmallow.Schema()", ["marshmallow"]),
    ("attrs", "attrs", "library", "packages", "Улучшенные классы.", "pip install attrs", "@attrs.define", ["attrs"]),
    ("pydantic", "pydantic", "library", "packages", "Валидация данных.", "pip install pydantic", "pydantic.BaseModel", ["pydantic"]),
    ("sqlalchemy", "SQLAlchemy", "library", "packages", "ORM.", "pip install sqlalchemy", "sqlalchemy.create_engine()", ["sqlalchemy"]),
    ("alembic", "alembic", "library", "packages", "Миграции БД.", "pip install alembic", "alembic upgrade head", ["alembic"]),
    ("django-rest-framework", "DRF", "library", "packages", "REST API для Django.", "pip install djangorestframework", "rest_framework.views.APIView", ["django"]),
    ("graphene", "graphene", "library", "packages", "GraphQL для Python.", "pip install graphene", "graphene.ObjectType", ["graphene"]),
    ("strawberry", "strawberry", "library", "packages", "GraphQL (современный).", "pip install strawberry-graphql", "@strawberry.type", ["strawberry"]),
    ("ariadne", "ariadne", "library", "packages", "GraphQL сервер.", "pip install ariadne", "ariadne.make_executable_schema()", ["ariadne"]),
    ("sentry-sdk", "sentry-sdk", "library", "packages", "Отслеживание ошибок.", "pip install sentry-sdk", "sentry_sdk.init()", ["sentry"]),
    ("prometheus-client", "prometheus-client", "library", "packages", "Метрики Prometheus.", "pip install prometheus-client", "prometheus_client.Counter()", ["prometheus"]),
    ("opentelemetry", "opentelemetry", "library", "packages", "Трассировка и метрики.", "pip install opentelemetry-api", "opentelemetry.trace.get_tracer()", ["opentelemetry"]),
    ("structlog", "structlog", "library", "packages", "Структурированные логи.", "pip install structlog", "structlog.get_logger()", ["structlog"]),
    ("loguru", "loguru", "library", "packages", "Простое логирование.", "pip install loguru", "from loguru import logger", ["loguru"]),
    ("tenacity", "tenacity", "library", "packages", "Повторы с backoff.", "pip install tenacity", "@tenacity.retry", ["tenacity"]),
    ("circuitbreaker", "circuitbreaker", "library", "packages", "Circuit breaker.", "pip install circuitbreaker", "@circuitbreaker.circuit", ["circuitbreaker"]),
    ("limits", "limits", "library", "packages", "Rate limiting.", "pip install limits", "limits.parse('10/minute')", ["limits"]),
    ("slowapi", "slowapi", "library", "packages", "Rate limiting для FastAPI.", "pip install slowapi", "slowapi.Limiter()", ["slowapi"]),
    ("python-jose", "python-jose", "library", "packages", "JWT токены.", "pip install python-jose", "jose.jwt.encode()", ["jose"]),
    ("passlib", "passlib", "library", "packages", "Хэширование паролей.", "pip install passlib", "passlib.hash.bcrypt.hash()", ["passlib"]),
    ("bcrypt", "bcrypt", "library", "packages", "Bcrypt хэширование.", "pip install bcrypt", "bcrypt.hashpw()", ["bcrypt"]),
    ("cryptography", "cryptography", "library", "packages", "Криптография.", "pip install cryptography", "cryptography.fernet.Fernet()", ["cryptography"]),
    ("pyjwt", "PyJWT", "library", "packages", "JWT токены.", "pip install pyjwt", "jwt.encode()", ["jwt"]),
    ("oauthlib", "oauthlib", "library", "packages", "OAuth.", "pip install oauthlib", "oauthlib.oauth2.WebApplicationClient()", ["oauth"]),
    ("authlib", "authlib", "library", "packages", "OAuth/OpenID Connect.", "pip install authlib", "authlib.integrations.flask_client.OAuth()", ["authlib"]),
    ("python-multipart", "python-multipart", "library", "packages", "Парсинг multipart.", "pip install python-multipart", "multipart.parse_form_data()", ["multipart"]),
    ("python-magic", "python-magic", "library", "packages", "Определение MIME-типов.", "pip install python-magic", "magic.from_file('f')", ["magic"]),
    ("pillow", "Pillow", "library", "packages", "Обработка изображений.", "pip install pillow", "PIL.Image.open('f.png')", ["pillow"]),
    ("opencv-python", "opencv-python", "library", "packages", "Компьютерное зрение.", "pip install opencv-python", "cv2.imread('f.png')", ["opencv"]),
    ("matplotlib", "matplotlib", "library", "packages", "Графики.", "pip install matplotlib", "matplotlib.pyplot.plot()", ["matplotlib"]),
    ("seaborn", "seaborn", "library", "packages", "Статистические графики.", "pip install seaborn", "seaborn.scatterplot()", ["seaborn"]),
    ("plotly", "plotly", "library", "packages", "Интерактивные графики.", "pip install plotly", "plotly.express.scatter()", ["plotly"]),
    ("bokeh", "bokeh", "library", "packages", "Интерактивная визуализация.", "pip install bokeh", "bokeh.plotting.figure()", ["bokeh"]),
    ("altair", "altair", "library", "packages", "Декларативная визуализация.", "pip install altair", "altair.Chart()", ["altair"]),
    ("scikit-learn", "scikit-learn", "library", "packages", "Машинное обучение.", "pip install scikit-learn", "sklearn.ensemble.RandomForestClassifier()", ["sklearn"]),
    ("tensorflow", "TensorFlow", "library", "packages", "Глубокое обучение.", "pip install tensorflow", "tf.keras.Sequential()", ["tensorflow"]),
    ("pytorch", "PyTorch", "library", "packages", "Глубокое обучение.", "pip install torch", "torch.nn.Linear()", ["pytorch"]),
    ("keras", "Keras", "library", "packages", "API для глубокого обучения.", "pip install keras", "keras.Sequential()", ["keras"]),
    ("xgboost", "xgboost", "library", "packages", "Градиентный бустинг.", "pip install xgboost", "xgboost.XGBClassifier()", ["xgboost"]),
    ("lightgbm", "lightgbm", "library", "packages", "Градиентный бустинг.", "pip install lightgbm", "lightgbm.LGBMClassifier()", ["lightgbm"]),
    ("catboost", "catboost", "library", "packages", "Градиентный бустинг.", "pip install catboost", "catboost.CatBoostClassifier()", ["catboost"]),
    ("spacy", "spaCy", "library", "packages", "NLP.", "pip install spacy", "spacy.load('en_core_web_sm')", ["spacy"]),
    ("nltk", "nltk", "library", "packages", "NLP (классика).", "pip install nltk", "nltk.word_tokenize()", ["nltk"]),
    ("transformers", "transformers", "library", "packages", "Hugging Face модели.", "pip install transformers", "transformers.pipeline()", ["transformers"]),
    ("datasets", "datasets", "library", "packages", "Hugging Face датасеты.", "pip install datasets", "datasets.load_dataset()", ["datasets"]),
    ("langchain", "langchain", "library", "packages", "LLM приложения.", "pip install langchain", "langchain.LLMChain()", ["langchain"]),
    ("llama-index", "llama-index", "library", "packages", "Индексы для LLM.", "pip install llama-index", "llama_index.VectorStoreIndex()", ["llama"]),
    ("openai", "openai", "library", "packages", "OpenAI API.", "pip install openai", "openai.ChatCompletion.create()", ["openai"]),
    ("anthropic", "anthropic", "library", "packages", "Anthropic API.", "pip install anthropic", "anthropic.Anthropic()", ["anthropic"]),
    ("google-generativeai", "google-generativeai", "library", "packages", "Google AI API.", "pip install google-generativeai", "genai.GenerativeModel()", ["google"]),
    ("streamlit", "streamlit", "library", "packages", "Веб-приложения для данных.", "pip install streamlit", "streamlit.title()", ["streamlit"]),
    ("gradio", "gradio", "library", "packages", "UI для ML моделей.", "pip install gradio", "gradio.Interface()", ["gradio"]),
    ("dash", "dash", "library", "packages", "Веб-приложения для данных.", "pip install dash", "dash.Dash()", ["dash"]),
    ("panel", "panel", "library", "packages", "Интерактивные дашборды.", "pip install panel", "panel.pane.Markdown()", ["panel"]),
    ("voila", "voila", "library", "packages", "Jupyter в веб.", "pip install voila", "voila app.ipynb", ["voila"]),
    ("nbconvert", "nbconvert", "library", "packages", "Конвертация ноутбуков.", "pip install nbconvert", "jupyter nbconvert --to html", ["nbconvert"]),
    ("papermill", "papermill", "library", "packages", "Параметризация ноутбуков.", "pip install papermill", "papermill.execute_notebook()", ["papermill"]),
    ("prefect", "prefect", "library", "packages", "Оркестрация workflow.", "pip install prefect", "prefect.Flow()", ["prefect"]),
    ("airflow", "airflow", "library", "packages", "Оркестрация workflow.", "pip install apache-airflow", "airflow.models.DAG()", ["airflow"]),
    ("luigi", "luigi", "library", "packages", "Pipeline orchestration.", "pip install luigi", "luigi.Task()", ["luigi"]),
    ("dask", "dask", "library", "packages", "Параллельные вычисления.", "pip install dask", "dask.dataframe.read_csv()", ["dask"]),
    ("ray", "ray", "library", "packages", "Распределённые вычисления.", "pip install ray", "ray.init()", ["ray"]),
    ("modin", "modin", "library", "packages", "Быстрый pandas.", "pip install modin", "modin.pandas.DataFrame()", ["modin"]),
    ("vaex", "vaex", "library", "packages", "Большие данные.", "pip install vaex", "vaex.open('file.hdf5')", ["vaex"]),
    ("pyspark", "pyspark", "library", "packages", "Apache Spark.", "pip install pyspark", "pyspark.sql.SparkSession.builder.getOrCreate()", ["pyspark"]),
    ("delta-spark", "delta-spark", "library", "packages", "Delta Lake.", "pip install delta-spark", "delta.tables.DeltaTable.forPath()", ["delta"]),
    ("great-expectations", "great-expectations", "library", "packages", "Валидация данных.", "pip install great-expectations", "great_expectations.dataset.PandasDataset()", ["great_expectations"]),
    ("pandera", "pandera", "library", "packages", "Валидация pandas.", "pip install pandera", "pandera.DataFrameSchema()", ["pandera"]),
    ("pyarrow", "pyarrow", "library", "packages", "Apache Arrow.", "pip install pyarrow", "pyarrow.Table.from_pandas()", ["pyarrow"]),
    ("fastparquet", "fastparquet", "library", "packages", "Parquet файлы.", "pip install fastparquet", "fastparquet.ParquetFile()", ["fastparquet"]),
    ("geopandas", "geopandas", "library", "packages", "Геопространственные данные.", "pip install geopandas", "geopandas.GeoDataFrame()", ["geopandas"]),
    ("folium", "folium", "library", "packages", "Интерактивные карты.", "pip install folium", "folium.Map()", ["folium"]),
    ("shapely", "shapely", "library", "packages", "Геометрические объекты.", "pip install shapely", "shapely.geometry.Point()", ["shapely"]),
    ("fiona", "fiona", "library", "packages", "Чтение/запись геоданных.", "pip install fiona", "fiona.open('file.shp')", ["fiona"]),
    ("rasterio", "rasterio", "library", "packages", "Растровые данные.", "pip install rasterio", "rasterio.open('file.tif')", ["rasterio"]),
    ("networkx", "networkx", "library", "packages", "Графы и сети.", "pip install networkx", "networkx.Graph()", ["networkx"]),
    ("igraph", "igraph", "library", "packages", "Графы (быстрый).", "pip install python-igraph", "igraph.Graph()", ["igraph"]),
    ("scipy", "scipy", "library", "packages", "Научные вычисления.", "pip install scipy", "scipy.optimize.minimize()", ["scipy"]),
    ("statsmodels", "statsmodels", "library", "packages", "Статистика.", "pip install statsmodels", "statsmodels.api.OLS()", ["statsmodels"]),
    ("sympy", "sympy", "library", "packages", "Символьная математика.", "pip install sympy", "sympy.Symbol('x')", ["sympy"]),
    ("numpy", "numpy", "library", "packages", "Числовые вычисления.", "pip install numpy", "numpy.array()", ["numpy"]),
    ("jax", "jax", "library", "packages", "Дифференцируемое программирование.", "pip install jax", "jax.numpy.array()", ["jax"]),
    ("cupy", "cupy", "library", "packages", "GPU вычисления.", "pip install cupy-cuda11x", "cupy.array()", ["cupy"]),
    ("numba", "numba", "library", "packages", "JIT компиляция.", "pip install numba", "@numba.jit", ["numba"]),
    ("cython", "cython", "library", "packages", "C-расширения.", "pip install cython", "%%cython", ["cython"]),
    ("pybind11", "pybind11", "library", "packages", "C++ bindings.", "pip install pybind11", "pybind11.include()", ["pybind11"]),
    ("cffi", "cffi", "library", "packages", "C FFI.", "pip install cffi", "cffi.FFI()", ["cffi"]),
    ("swig", "swig", "library", "packages", "C/C++ bindings.", "swig -python", "swig -python -c++ interface.i", ["swig"]),
]


RELATED3 = {
    "__init__": {"alternatives": ["__new__"], "complements": ["__del__"], "seealso": ["__new__"]},
    "__str__": {"alternatives": ["__repr__"], "complements": ["print"], "seealso": ["__repr__"]},
    "__repr__": {"alternatives": ["__str__"], "complements": [], "seealso": ["__str__"]},
    "__len__": {"alternatives": [], "complements": ["len"], "seealso": ["len"]},
    "__getitem__": {"alternatives": [], "complements": ["__setitem__", "__delitem__"], "seealso": ["list", "dict"]},
    "__iter__": {"alternatives": [], "complements": ["__next__"], "seealso": ["for"]},
    "__contains__": {"alternatives": [], "complements": ["in"], "seealso": ["in"]},
    "__call__": {"alternatives": [], "complements": [], "seealso": ["def"]},
    "__enter__": {"alternatives": [], "complements": ["__exit__", "with"], "seealso": ["with"]},
    "__add__": {"alternatives": [], "complements": ["plus"], "seealso": ["plus"]},
    "__eq__": {"alternatives": [], "complements": ["equals"], "seealso": ["equals"]},
    "git-merge": {"alternatives": ["git-rebase"], "complements": ["git"], "seealso": ["git-rebase"]},
    "git-rebase": {"alternatives": ["git-merge"], "complements": ["git"], "seealso": ["git-merge"]},
    "git-stash": {"alternatives": [], "complements": ["git"], "seealso": ["git"]},
    "awk": {"alternatives": ["sed", "grep"], "complements": [], "seealso": ["sed"]},
    "sed": {"alternatives": ["awk", "grep"], "complements": [], "seealso": ["awk"]},
    "docker": {"alternatives": [], "complements": ["docker-compose"], "seealso": ["docker-compose"]},
    "kubernetes": {"alternatives": ["docker"], "complements": ["kubectl"], "seealso": ["docker"]},
    "celery": {"alternatives": ["rq", "dramatiq"], "complements": ["redis"], "seealso": ["rq"]},
    "rq": {"alternatives": ["celery", "dramatiq"], "complements": ["redis"], "seealso": ["celery"]},
    "fastapi": {"alternatives": ["flask", "django"], "complements": ["uvicorn", "pydantic"], "seealso": ["flask"]},
    "django": {"alternatives": ["flask", "fastapi"], "complements": ["django-rest-framework"], "seealso": ["flask"]},
    "flask": {"alternatives": ["fastapi", "django"], "complements": [], "seealso": ["fastapi"]},
    "sqlalchemy": {"alternatives": ["django-orm"], "complements": ["alembic"], "seealso": ["alembic"]},
    "pydantic": {"alternatives": ["marshmallow", "attrs"], "complements": ["fastapi"], "seealso": ["dataclasses"]},
    "redis": {"alternatives": ["memcached"], "complements": ["rq", "celery"], "seealso": ["rq"]},
    "postgresql": {"alternatives": ["mysql", "sqlite"], "complements": ["psycopg2"], "seealso": ["sqlite3"]},
    "mongodb": {"alternatives": ["postgresql"], "complements": ["pymongo", "motor"], "seealso": ["pymongo"]},
    "elasticsearch": {"alternatives": [], "complements": [], "seealso": []},
    "kafka": {"alternatives": ["rabbitmq"], "complements": ["kafka-python"], "seealso": ["pika"]},
    "rabbitmq": {"alternatives": ["kafka"], "complements": ["pika"], "seealso": ["kafka"]},
    "grpc": {"alternatives": ["rest"], "complements": ["protobuf"], "seealso": ["protobuf"]},
    "graphql": {"alternatives": ["rest"], "complements": ["graphene", "strawberry"], "seealso": ["graphene"]},
    "sentry": {"alternatives": [], "complements": ["sentry-sdk"], "seealso": []},
    "prometheus": {"alternatives": [], "complements": ["prometheus-client"], "seealso": []},
    "opentelemetry": {"alternatives": ["sentry", "prometheus"], "complements": [], "seealso": []},
    "jwt": {"alternatives": ["oauth"], "complements": ["pyjwt", "python-jose"], "seealso": ["oauth"]},
    "oauth": {"alternatives": ["jwt"], "complements": ["oauthlib", "authlib"], "seealso": ["jwt"]},
    "bcrypt": {"alternatives": ["passlib"], "complements": [], "seealso": ["passlib"]},
    "cryptography": {"alternatives": [], "complements": [], "seealso": []},
    "tensorflow": {"alternatives": ["pytorch", "jax"], "complements": ["keras"], "seealso": ["pytorch"]},
    "pytorch": {"alternatives": ["tensorflow", "jax"], "complements": [], "seealso": ["tensorflow"]},
    "jax": {"alternatives": ["tensorflow", "pytorch"], "complements": [], "seealso": ["tensorflow"]},
    "scikit-learn": {"alternatives": ["xgboost", "lightgbm"], "complements": [], "seealso": ["xgboost"]},
    "xgboost": {"alternatives": ["lightgbm", "catboost"], "complements": [], "seealso": ["lightgbm"]},
    "lightgbm": {"alternatives": ["xgboost", "catboost"], "complements": [], "seealso": ["xgboost"]},
    "catboost": {"alternatives": ["xgboost", "lightgbm"], "complements": [], "seealso": ["xgboost"]},
    "spacy": {"alternatives": ["nltk"], "complements": [], "seealso": ["nltk"]},
    "nltk": {"alternatives": ["spacy"], "complements": [], "seealso": ["spacy"]},
    "transformers": {"alternatives": [], "complements": ["datasets"], "seealso": ["datasets"]},
    "langchain": {"alternatives": ["llama-index"], "complements": ["openai", "anthropic"], "seealso": ["llama-index"]},
    "llama-index": {"alternatives": ["langchain"], "complements": [], "seealso": ["langchain"]},
    "openai": {"alternatives": ["anthropic", "google-generativeai"], "complements": [], "seealso": ["anthropic"]},
    "anthropic": {"alternatives": ["openai", "google-generativeai"], "complements": [], "seealso": ["openai"]},
    "streamlit": {"alternatives": ["gradio", "dash"], "complements": [], "seealso": ["gradio"]},
    "gradio": {"alternatives": ["streamlit"], "complements": [], "seealso": ["streamlit"]},
    "dash": {"alternatives": ["streamlit", "panel"], "complements": [], "seealso": ["streamlit"]},
    "airflow": {"alternatives": ["prefect", "luigi"], "complements": [], "seealso": ["prefect"]},
    "prefect": {"alternatives": ["airflow", "luigi"], "complements": [], "seealso": ["airflow"]},
    "dask": {"alternatives": ["ray", "pyspark"], "complements": [], "seealso": ["ray"]},
    "ray": {"alternatives": ["dask"], "complements": [], "seealso": ["dask"]},
    "pyspark": {"alternatives": ["dask", "ray"], "complements": ["delta-spark"], "seealso": ["dask"]},
    "pandas": {"alternatives": ["polars", "modin"], "complements": ["numpy"], "seealso": ["numpy"]},
    "numpy": {"alternatives": ["jax"], "complements": ["pandas", "scipy"], "seealso": ["pandas"]},
    "matplotlib": {"alternatives": ["plotly", "seaborn"], "complements": [], "seealso": ["plotly"]},
    "plotly": {"alternatives": ["matplotlib", "bokeh"], "complements": [], "seealso": ["matplotlib"]},
    "pillow": {"alternatives": ["opencv-python"], "complements": [], "seealso": ["opencv-python"]},
    "opencv-python": {"alternatives": ["pillow"], "complements": [], "seealso": ["pillow"]},
    "geopandas": {"alternatives": [], "complements": ["shapely", "folium"], "seealso": ["shapely"]},
    "networkx": {"alternatives": ["igraph"], "complements": [], "seealso": ["igraph"]},
    "scipy": {"alternatives": ["numpy"], "complements": ["numpy", "statsmodels"], "seealso": ["numpy"]},
    "statsmodels": {"alternatives": [], "complements": ["scipy"], "seealso": ["scipy"]},
    "sympy": {"alternatives": [], "complements": [], "seealso": []},
    "numba": {"alternatives": ["cython", "pybind11"], "complements": [], "seealso": ["cython"]},
    "cython": {"alternatives": ["numba", "pybind11"], "complements": [], "seealso": ["numba"]},
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
    ent = load(INPUT_PATHS)

    if ent is None:
        print("Сначала запусти build_all.py")
        return

    if isinstance(ent, list):
        ent = {"meta": {}, "entries": ent}

    entries = ent.get("entries", [])
    by_id = {e["id"]: e for e in entries if "id" in e}

    for item in NEW3:
        e = make_entry(item)
        if e["id"] not in by_id:
            by_id[e["id"]] = e

    ids = set(by_id)

    for e in by_id.values():
        rel = e.setdefault("related", {"alternatives": [], "complements": [], "seealso": []})

        extra = RELATED3.get(e["id"])
        if extra:
            for k in ["alternatives", "complements", "seealso"]:
                rel[k] = merge_list(rel.get(k, []), extra.get(k, []), ids)

    prepared = []
    for e in by_id.values():
        e["related"]["alternatives"] = e["related"]["alternatives"][:3]
        e["rank"] = e.get("rank", CATEGORY_DEFAULT_RANK.get(e.get("category"), 10000))
        prepared.append(e)

    prepared.sort(key=lambda x: (x.get("rank", 10000), x.get("name", "").lower()))
    ent["entries"] = prepared

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(ent, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Saved {len(prepared)} entries to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()