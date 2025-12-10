# Intensive-Bot

Telethon-бот с реальным съёмом сообщений, SQLite и асинхронными датчиками событий для клиента Telegram.

## Функционал

- ✅ Асинхронное подключение к Telegram на Telethon
- ✅ Получение списка доступных диалогов
- ✅ Сбор последних N сообщений из выбранного чата
- ✅ Live-слушатель новых сообщений в реальном времени
- ✅ Автоматическое объявление ошибок и переподключение
- ✅ Комплексное логирование
- ✅ SQLite база данных для сохранения сообщений
- ✅ Проверка дублей по id сообщения

## Установка

### 1. Клонирование
```bash
git clone https://github.com/AIzotov093/Intensive-Bot.git
cd Intensive-Bot
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Конфигурация
Откройте `config.py` и вставьте свои значения:

```python
api_id = YOUR_API_ID  # ваш api_id из https://my.telegram.org
api_hash = "YOUR_API_HASH"  # ваш api_hash
session_name = "telegram_session"  # имя session файла
```

## Наполнение

```bash
python main.py
```

Пы будете просинден ввести ПИН-код для линиц с рассылкой к эТ коду. По вводу пин-кода бот начнёт скачивать сообщения и странслит их в SQLite базе.

## Структура файлов

```
Intensive-Bot/
├── main.py           # Основной асинхронный клиент
├── config.py           # Конфигурация (api_id, api_hash)
├── db.py              # Модуль работы с SQLite
├── requirements.txt    # При висимостем (telethon)
├── messages.db         # SQLite база (генерируется автоматически)
└── README.md           # Эта документация
```

## Пример вывода

```
[My Chat] username: Hello, world!
[Мой траня дю] contact_name: Это сообщение было сорхранено...
```

