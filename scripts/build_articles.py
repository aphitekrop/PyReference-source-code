#!/usr/bin/env python3
import json
from pathlib import Path


OUTPUT_PATH = Path("data/articles.json")


def bi(ru, en):
    return {
        "ru": ru,
        "en": en
    }


def screenshot(note_ru, note_en, alt_ru="Скриншот", alt_en="Screenshot"):
    return {
        "src": None,
        "alt": bi(alt_ru, alt_en),
        "note": bi(note_ru, note_en)
    }


ARTICLES = [
    {
        "id": "venv",
        "title": bi("Как создать виртуальное окружение", "How to create a virtual environment"),
        "summary": bi("Создание изолированного окружения Python для проекта.", "Create an isolated Python environment for a project."),
        "category": "environment",
        "tags": ["venv", "pip"],
        "rank": 10,
        "updated": "2026-02-14",
        "intro": [
            bi("Виртуальное окружение устанавливает библиотеки отдельно для каждого проекта.", "A virtual environment installs libraries separately for each project.")
        ],
        "links": [
            {
                "title": bi("Документация venv", "venv documentation"),
                "url": "https://docs.python.org/3/library/venv.html"
            }
        ],
        "steps": [
            {
                "title": bi("Открой терминал в папке проекта", "Open a terminal in the project folder"),
                "text": bi("Перейди в папку проекта.", "Go to the project folder."),
                "code": "cd my_project",
                "screenshot": screenshot("Терминал открыт в папке проекта.", "Terminal opened in the project folder.")
            },
            {
                "title": bi("Создай окружение", "Create the environment"),
                "text": bi("Команда создаст папку .venv.", "The command creates the .venv folder."),
                "code": "python -m venv .venv",
                "screenshot": screenshot("Создание виртуального окружения.", "Creating the virtual environment.")
            },
            {
                "title": bi("Активируй окружение в Windows", "Activate on Windows"),
                "text": bi("Используй activate из папки Scripts.", "Use activate from the Scripts folder."),
                "code": ".venv\\Scripts\\activate"
            },
            {
                "title": bi("Активируй окружение в Linux/macOS", "Activate on Linux/macOS"),
                "text": bi("Используй source.", "Use source."),
                "code": "source .venv/bin/activate",
                "screenshot": screenshot("Активированное окружение.", "Activated environment.")
            },
            {
                "title": bi("Выйди из окружения", "Deactivate"),
                "text": bi("Когда работа закончена.", "When you are done."),
                "code": "deactivate"
            }
        ],
        "images": []
    },
    {
        "id": "install-library",
        "title": bi("Как установить библиотеку", "How to install a library"),
        "summary": bi("Установка библиотеки через pip.", "Install a library with pip."),
        "category": "environment",
        "tags": ["pip", "библиотеки"],
        "rank": 20,
        "updated": "2026-02-14",
        "intro": [
            bi("Библиотеки устанавливаются через pip внутри окружения.", "Libraries are installed with pip inside the environment.")
        ],
        "links": [
            {
                "title": bi("pip install", "pip install"),
                "url": "https://pip.pypa.io/en/stable/cli/pip_install/"
            }
        ],
        "steps": [
            {
                "title": bi("Установи библиотеку", "Install the library"),
                "text": bi("Например, requests.", "For example, requests."),
                "code": "python -m pip install requests",
                "screenshot": screenshot("Установка requests.", "Installing requests.")
            },
            {
                "title": bi("Проверь установку", "Verify installation"),
                "text": bi("pip show показывает информацию о пакете.", "pip show prints package info."),
                "code": "python -m pip show requests",
                "screenshot": screenshot("Вывод pip show requests.", "pip show requests output.")
            },
            {
                "title": bi("Проверь импорт", "Check import"),
                "text": bi("Библиотека должна импортироваться.", "The library should import."),
                "code": "python -c \"import requests; print(requests.__version__)\""
            }
        ],
        "images": []
    },
    {
        "id": "save-dependencies",
        "title": bi("Как сохранить зависимости", "How to save dependencies"),
        "summary": bi("Сохранение библиотек в requirements.txt.", "Save libraries to requirements.txt."),
        "category": "environment",
        "tags": ["pip", "requirements"],
        "rank": 30,
        "updated": "2026-02-14",
        "intro": [
            bi("requirements.txt позволяет восстановить те же библиотеки.", "requirements.txt lets you restore the same libraries.")
        ],
        "links": [
            {
                "title": bi("pip freeze", "pip freeze"),
                "url": "https://pip.pypa.io/en/stable/cli/pip_freeze/"
            }
        ],
        "steps": [
            {
                "title": bi("Создай requirements.txt", "Create requirements.txt"),
                "text": bi("Сохраняет список пакетов.", "Saves the package list."),
                "code": "python -m pip freeze > requirements.txt",
                "screenshot": screenshot("Файл requirements.txt создан.", "requirements.txt created.")
            },
            {
                "title": bi("Установи зависимости из файла", "Install from the file"),
                "text": bi("На другой машине.", "On another machine."),
                "code": "python -m pip install -r requirements.txt",
                "screenshot": screenshot("Установка зависимостей.", "Installing dependencies.")
            }
        ],
        "images": []
    },
    {
        "id": "run-server",
        "title": bi("Как запустить сервер", "How to run a server"),
        "summary": bi("Локальный HTTP-сервер для файлов.", "Local HTTP server for files."),
        "category": "web",
        "tags": ["server", "http"],
        "rank": 40,
        "updated": "2026-02-14",
        "intro": [
            bi("Python умеет запускать простой сервер без установки программ.", "Python can run a simple server with no extra tools.")
        ],
        "links": [
            {
                "title": bi("http.server", "http.server"),
                "url": "https://docs.python.org/3/library/http.server.html"
            }
        ],
        "steps": [
            {
                "title": bi("Запусти сервер", "Start the server"),
                "text": bi("По умолчанию порт 8000.", "Default port is 8000."),
                "code": "python -m http.server 8000",
                "screenshot": screenshot("Запуск сервера.", "Server started.")
            },
            {
                "title": bi("Открой в браузере", "Open in browser"),
                "text": bi("Перейди на localhost.", "Go to localhost."),
                "code": "http://localhost:8000",
                "screenshot": screenshot("Открытый локальный сайт.", "Local site opened.")
            },
            {
                "title": bi("Останови сервер", "Stop the server"),
                "text": bi("Нажми Ctrl + C в терминале.", "Press Ctrl + C in the terminal."),
                "code": "Ctrl + C"
            }
        ],
        "images": []
    },
    {
        "id": "download-file",
        "title": bi("Как скачать файл", "How to download a file"),
        "summary": bi("Скачивание через curl, wget и Python.", "Download with curl, wget and Python."),
        "category": "network",
        "tags": ["curl", "wget", "requests"],
        "rank": 50,
        "updated": "2026-02-14",
        "intro": [
            bi("Файл можно скачать из терминала или из кода.", "A file can be downloaded from the terminal or from code.")
        ],
        "links": [
            {
                "title": bi("curl", "curl"),
                "url": "https://curl.se/"
            },
            {
                "title": bi("requests", "requests"),
                "url": "https://docs.python-requests.org/"
            }
        ],
        "steps": [
            {
                "title": bi("Скачать через curl", "Download with curl"),
                "text": bi("-O сохраняет имя файла.", "-O keeps the file name."),
                "code": "curl -O https://example.com/file.txt",
                "screenshot": screenshot("Скачивание через curl.", "Downloading with curl.")
            },
            {
                "title": bi("Скачать через wget", "Download with wget"),
                "text": bi("wget тоже сохраняет файл.", "wget also saves the file."),
                "code": "wget https://example.com/file.txt"
            },
            {
                "title": bi("Скачать через requests", "Download with requests"),
                "text": bi("Пример на Python.", "Python example."),
                "code": "import requests\n\nresponse = requests.get('https://example.com/file.txt')\n\nwith open('file.txt', 'wb') as f:\n    f.write(response.content)",
                "screenshot": screenshot("Python-код скачивания.", "Python download code.")
            }
        ],
        "images": []
    },
    {
        "id": "handle-error",
        "title": bi("Как обработать ошибку", "How to handle an error"),
        "summary": bi("Использование try, except, else и finally.", "Using try, except, else and finally."),
        "category": "core",
        "tags": ["try", "except"],
        "rank": 60,
        "updated": "2026-02-14",
        "intro": [
            bi("Обработка ошибок не даёт программе падать.", "Error handling keeps the program from crashing.")
        ],
        "links": [
            {
                "title": bi("Ошибки и исключения", "Errors and exceptions"),
                "url": "https://docs.python.org/3/tutorial/errors.html"
            }
        ],
        "steps": [
            {
                "title": bi("Базовый try/except", "Basic try/except"),
                "text": bi("except выполняется при ошибке.", "except runs on error."),
                "code": "try:\n    number = int('abc')\nexcept ValueError:\n    print('Это не число')",
                "screenshot": screenshot("Работа try/except.", "try/except in action.")
            },
            {
                "title": bi("Конкретная ошибка", "Specific error"),
                "text": bi("Лови конкретный тип ошибки.", "Catch a specific error type."),
                "code": "try:\n    file = open('missing.txt', encoding='utf-8')\nexcept FileNotFoundError:\n    print('Файл не найден')"
            },
            {
                "title": bi("else и finally", "else and finally"),
                "text": bi("else — если ошибки не было, finally — всегда.", "else — when no error, finally — always."),
                "code": "try:\n    x = 10 / 2\nexcept ZeroDivisionError:\n    print('Деление на ноль')\nelse:\n    print('Ошибок нет')\nfinally:\n    print('Выполняется всегда')"
            }
        ],
        "images": []
    },
    {
        "id": "read-json",
        "title": bi("Как прочитать JSON", "How to read JSON"),
        "summary": bi("Чтение JSON из файла, строки и HTTP.", "Read JSON from a file, string and HTTP."),
        "category": "data",
        "tags": ["json"],
        "rank": 70,
        "updated": "2026-02-14",
        "intro": [
            bi("В Python есть встроенный модуль json.", "Python has a built-in json module.")
        ],
        "links": [
            {
                "title": bi("Модуль json", "json module"),
                "url": "https://docs.python.org/3/library/json.html"
            }
        ],
        "steps": [
            {
                "title": bi("Из файла", "From a file"),
                "text": bi("Используй json.load().", "Use json.load()."),
                "code": "import json\n\nwith open('data.json', encoding='utf-8') as f:\n    data = json.load(f)\n\nprint(data)",
                "screenshot": screenshot("Чтение JSON из файла.", "Reading JSON from a file.")
            },
            {
                "title": bi("Из строки", "From a string"),
                "text": bi("Используй json.loads().", "Use json.loads()."),
                "code": "import json\n\ntext = '{\"name\": \"Alice\"}'\ndata = json.loads(text)\n\nprint(data['name'])"
            },
            {
                "title": bi("Из HTTP-ответа", "From an HTTP response"),
                "text": bi("requests: response.json().", "requests: response.json()."),
                "code": "import requests\n\nresponse = requests.get('https://api.example.com/data')\ndata = response.json()"
            }
        ],
        "images": []
    },
    {
        "id": "write-csv",
        "title": bi("Как записать CSV", "How to write CSV"),
        "summary": bi("Запись таблиц через модуль csv.", "Write tables with the csv module."),
        "category": "data",
        "tags": ["csv", "файлы"],
        "rank": 80,
        "updated": "2026-02-14",
        "intro": [
            bi("CSV — простой табличный формат.", "CSV is a simple table format.")
        ],
        "links": [
            {
                "title": bi("Модуль csv", "csv module"),
                "url": "https://docs.python.org/3/library/csv.html"
            }
        ],
        "steps": [
            {
                "title": bi("Записать список списков", "Write a list of lists"),
                "text": bi("Каждый список — строка таблицы.", "Each list is a table row."),
                "code": "import csv\n\nrows = [\n    ['name', 'age'],\n    ['Alice', 30],\n    ['Bob', 25]\n]\n\nwith open('people.csv', 'w', encoding='utf-8', newline='') as f:\n    csv.writer(f).writerows(rows)",
                "screenshot": screenshot("Запись CSV.", "Writing CSV.")
            },
            {
                "title": bi("Записать словари", "Write dictionaries"),
                "text": bi("DictWriter удобен для словарей.", "DictWriter is handy for dicts."),
                "code": "import csv\n\npeople = [\n    {'name': 'Alice', 'age': 30},\n    {'name': 'Bob', 'age': 25}\n]\n\nwith open('people.csv', 'w', encoding='utf-8', newline='') as f:\n    writer = csv.DictWriter(f, fieldnames=['name', 'age'])\n    writer.writeheader()\n    writer.writerows(people)"
            }
        ],
        "images": []
    },
    {
        "id": "create-project",
        "title": bi("Как создать проект", "How to create a project"),
        "summary": bi("Пошаговое создание нового Python-проекта.", "Step-by-step creation of a new Python project."),
        "category": "environment",
        "tags": ["проект", "project"],
        "rank": 90,
        "updated": "2026-02-14",
        "intro": [
            bi("Проект начинается с папки, окружения и главного файла.", "A project starts with a folder, an environment and a main file.")
        ],
        "links": [
            {
                "title": bi("Документация venv", "venv documentation"),
                "url": "https://docs.python.org/3/library/venv.html"
            }
        ],
        "steps": [
            {
                "title": bi("Создай папку проекта", "Create the project folder"),
                "text": bi("И перейди в неё.", "And go into it."),
                "code": "mkdir my_project\ncd my_project",
                "screenshot": screenshot("Создание папки проекта.", "Creating the project folder.")
            },
            {
                "title": bi("Создай окружение", "Create the environment"),
                "text": bi("И активируй его.", "And activate it."),
                "code": "python -m venv .venv\n.venv\\Scripts\\activate"
            },
            {
                "title": bi("Создай main.py", "Create main.py"),
                "text": bi("Первый файл проекта.", "The first project file."),
                "code": "print('Hello, project!')",
                "screenshot": screenshot("Файл main.py в редакторе.", "main.py in the editor.")
            },
            {
                "title": bi("Запусти проект", "Run the project"),
                "text": bi("Выполни файл.", "Run the file."),
                "code": "python main.py",
                "screenshot": screenshot("Запуск main.py.", "Running main.py.")
            }
        ],
        "images": []
    },
    {
        "id": "install-flask",
        "title": bi("Как установить Flask", "How to install Flask"),
        "summary": bi("Установка Flask и первый веб-сервер.", "Install Flask and run a first web server."),
        "category": "web",
        "tags": ["flask", "web"],
        "rank": 100,
        "updated": "2026-02-14",
        "intro": [
            bi("Flask — лёгкий веб-фреймворк.", "Flask is a lightweight web framework.")
        ],
        "links": [
            {
                "title": bi("Документация Flask", "Flask documentation"),
                "url": "https://flask.palletsprojects.com/"
            }
        ],
        "steps": [
            {
                "title": bi("Установи Flask", "Install Flask"),
                "text": bi("Внутри виртуального окружения.", "Inside the virtual environment."),
                "code": "python -m pip install flask",
                "screenshot": screenshot("Установка Flask.", "Installing Flask.")
            },
            {
                "title": bi("Создай app.py", "Create app.py"),
                "text": bi("Минимальное приложение.", "Minimal app."),
                "code": "from flask import Flask\n\napp = Flask(__name__)\n\n@app.route('/')\ndef hello():\n    return 'Hello, Flask!'",
                "screenshot": screenshot("Код app.py.", "app.py code.")
            },
            {
                "title": bi("Запусти сервер", "Run the server"),
                "text": bi("Запуск Flask.", "Run Flask."),
                "code": "flask --app app run"
            },
            {
                "title": bi("Открой сайт", "Open the site"),
                "text": bi("По умолчанию порт 5000.", "Default port is 5000."),
                "code": "http://127.0.0.1:5000",
                "screenshot": screenshot("Страница Hello, Flask!.", "Hello, Flask! page.")
            }
        ],
        "images": []
    },
    {
        "id": "install-fastapi",
        "title": bi("Как установить FastAPI", "How to install FastAPI"),
        "summary": bi("Установка FastAPI и запуск API.", "Install FastAPI and run an API."),
        "category": "web",
        "tags": ["fastapi", "api"],
        "rank": 110,
        "updated": "2026-02-14",
        "intro": [
            bi("FastAPI — современный фреймворк для API.", "FastAPI is a modern API framework.")
        ],
        "links": [
            {
                "title": bi("Документация FastAPI", "FastAPI documentation"),
                "url": "https://fastapi.tiangolo.com/"
            }
        ],
        "steps": [
            {
                "title": bi("Установи FastAPI и uvicorn", "Install FastAPI and uvicorn"),
                "text": bi("uvicorn — сервер для запуска.", "uvicorn is the runtime server."),
                "code": "python -m pip install fastapi uvicorn",
                "screenshot": screenshot("Установка FastAPI.", "Installing FastAPI.")
            },
            {
                "title": bi("Создай main.py", "Create main.py"),
                "text": bi("Минимальный API.", "Minimal API."),
                "code": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef hello():\n    return {'message': 'Hello, FastAPI!'}"
            },
            {
                "title": bi("Запусти сервер", "Run the server"),
                "text": bi("С автоперезагрузкой.", "With auto-reload."),
                "code": "uvicorn main:app --reload",
                "screenshot": screenshot("Запуск uvicorn.", "Running uvicorn.")
            },
            {
                "title": bi("Открой документацию", "Open the docs"),
                "text": bi("FastAPI даёт документацию автоматически.", "FastAPI provides docs automatically."),
                "code": "http://127.0.0.1:8000/docs",
                "screenshot": screenshot("Swagger-документация.", "Swagger docs.")
            }
        ],
        "images": []
    },
    {
        "id": "github",
        "title": bi("Как работать с GitHub", "How to work with GitHub"),
        "summary": bi("Подключение проекта к GitHub и отправка кода.", "Connect a project to GitHub and push code."),
        "category": "dev-tools",
        "tags": ["git", "github"],
        "rank": 120,
        "updated": "2026-02-14",
        "intro": [
            bi("GitHub хранит код и историю изменений.", "GitHub stores code and its history.")
        ],
        "links": [
            {
                "title": bi("Документация Git", "Git documentation"),
                "url": "https://git-scm.com/doc"
            },
            {
                "title": bi("GitHub", "GitHub"),
                "url": "https://github.com/"
            }
        ],
        "steps": [
            {
                "title": bi("Настрой Git", "Configure Git"),
                "text": bi("Укажи имя и email.", "Set your name and email."),
                "code": "git config --global user.name 'Your Name'\ngit config --global user.email 'you@example.com'",
                "screenshot": screenshot("Настройка git config.", "git config setup.")
            },
            {
                "title": bi("Создай репозиторий на GitHub", "Create a GitHub repository"),
                "text": bi("Создай пустой репозиторий на сайте.", "Create an empty repository on the site."),
                "screenshot": screenshot("Страница создания репозитория.", "Repository creation page.")
            },
            {
                "title": bi("Свяжи проект с GitHub", "Link the project to GitHub"),
                "text": bi("Инициализация и первый коммит.", "Init and first commit."),
                "code": "git init\ngit add .\ngit commit -m 'first commit'\ngit branch -M main\ngit remote add origin https://github.com/USER/REPO.git"
            },
            {
                "title": bi("Отправь код", "Push the code"),
                "text": bi("Первая отправка на GitHub.", "First push to GitHub."),
                "code": "git push -u origin main",
                "screenshot": screenshot("Код на GitHub.", "Code on GitHub.")
            }
        ],
        "images": []
    },
    {
        "id": "git-commit",
        "title": bi("Как сделать git commit", "How to make a git commit"),
        "summary": bi("Сохранение изменений в истории Git.", "Save changes to Git history."),
        "category": "dev-tools",
        "tags": ["git", "commit"],
        "rank": 130,
        "updated": "2026-02-14",
        "intro": [
            bi("Коммит — это снимок изменений проекта.", "A commit is a snapshot of project changes.")
        ],
        "links": [
            {
                "title": bi("git commit", "git commit"),
                "url": "https://git-scm.com/docs/git-commit"
            }
        ],
        "steps": [
            {
                "title": bi("Посмотри изменения", "See changes"),
                "text": bi("git status показывает изменённые файлы.", "git status shows modified files."),
                "code": "git status",
                "screenshot": screenshot("Вывод git status.", "git status output.")
            },
            {
                "title": bi("Добавь файлы", "Stage files"),
                "text": bi("Добавь все изменения.", "Stage all changes."),
                "code": "git add ."
            },
            {
                "title": bi("Сделай коммит", "Commit"),
                "text": bi("Опиши изменение.", "Describe the change."),
                "code": "git commit -m 'Добавлен main.py'",
                "screenshot": screenshot("Вывод git commit.", "git commit output.")
            },
            {
                "title": bi("Отправь на GitHub", "Push to GitHub"),
                "text": bi("Если есть удалённый репозиторий.", "If a remote exists."),
                "code": "git push"
            }
        ],
        "images": []
    },
    {
        "id": "http-request",
        "title": bi("Как отправить HTTP-запрос", "How to send an HTTP request"),
        "summary": bi("GET и POST запросы через requests.", "GET and POST requests with requests."),
        "category": "network",
        "tags": ["requests", "http", "api"],
        "rank": 140,
        "updated": "2026-02-14",
        "intro": [
            bi("requests — самый удобный способ делать HTTP-запросы.", "requests is the most convenient way to make HTTP requests.")
        ],
        "links": [
            {
                "title": bi("Документация requests", "requests documentation"),
                "url": "https://docs.python-requests.org/"
            }
        ],
        "steps": [
            {
                "title": bi("GET-запрос", "GET request"),
                "text": bi("Получение данных.", "Fetching data."),
                "code": "import requests\n\nresponse = requests.get('https://api.example.com/data')\nprint(response.status_code)\nprint(response.json())",
                "screenshot": screenshot("GET-запрос и ответ.", "GET request and response.")
            },
            {
                "title": bi("GET с параметрами", "GET with params"),
                "text": bi("Параметры передаются в URL.", "Params go into the URL."),
                "code": "params = {'q': 'python'}\nresponse = requests.get('https://api.example.com/search', params=params)"
            },
            {
                "title": bi("POST с JSON", "POST with JSON"),
                "text": bi("Отправка данных.", "Sending data."),
                "code": "payload = {'name': 'Alice'}\nresponse = requests.post('https://api.example.com/users', json=payload)",
                "screenshot": screenshot("POST-запрос.", "POST request.")
            }
        ],
        "images": []
    },
    {
        "id": "telegram-bot",
        "title": bi("Как создать Telegram-бота", "How to create a Telegram bot"),
        "summary": bi("Простой бот на pyTelegramBotAPI.", "A simple bot with pyTelegramBotAPI."),
        "category": "bots",
        "tags": ["telegram", "bot"],
        "rank": 150,
        "updated": "2026-02-14",
        "intro": [
            bi("Бот создаётся через BotFather и управляется токеном.", "A bot is created via BotFather and controlled by a token.")
        ],
        "links": [
            {
                "title": bi("BotFather", "BotFather"),
                "url": "https://t.me/BotFather"
            },
            {
                "title": bi("pyTelegramBotAPI", "pyTelegramBotAPI"),
                "url": "https://github.com/eternnoir/pyTelegramBotAPI"
            }
        ],
        "steps": [
            {
                "title": bi("Создай бота в BotFather", "Create a bot in BotFather"),
                "text": bi("Команда /newbot даёт токен.", "The /newbot command gives a token."),
                "screenshot": screenshot("Диалог с BotFather и токен.", "BotFather dialog and token.")
            },
            {
                "title": bi("Установи библиотеку", "Install the library"),
                "text": bi("pyTelegramBotAPI.", "pyTelegramBotAPI."),
                "code": "python -m pip install pyTelegramBotAPI"
            },
            {
                "title": bi("Создай bot.py", "Create bot.py"),
                "text": bi("Вставь свой токен вместо TOKEN.", "Replace TOKEN with your token."),
                "code": "import telebot\n\nbot = telebot.TeleBot('TOKEN')\n\n@bot.message_handler(commands=['start'])\ndef start(message):\n    bot.reply_to(message, 'Hello!')\n\nbot.infinity_polling()",
                "screenshot": screenshot("Код bot.py.", "bot.py code.")
            },
            {
                "title": bi("Запусти бота", "Run the bot"),
                "text": bi("Бот начнёт отвечать в Telegram.", "The bot starts replying in Telegram."),
                "code": "python bot.py",
                "screenshot": screenshot("Ответ бота в Telegram.", "Bot reply in Telegram.")
            }
        ],
        "images": []
    },
    {
        "id": "sqlite",
        "title": bi("Как работать с базой SQLite", "How to work with a SQLite database"),
        "summary": bi("Создание таблицы, запись и чтение данных.", "Create a table, insert and read data."),
        "category": "data",
        "tags": ["sqlite", "база"],
        "rank": 160,
        "updated": "2026-02-14",
        "intro": [
            bi("SQLite — встроенная база данных, не требующая сервера.", "SQLite is a built-in serverless database.")
        ],
        "links": [
            {
                "title": bi("Модуль sqlite3", "sqlite3 module"),
                "url": "https://docs.python.org/3/library/sqlite3.html"
            }
        ],
        "steps": [
            {
                "title": bi("Создай таблицу", "Create a table"),
                "text": bi("Подключение и создание таблицы.", "Connect and create a table."),
                "code": "import sqlite3\n\nconn = sqlite3.connect('app.db')\ncursor = conn.cursor()\n\ncursor.execute('''\nCREATE TABLE IF NOT EXISTS users (\n    id INTEGER PRIMARY KEY,\n    name TEXT\n)\n''')\nconn.commit()",
                "screenshot": screenshot("Создание таблицы users.", "Creating the users table.")
            },
            {
                "title": bi("Добавь данные", "Insert data"),
                "text": bi("Используй параметры ?.", "Use ? placeholders."),
                "code": "cursor.execute(\"INSERT INTO users (name) VALUES (?)\", ('Alice',))\nconn.commit()"
            },
            {
                "title": bi("Прочитай данные", "Read data"),
                "text": bi("SELECT возвращает строки.", "SELECT returns rows."),
                "code": "cursor.execute(\"SELECT id, name FROM users\")\nprint(cursor.fetchall())",
                "screenshot": screenshot("Вывод данных из базы.", "Data output from the database.")
            },
            {
                "title": bi("Закрой соединение", "Close the connection"),
                "text": bi("Всегда закрывай соединение.", "Always close the connection."),
                "code": "conn.close()"
            }
        ],
        "images": []
    },
    {
        "id": "logging",
        "title": bi("Как логировать ошибки", "How to log errors"),
        "summary": bi("Логирование в консоль и файл.", "Logging to console and file."),
        "category": "core",
        "tags": ["logging", "ошибки"],
        "rank": 170,
        "updated": "2026-02-14",
        "intro": [
            bi("logging лучше, чем print, для отслеживания работы программы.", "logging is better than print for tracking program behavior.")
        ],
        "links": [
            {
                "title": bi("Модуль logging", "logging module"),
                "url": "https://docs.python.org/3/library/logging.html"
            }
        ],
        "steps": [
            {
                "title": bi("Базовая настройка", "Basic setup"),
                "text": bi("Уровни: info, warning, error.", "Levels: info, warning, error."),
                "code": "import logging\n\nlogging.basicConfig(\n    level=logging.INFO,\n    format='%(asctime)s %(levelname)s %(message)s'\n)\n\nlogging.info('Старт')\nlogging.warning('Предупреждение')\nlogging.error('Ошибка')",
                "screenshot": screenshot("Вывод логов в консоль.", "Console log output.")
            },
            {
                "title": bi("Логируй исключения", "Log exceptions"),
                "text": bi("logging.exception пишет текст ошибки.", "logging.exception writes the error text."),
                "code": "try:\n    1 / 0\nexcept ZeroDivisionError:\n    logging.exception('Ошибка деления')"
            },
            {
                "title": bi("Запись в файл", "Write to a file"),
                "text": bi("Логи сохраняются в app.log.", "Logs are saved to app.log."),
                "code": "logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.INFO)",
                "screenshot": screenshot("Файл app.log с логами.", "app.log file with logs.")
            }
        ],
        "images": []
    },
    {
        "id": "tests",
        "title": bi("Как запускать тесты", "How to run tests"),
        "summary": bi("Простые тесты с pytest.", "Simple tests with pytest."),
        "category": "testing",
        "tags": ["pytest", "тесты"],
        "rank": 180,
        "updated": "2026-02-14",
        "intro": [
            bi("Тесты проверяют, что код работает как ожидается.", "Tests verify that code works as expected.")
        ],
        "links": [
            {
                "title": bi("Документация pytest", "pytest documentation"),
                "url": "https://docs.pytest.org/"
            }
        ],
        "steps": [
            {
                "title": bi("Установи pytest", "Install pytest"),
                "text": bi("Внутри окружения.", "Inside the environment."),
                "code": "python -m pip install pytest",
                "screenshot": screenshot("Установка pytest.", "Installing pytest.")
            },
            {
                "title": bi("Создай test_app.py", "Create test_app.py"),
                "text": bi("Имя файла должно начинаться с test_.", "The file name must start with test_."),
                "code": "def add(a, b):\n    return a + b\n\ndef test_add():\n    assert add(2, 2) == 4",
                "screenshot": screenshot("Код test_app.py.", "test_app.py code.")
            },
            {
                "title": bi("Запусти тесты", "Run tests"),
                "text": bi("pytest найдёт все test_-файлы.", "pytest finds all test_ files."),
                "code": "pytest",
                "screenshot": screenshot("Результат запуска pytest.", "pytest run result.")
            },
            {
                "title": bi("Подробный вывод", "Verbose output"),
                "text": bi("Флаг -v показывает детали.", "The -v flag shows details."),
                "code": "pytest -v"
            }
        ],
        "images": []
    }
]


def main():
    payload = {
        "meta": {
            "version": 2,
            "sectionTitle": {
                "ru": "Полезные статьи",
                "en": "Useful articles"
            }
        },
        "articles": ARTICLES
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Saved {len(payload['articles'])} articles to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()