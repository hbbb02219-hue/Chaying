import importlib

from pyrogram import idle

from SonaliChat import app, LOGGER
from SonaliChat.database import ensure_indexes
from SonaliChat.modules import ALL_MODULES
from SonaliChat.modules.helpers.ai import is_ai_configured

async def boot():
    await app.start()
    await ensure_indexes()

    for module in ALL_MODULES:
        importlib.import_module(f"SonaliChat.modules.{module}")

    if is_ai_configured():
        LOGGER.info("AI replies: ENABLED (Groq) ⚡")
    else:
        LOGGER.info("AI replies: DISABLED (no GROQ_API_KEY set) — using learned replies only")

    await idle()
    await app.stop()

if __name__ == "__main__":
    app.run(boot())