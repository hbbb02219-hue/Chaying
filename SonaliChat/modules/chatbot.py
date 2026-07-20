"""
Chatbot module.

Reply pipeline for every eligible message:
  1. If the bot is disabled for this group -> do nothing.
  2. If AI (Groq) is configured -> ask it for a reply (fast, contextual).
  3. If AI isn't configured or the call fails -> fall back to any reply the
     bot has *learned* before for this exact trigger text.
  4. If nothing matches -> send a friendly "didn't get that" nudge instead
     of staying silent (feels more alive / attractive to chat with).

Teaching: if a user replies to *another user's* message with some text or
a sticker, that pair is learned as trigger -> reply, exactly like before,
but now stored through the shared async Motor connection with an index,
instead of opening a brand-new blocking pymongo connection per message
(which was the main cause of slowness).
"""

import random

from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from SonaliChat import app as AMBOT
from SonaliChat.database import (
    get_learned_replies,
    is_bot_enabled,
    learn,
    set_bot_enabled,
)
from SonaliChat.modules.helpers import CHATBOT_ON
from SonaliChat.modules.helpers.ai import get_ai_reply, is_ai_configured

COMMAND_PREFIXES = ("!", "/", "?", "@", "#")

FALLBACK_REPLIES = [
    "Hmm samajh nahi aaya 🤔 thoda alag se bolo na?",
    "Oops, wo mujhe abhi nahi pata 😅 kuch aur pucho?",
    "Main soch rahi hoon iske baare mein... phir se try karo? 💭",
]


def _looks_like_command(text: str) -> bool:
    return bool(text) and text.startswith(COMMAND_PREFIXES)


@AMBOT.on_message(filters.command(["chatbot"]) & filters.group & ~filters.bot)
async def chatbot_toggle_menu(_, m: Message):
    await m.reply_text(
        f"ᴄʜᴀᴛ: `{m.chat.id}`\n**ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ.**",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )


@AMBOT.on_callback_query(filters.regex("^addchat$"))
async def enable_chatbot_cb(_, cq: CallbackQuery):
    await set_bot_enabled(cq.message.chat.id, True)
    await cq.answer("ᴄʜᴀᴛʙᴏᴛ ᴇɴᴀʙʟᴇᴅ ✅", show_alert=True)


@AMBOT.on_callback_query(filters.regex("^rmchat$"))
async def disable_chatbot_cb(_, cq: CallbackQuery):
    await set_bot_enabled(cq.message.chat.id, False)
    await cq.answer("ᴄʜᴀᴛʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ ❌", show_alert=True)


async def _reply_smart(client: Client, message: Message, trigger_text: str) -> None:
    """Core reply logic shared by group + private handlers."""
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)

    reply_text = None
    if is_ai_configured():
        reply_text = await get_ai_reply(message.chat.id, trigger_text)

    if reply_text:
        await message.reply_text(reply_text)
        return

    # Fall back to learned replies for this exact trigger.
    learned = await get_learned_replies(trigger_text)
    if learned:
        pick = random.choice(learned)
        if pick.get("kind") == "sticker":
            await message.reply_sticker(pick["reply"])
        else:
            await message.reply_text(pick["reply"])
        return

    await message.reply_text(random.choice(FALLBACK_REPLIES))


async def _maybe_learn(message: Message) -> None:
    """
    Teaching path: replying to someone else's message teaches the bot
    that {their message} -> {your message} is a valid response pair.
    """
    reply_to = message.reply_to_message
    if not reply_to:
        return

    trigger = reply_to.text or (
        reply_to.sticker.file_unique_id if reply_to.sticker else None
    )
    if not trigger:
        return

    if message.sticker:
        await learn(trigger, message.sticker.file_id, kind="sticker")
    elif message.text:
        await learn(trigger, message.text, kind="text")


@AMBOT.on_message(
    (filters.text | filters.sticker) & filters.group & ~filters.bot & ~filters.via_bot
)
async def chatbot_group(client: Client, message: Message):
    if message.text and _looks_like_command(message.text):
        return

    if not await is_bot_enabled(message.chat.id):
        return

    reply_to = message.reply_to_message

    # Someone replying to the bot -> talk to it.
    if reply_to and reply_to.from_user and reply_to.from_user.id == client.me.id:
        text = message.text or "[sticker]"
        await _reply_smart(client, message, text)
        return

    # Someone replying to another user -> teach the bot that pairing.
    if reply_to and reply_to.from_user and reply_to.from_user.id != client.me.id:
        await _maybe_learn(message)
        return

    # A plain message (not a reply at all) -> bot jumps into the chat.
    if not reply_to and message.text:
        await _reply_smart(client, message, message.text)


@AMBOT.on_message(
    (filters.text | filters.sticker) & filters.private & ~filters.bot & ~filters.via_bot
)
async def chatbot_private(client: Client, message: Message):
    if message.text and _looks_like_command(message.text):
        return

    text = message.text or "[sticker]"
    await _reply_smart(client, message, text)