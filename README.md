Структура проекта

├── database
│   ├── __init__.py
│   ├── models.py             # Модели и функции взаимодествий с БД
│   └── __pycache__           # Скомпилированные байткоды Python
│       ├── __init__.cpython-310.pyc
│       └── models.cpython-310.pyc
├── data.py                   # Работа с данными
├── docker-compose.yml        # Конфигурация Docker Compose
├── dockerfile                # Файл конфигурации Docker
├── file                      # Папка для файлов
│   └── __init__.py
├── function                  # Функции для роутев
│   ├── function_out.py
│   ├── __init__.py
│   └── __pycache__
│       ├── function_out.cpython-310.pyc
│       └── __init__.cpython-310.pyc
├── __init__.py               # Инициализация пакета
├── main.py                   # Главный файл запуска приложения
├── nginx.conf                # Конфигурационный файл Nginx
├── __pycache__               # Скомпилированные байткоды Python
│   └── main.cpython-310.pyc
├── pytest.ini                # Настройки Pytest
├── reg.txt                   # Файл регистрации
├── shema                     # Схемы данных
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   └── shema.cpython-310.pyc
│   └── shema.py              # Схемы пандастика
├── static                    # Статические файлы (CSS, JS)
│   ├── css
│   ├── favicon.ico
│   └── js
├── templates                 # HTML-шаблоны
│   └── index.html
├── test                      # Тесты
│   ├── confest.py            # Конфигурационные тесты
│   ├── func.py               # Функции дляя некоторых фикстуров
│   ├── __init__.py
│   ├── rengoku.jpg           # Изображение для тестов
│   └── test_fastapi.py       # Тесты для FastAPI
├── test_datadb.py            # Тесты базы данных
└── Итоговый проект «Python Advanced».pdf  # PDF-файл с описанием проекта

Запуск проекта

Для запуска проекта необходимо выполнить следующие шаги:

    Установить зависимости:

pip install -r reg.txt

Запустить приложение:

uvicorn main:app --reload

Открыть браузер и перейти по адресу http://localhost:8000.


для развортывание через контейнер ввести команду docker-compose up -d
