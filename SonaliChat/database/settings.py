from . import db
import config

# Per-chat toggle: whether the bot responds at all in a given group.
settingsdb = db["chat_settings"]

# Learned word -> reply pairs (used as a fast local fallback when AI
# is unavailable, and to keep the "teach me" reply-training feature).
learndb = db["learned"]

_indexes_ready = False


async def ensure_indexes():
    """Create indexes once at startup so lookups stay fast as data grows."""
    global _indexes_ready
    if _indexes_ready:
        return
    await settingsdb.create_index("chat_id", unique=True)
    await learndb.create_index("trigger")
    _indexes_ready = True


async def is_bot_enabled(chat_id: int) -> bool:
    doc = await settingsdb.find_one({"chat_id": chat_id})
    if doc is None:
        return True
    return doc.get("enabled", True)


async def set_bot_enabled(chat_id: int, enabled: bool) -> None:
    await settingsdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_id": chat_id, "enabled": enabled}},
        upsert=True,
    )


async def learn(trigger: str, reply: str, kind: str = "text") -> None:
    """Store a trigger -> reply pair, skipping exact duplicates."""
    if not trigger or not reply:
        return
    exists = await learndb.find_one({"trigger": trigger, "reply": reply})
    if not exists:
        await learndb.insert_one({"trigger": trigger, "reply": reply, "kind": kind})


async def get_learned_replies(trigger: str) -> list:
    cursor = learndb.find({"trigger": trigger})
    return [doc async for doc in cursor]