# -----------------------------------------------
# 🔸 ShashankMusic Project
# 🔹 Developed & Maintained by: Shashank Shukla (https://github.com/itzshukla)
# 📅 Copyright © 2025 – All Rights Reserved
#
# 📖 License:
# This source code is open for educational and non-commercial use ONLY.
# You are required to retain this credit in all copies or substantial portions of this file.
# Commercial use, redistribution, or removal of this notice is strictly prohibited
# without prior written permission from the author.
#
# ❤️ Made with dedication and love by ItzShukla
# -----------------------------------------------

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ShashankMusic import app
from ShashankMusic.utils.stream.autoplay import is_autoplay, enable_autoplay, disable_autoplay
from ShashankMusic.utils.decorators.admins import ActualAdminCB
from config import BANNED_USERS

@app.on_message(
    filters.command(["autoplay", "ap"])
    & filters.group
    & ~BANNED_USERS
)
async def autoplay_command(client, message: Message):
    chat_id = message.chat.id
    status = await is_autoplay(chat_id)

    current_status = "ᴇɴᴀʙʟᴇᴅ ✅" if status else "ᴅɪsᴀʙʟᴇᴅ ❌"

    text = (
        f"💮 <b>ᴀᴜᴛᴏᴘʟᴀʏ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ</b>\n\n"
        f"ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs: {current_status}\n\n"
        f"ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴᴛʀᴏʟ ᴀᴜᴛᴏᴘʟᴀʏ."
    )

    buttons = [
        [
            InlineKeyboardButton("ᴇɴᴀʙʟᴇ", callback_data="set_autoplay|enable"),
            InlineKeyboardButton("ᴅɪsᴀʙʟᴇ", callback_data="set_autoplay|disable")
        ],
        [
            InlineKeyboardButton("ᴄʟᴏsᴇ ⌫", callback_data="close")
        ]
    ]

    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex(pattern=r"set_autoplay") & ~BANNED_USERS)
@ActualAdminCB
async def autoplay_callback(client, callback_query: CallbackQuery, _):
    chat_id = callback_query.message.chat.id
    data_parts = callback_query.data.split("|")
    data = data_parts[1]

    is_from_settings = len(data_parts) > 2 and data_parts[2] == "settings"

    current_status = await is_autoplay(chat_id)

    if data == "enable":
        if current_status:
            return await callback_query.answer("⚠️ ᴀᴜᴛᴏᴘʟᴀʏ ɪs ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ.!", show_alert=True)

        await enable_autoplay(chat_id)
        new_status_text = "ᴇɴᴀʙʟᴇᴅ ✅"
        await callback_query.answer("✅ ᴀᴜᴛᴏᴘʟᴀʏ ᴇɴᴀʙʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.!", show_alert=False)

    else: # data == "disable"
        if not current_status:
            return await callback_query.answer("⚠️ ᴀᴜᴛᴏᴘʟᴀʏ ɪs ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ.!", show_alert=True)

        await disable_autoplay(chat_id)
        new_status_text = "ᴅɪsᴀʙʟᴇᴅ ❌"
        await callback_query.answer("❌ ᴀᴜᴛᴏᴘʟᴀʏ ᴅɪsᴀʙʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.!", show_alert=False)

    text = (
        f"💮 <b>ᴀᴜᴛᴏᴘʟᴀʏ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ</b>\n\n"
        f"ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs: {new_status_text}\n\n"
        f"ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴᴛʀᴏʟ ᴀᴜᴛᴏᴘʟᴀʏ."
    )

    buttons = [
        [
            InlineKeyboardButton("ᴇɴᴀʙʟᴇ", callback_data=f"set_autoplay|enable|settings" if is_from_settings else "set_autoplay|enable"),
            InlineKeyboardButton("ᴅɪsᴀʙʟᴇ", callback_data=f"set_autoplay|disable|settings" if is_from_settings else "set_autoplay|disable")
        ]
    ]

    if is_from_settings:
        buttons.append([
            InlineKeyboardButton("ʙᴀᴄᴋ ⟲", callback_data="settings_helper"),
            InlineKeyboardButton("ᴄʟᴏsᴇ ⌫", callback_data="close")
        ])
    else:
        buttons.append([
            InlineKeyboardButton("ᴄʟᴏsᴇ ⌫", callback_data="close")
        ])

    try:
        await callback_query.edit_message_text(
            text, 
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except:
        pass