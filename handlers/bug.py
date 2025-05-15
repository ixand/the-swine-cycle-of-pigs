from aiogram import types
from aiogram.filters import CommandObject
from aiogram.types import Message
import html

ADMIN_CHAT_ID = -1002500459432
BUG_TOPIC_ID = 9121
MAX_MESSAGE_LENGTH = 4000  # офіційний Telegram ліміт — 4096, беремо запас

async def bug_report_handler(message: Message, command: CommandObject):
    user = message.from_user
    text = command.args

    if not text:
        await message.answer("❗ Будь ласка, надішли опис проблеми. Наприклад:\n/bug бот не відповідає після команди /fight")
        return

    if len(text) > MAX_MESSAGE_LENGTH:
        await message.answer("❗ Повідомлення надто довге (максимум 4000 символів).\nСкороти текст і спробуй ще раз.")
        return

    author = f"{user.full_name} (@{user.username or 'no username'}) [ID: {user.id}]"
    text_escaped = html.escape(text)
    author_escaped = html.escape(author)

    report = (
        f"🐞 <b>Надійшло повідомлення про баг:</b>\n\n"
        f"📨 <i>{text_escaped}</i>\n\n"
        f"👤 Від: {author_escaped}"
    )

    await message.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=report,
        parse_mode="HTML",
        message_thread_id=BUG_TOPIC_ID
    )

    await message.answer("✅ Дякую! Твоє повідомлення про баг надіслано розробникам.")
