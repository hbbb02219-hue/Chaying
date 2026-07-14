from pyrogram.types import InlineKeyboardButton

from config import BOT_USERNAME, OWNER_ID, SUPPORT_GROUP


STBUTTON = [
  [
       InlineKeyboardButton(
    text="✙ ʌᴅᴅ ϻє ʙᴧʙʏ ✙",
    url=f"https://t.me/{BOT_USERNAME}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users",
        ),
  ],
  [
    InlineKeyboardButton(
      text="⌯ ❍ᴡɴᴇʀ ⌯",
      user_id=OWNER_ID,
    ),
      InlineKeyboardButton(
      text="⌯ ᴧʙσᴜᴛ ⌯",
      callback_data="ABOUT",
    ),
  ],
    [
        InlineKeyboardButton(text="⌯ ʜєʟᴘ ᴧηᴅ ᴄσϻϻᴧηᴅs ⌯", callback_data="help"),
    ],
]

ABOUT_BUTTON = [
    [
        InlineKeyboardButton("⌯ 𝛅ᴜᴘᴘσʀᴛ ⌯", url="https://t.me/evasupportt"),
        InlineKeyboardButton("⌯ ᴜᴘᴅᴧᴛє ˼⌯", url="https://t.me/evasupportt")
    ],
    [
        InlineKeyboardButton("⌯ ʙᴧᴄᴋ ⌯", callback_data=f"HELP_BACK")
    ]
]

PNG_BTN = [
    [
        InlineKeyboardButton(
            text="ʌᴅᴅ ϻє", 
            url=f"https://t.me/{BOT_USERNAME}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users"
        ),
        InlineKeyboardButton(
            text="⌯ 𝛅ᴜᴘᴘᴏʀᴛ ⌯", 
            url=f"https://t.me/{SUPPORT_GROUP}"
        ),
    ],
]



HELP_BACK = [

    [
        InlineKeyboardButton(text="𝛅ᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_GROUP}"),
        InlineKeyboardButton(text="вᴧᴄᴋ", callback_data="HELP_BACK"),
    ],
]


CHATBOT_ON = [
    [
        InlineKeyboardButton(text="ᴇɴᴀʙʟᴇ", callback_data=f"addchat"),
        InlineKeyboardButton(text="ᴅɪsᴀʙʟᴇ", callback_data=f"rmchat"),
    ],
]
