"""
Fast AI reply engine using Groq's LPU inference API.

Groq is used deliberately over other providers because it serves open
models (Llama 3.3 etc.) at very high tokens/sec, which keeps the bot's
replies feeling near-instant even under group-chat load.

Falls back gracefully (returns None) if no API key is configured or the
request fails, so the caller can fall back to the learned-reply system.
"""

import asyncio
import logging
import time
from collections import defaultdict, deque

import aiohttp

import config

LOGGER = logging.getLogger("SonaliChat.ai")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# Short rolling per-chat memory so replies feel contextual, not amnesiac.
# Deliberately kept small (in RAM) so it never becomes a DB bottleneck.
_HISTORY_LIMIT = 8
_history: dict[int, deque] = defaultdict(lambda: deque(maxlen=_HISTORY_LIMIT))

# One shared aiohttp session for connection pooling -> much faster than
# opening a new TCP/TLS connection on every single message.
_session: aiohttp.ClientSession | None = None
_session_lock = asyncio.Lock()


async def _get_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        async with _session_lock:
            if _session is None or _session.closed:
                timeout = aiohttp.ClientTimeout(total=12)
                _session = aiohttp.ClientSession(timeout=timeout)
    return _session


def is_ai_configured() -> bool:
    return bool(config.GROQ_API_KEY)


def remember(chat_id: int, role: str, content: str) -> None:
    """Store a message in the short rolling history for a chat."""
    if not content:
        return
    _history[chat_id].append({"role": role, "content": content[:2000]})


def clear_history(chat_id: int) -> None:
    _history.pop(chat_id, None)


async def get_ai_reply(chat_id: int, user_text: str) -> str | None:
    """
    Ask Groq for a reply. Returns None on any failure so the caller can
    fall back to another response method instead of erroring out to the user.
    """
    if not is_ai_configured():
        return None

    messages = [{"role": "system", "content": config.AI_PERSONA}]
    messages.extend(_history[chat_id])
    messages.append({"role": "user", "content": user_text[:2000]})

    payload = {
        "model": config.GROQ_MODEL,
        "messages": messages,
        "temperature": 0.8,
        "max_tokens": 300,
    }
    headers = {
        "Authorization": f"Bearer {config.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        session = await _get_session()
        t0 = time.monotonic()
        async with session.post(GROQ_URL, json=payload, headers=headers) as resp:
            if resp.status != 200:
                body = await resp.text()
                LOGGER.warning("Groq API error %s: %s", resp.status, body[:300])
                return None
            data = await resp.json()
        elapsed = (time.monotonic() - t0) * 1000
        LOGGER.info("Groq reply in %.0fms", elapsed)

        reply = data["choices"][0]["message"]["content"].strip()
        if reply:
            remember(chat_id, "user", user_text)
            remember(chat_id, "assistant", reply)
        return reply or None
    except asyncio.TimeoutError:
        LOGGER.warning("Groq request timed out")
        return None
    except Exception:
        LOGGER.exception("Groq request failed")
        return None