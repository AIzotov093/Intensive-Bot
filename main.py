# main.py
import asyncio
import logging
from typing import List, Optional
from telethon import TelegramClient, events
from telethon.errors import RPCError
from telethon.tl.custom import Dialog, Message
import config
from db import init_db, save_message

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

async def list_dialogs(client: TelegramClient) -> List[Dialog]:
    dialogs = []
    logger.info("Запрос списка диалогов...")
    async for dialog in client.iter_dialogs():
        dialogs.append(dialog)
        logger.info("ID=%s | title=%s", dialog.id, dialog.name)
    return dialogs

async def fetch_last_messages(client: TelegramClient, dialog: Dialog, limit: int = 100) -> None:
    logger.info("Сбор последних %s сообщений", limit)
    async for message in client.iter_messages(dialog.entity, limit=limit):
        await process_and_save_message(message, dialog.name)

async def process_and_save_message(message: Message, chat_title: str) -> None:
    if not message:
        return
    msg_id = message.id
    chat_id = message.chat_id or 0
    sender = None
    try:
        if message.sender:
            sender = getattr(message.sender, "username", None) or getattr(message.sender, "first_name", None)
    except AttributeError:
        sender = None
    text = message.message or ""
    date_str = message.date.isoformat() if message.date else ""
    save_message(msg_id, chat_id, sender, text, date_str)
    short_text = text.replace("\n", " ")
    if len(short_text) > 60:
        short_text = short_text[:57] + "..."
    print(f"[{chat_title}] {sender}: {short_text}")

def register_handlers(client: TelegramClient) -> None:
    @client.on(events.NewMessage)
    async def new_message_handler(event: events.NewMessage.Event) -> None:
        try:
            message = event.message
            chat = await event.get_chat()
            chat_title = getattr(chat, "title", None) or getattr(chat, "username", "Unknown")
            await process_and_save_message(message, chat_title)
        except Exception as e:
            logger.exception("Ошибка: %s", e)

async def run_client() -> None:
    init_db()
    client = TelegramClient(config.session_name, config.api_id, config.api_hash)
    while True:
        try:
            logger.info("Запуск TelegramClient...")
            async with client:
                register_handlers(client)
                dialogs = await list_dialogs(client)
                if not dialogs:
                    logger.warning("Нет диалогов")
                    return
                chosen_dialog = dialogs[0]
                logger.info("Выбран: %s (%s)", chosen_dialog.name, chosen_dialog.id)
                await fetch_last_messages(client, chosen_dialog, limit=100)
                logger.info("Начало live-слушания")
                await client.run_until_disconnected()
        except (ConnectionError, RPCError) as e:
            logger.warning("Ошибка соединения (%s). Повтор...", e)
            await asyncio.sleep(5)
            continue
        except KeyboardInterrupt:
            logger.info("Остановка")
            break
        except Exception as e:
            logger.exception("Неожиданная ошибка: %s", e)
            await asyncio.sleep(5)
            continue

if __name__ == "__main__":
    asyncio.run(run_client())
