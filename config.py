from os import getenv
import os

from dotenv import load_dotenv
load_dotenv()

API_ID = int(getenv("API_ID", None))
API_HASH = getenv("API_HASH", None)
BOT_TOKEN = getenv("BOT_TOKEN", None)
OWNER_ID = int(getenv("OWNER_ID", None))
MONGO_URL = getenv("MONGO_URL", None)

_auth_channel = getenv("AUTH_CHANNEL")
AUTH_CHANNEL = int(_auth_channel) if _auth_channel else None
FSUB = getenv("FSUB", "false").lower() == "true"

# NOTE: previously these were hardcoded to the original template author's
# Telegram ID / private group, which silently gave THEM /eval & /sh (remote
# code execution) access on every forked deployment, and sent every
# "user started bot" / "bot added to group" log to THEIR private chat.
# Both now come from your own env vars instead.
OWNER = OWNER_ID
LOGGER_GROUP_ID = int(getenv("LOGGER_GROUP_ID", OWNER_ID))
BOT_NAME = os.environ.get("BOT_NAME", "𝗡𝗼𝘃𝗮 𝗔𝗜 ⚡")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "Evachatrobot")
SUPPORT_GROUP = os.environ.get("SUPPORT_GROUP", "evagroupp")
UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "evasupportt")

# ── AI (Groq) settings ────────────────────────────────────────────────
# Groq is used because it is currently the fastest LLM inference API
# available, which keeps chat replies near-instant.
# Get a free key at: https://console.groq.com/keys
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
AI_ENABLED_BY_DEFAULT = os.environ.get("AI_ENABLED_BY_DEFAULT", "true").lower() == "true"

# Personality the AI replies with. Feel free to edit this to change the bot's tone.
AI_PERSONA = os.environ.get(
    "AI_PERSONA",
    f"You are {BOT_NAME}, a friendly, witty, upbeat Telegram chat companion. "
    "Reply in a warm, casual, slightly playful tone. Keep replies short "
    "(1-3 sentences) unless the user clearly wants a detailed answer. "
    "Mirror the user's language (Hindi/Hinglish/English) naturally. "
    "Never claim to be human, never generate harmful content."
)

STICKER = [
"CAACAgUAAxkBAAKV2Ge_HEejUGb8foZZ9eunAivt46rNAAL9EQAC-EXwV3yNmpSjijuwHgQ",
"CAACAgUAAxkBAAKV12e_HEUWk7Dr9lPFRy0YJ2W_aZQnAAIgEgACRnzxV6MUtKkl8-lcHgQ",
"CAACAgQAAxkBAAKV1me_HC0meq-fnc8-RrNQlkuvuddmAAKpFgACpvFxHgRaY3CLWAIXHgQ",
"CAACAgQAAxkBAAKV1We_HCp1JciP72U9NorWCvM9IvjSAAI9CQACzsTxUNSMpeZiwDESHgQ",
"CAACAgQAAxkBAAKV1Ge_HB5qp-1sh5Fih-RTyLJ34bljAAL6FgACpvFxHkyKzYENX-WBHgQ",
"CAACAgUAAxkBAAKV2We_HErZCR15-PcfUV3OEeNjsvMlAAITEAAC2ITwV380JBetASe0HgQ",
"CAACAgUAAxkBAAKV2me_HEpT3JOOUzFYXEx60jHrS1SKAAKtEQACgNnwV69z3WlbOQegHgQ",
"CAACAgQAAxkBAAKV62e_HSAOCrZl91ePlp-ycQWJXSNAAALYFgACpvFxHj74GKD3lBVqHgQ",
"CAACAgQAAxkBAAKV6me_HRbgSn9-ggtXybOk2ttI_LCXAAIYCQACQ_8RUpOq_3qBgteUHgQ",
"CAACAgQAAxkBAAKV6We_HRQoxwv5PwHe6EFISSLODrzjAAK9FgACpvFxHqjYRWoNyxh4HgQ",
]


IMG = [
"https://graph.org/file/eaa3a2602e43844a488a5.jpg",
"https://graph.org/file/b129e98b6e5c4db81c15f.jpg",
"https://graph.org/file/3ccb86d7d62e8ee0a2e8b.jpg",
"https://graph.org/file/df11d8257613418142063.jpg",
"https://graph.org/file/9e23720fedc47259b6195.jpg",
"https://graph.org/file/826485f2d7db6f09db8ed.jpg",
"https://graph.org/file/ff3ad786da825b5205691.jpg",
"https://graph.org/file/52713c9fe9253ae668f13.jpg",
"https://graph.org/file/8f8516c86677a8c91bfb1.jpg",
"https://graph.org/file/6603c3740378d3f7187da.jpg",
"https://graph.org/file/66cb6ec40eea5c4670118.jpg",
"https://graph.org/file/2e3cf4327b169b981055e.jpg",
"https://files.catbox.moe/4q7c4w.jpg",
"https://files.catbox.moe/90z6sq.jpg",
"https://files.catbox.moe/rdfi4z.jpg",
"https://files.catbox.moe/6f9rgp.jpg",
"https://files.catbox.moe/99wj12.jpg",
"https://files.catbox.moe/ezpnd2.jpg",
"https://files.catbox.moe/e7q55f.jpg",
"https://files.catbox.moe/qyfsi7.jpg",
"https://files.catbox.moe/kbke7s.jpg",
"https://files.catbox.moe/7icvpu.jpg",
"https://files.catbox.moe/4hd77z.jpg",
"https://files.catbox.moe/yn7wje.jpg",
"https://files.catbox.moe/kifsir.jpg",
"https://files.catbox.moe/zi21kc.jpg",
]