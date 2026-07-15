"""
SonaliChat - AI Chatbot Toggle Module
--------------------------------------
Commands:
    /chatbot            -> Shows current status (ON/OFF) in this chat
    /chatbot enable     -> Turns ON AI auto-chat in this group/chat
    /chatbot disable    -> Turns OFF AI auto-chat in this group/chat

ASSUMPTIONS (badlo agar tumhara bot alag setup use karta hai):
    - Framework   : Pyrogram
    - Database    : MongoDB via Motor (motor.motor_asyncio)
    - Mongo URI   : env var DATABASE_URL / MONGO_DB_URI / MONGODB_URI / DB_URI
                    (jo bhi tumhare bot mein already set hai, wahi use ho jayega)
    - DB name     : "SonaliChat"  <-- ye line neeche badal do agar tumhara db
                    name different hai (check apne existing database file mein)
    - Collection  : "chatbot_settings" -> ye BILKUL NAYA collection hai,
                    tumhara purana data isse touch nahi hoga.

Agar tumhare bot mein already ek shared mongo client hai (e.g.
`SonaliChat/database/__init__.py` mein `mongodb = AsyncIOMotorClient(...)`),
to neeche wala "Database setup" block hata ke ye line use karo:

    from SonaliChat.database import mongodb as _mongo_client
"""

import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType, ChatMemberStatus
from motor.motor_asyncio import AsyncIOMotorClient

# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------
DB_URI = (
    os.getenv("DATABASE_URL")
    or os.getenv("MONGO_DB_URI")
    or os.getenv("MONGODB_URI")
    or os.getenv("DB_URI")
)

_mongo_client = AsyncIOMotorClient(DB_URI)
_db = _mongo_client["SonaliChat"]              # <-- apna actual DB name yahan check karo
chatbot_settings = _db["chatbot_settings"]      # naya collection, purana data safe


async def is_chatbot_enabled(chat_id: int) -> bool:
    doc = await chatbot_settings.find_one({"chat_id": chat_id})
    return bool(doc and doc.get("enabled", False))


async def set_chatbot_status(chat_id: int, enabled: bool):
    await chatbot_settings.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_id": chat_id, "enabled": enabled}},
        upsert=True,
    )


# ---------------------------------------------------------------------------
# Permission check: sirf admin (group mein) ya user khud (private mein)
# ---------------------------------------------------------------------------
async def can_toggle(client: Client, message: Message) -> bool:
    if message.chat.type == ChatType.PRIVATE:
        return True
    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)


# ---------------------------------------------------------------------------
# Command: /chatbot [enable|disable]
# ---------------------------------------------------------------------------
@Client.on_message(filters.command("chatbot"))
async def chatbot_toggle(client: Client, message: Message):
    if not await can_toggle(client, message):
        await message.reply_text("❌ Sirf group admins hi ye setting change kar sakte hain.")
        return

    if len(message.command) < 2:
        status = await is_chatbot_enabled(message.chat.id)
        await message.reply_text(
            f"🤖 Chatbot abhi **{'ON ✅' if status else 'OFF ❌'}** hai is chat mein.\n\n"
            "Use: `/chatbot enable` ya `/chatbot disable`"
        )
        return

    arg = message.command[1].lower()
    if arg == "enable":
        await set_chatbot_status(message.chat.id, True)
        await message.reply_text("✅ Chatbot **ON** kar diya gaya is chat ke liye.")
    elif arg == "disable":
        await set_chatbot_status(message.chat.id, False)
        await message.reply_text("❌ Chatbot **OFF** kar diya gaya is chat ke liye.")
    else:
        await message.reply_text("Use: `/chatbot enable` ya `/chatbot disable`")


# ---------------------------------------------------------------------------
# Auto-reply handler: sirf tab chalega jab us chat mein chatbot enabled ho
# ---------------------------------------------------------------------------
@Client.on_message(
    filters.text & ~filters.command(["chatbot"]) & ~filters.via_bot,
    group=1,
)
async def ai_auto_reply(client: Client, message: Message):
    if message.from_user and message.from_user.is_bot:
        return

    if not await is_chatbot_enabled(message.chat.id):
        return

    reply = await get_ai_response(message.text)
    if reply:
        await message.reply_text(reply)


async def get_ai_response(user_text: str) -> str:
    """
    🔌 Apna AI provider (OpenAI / Gemini / etc) yahan plug karo.
    Abhi ke liye ye placeholder hai.
    """
    return "🤖 (AI response yahan aayega — apna AI API call is function mein add karo)"
