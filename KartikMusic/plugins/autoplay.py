from pyrogram import filters, types
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from KartikMusic import app, db, lang
from KartikMusic.helpers import can_manage_vc


@app.on_message(filters.command(["autoplay", "ap"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def autoplay_panel(_, m: types.Message):
    status = await db.get_autoplay(m.chat.id)

    current = "ᴇɴᴀʙʟᴇᴅ ✅" if status else "ᴅɪsᴀʙʟᴇᴅ ❌"

    text = (
        "💮 <b>ᴀᴜᴛᴏᴘʟᴀʏ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ</b>\n\n"
        f"➥ <b>ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs :</b> {current}\n\n"
        "ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴᴛʀᴏʟ "
        "ᴀᴜᴛᴏᴘʟᴀʏ ꜰᴏʀ ᴛʜɪs ᴄʜᴀᴛ."
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ ᴇɴᴀʙʟᴇ",
                    callback_data="autoplay_enable",
                ),
                InlineKeyboardButton(
                    "❌ ᴅɪsᴀʙʟᴇ",
                    callback_data="autoplay_disable",
                ),
            ],
            [
                InlineKeyboardButton(
                    "⌫ ᴄʟᴏsᴇ",
                    callback_data="close",
                )
            ],
        ]
    )

    await m.reply_text(
        text,
        reply_markup=buttons,
    )
    
@app.on_callback_query(filters.regex("^autoplay_(enable|disable)$"))
@lang.language()
@can_manage_vc
async def autoplay_callback(_, cq: types.CallbackQuery):
    chat_id = cq.message.chat.id

    action = cq.data.split("_")[1]

    if action == "enable":
        await db.set_autoplay(chat_id, True)
        status = "ᴇɴᴀʙʟᴇᴅ ✅"
        await cq.answer("ᴀᴜᴛᴏᴘʟᴀʏ ᴇɴᴀʙʟᴇᴅ.")
    else:
        await db.set_autoplay(chat_id, False)
        status = "ᴅɪsᴀʙʟᴇᴅ ❌"
        await cq.answer("ᴀᴜᴛᴏᴘʟᴀʏ ᴅɪsᴀʙʟᴇᴅ.")

    text = (
        "💮 <b>ᴀᴜᴛᴏᴘʟᴀʏ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ</b>\n\n"
        f"➥ <b>ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs :</b> {status}\n\n"
        "ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴᴛʀᴏʟ "
        "ᴀᴜᴛᴏᴘʟᴀʏ ꜰᴏʀ ᴛʜɪs ᴄʜᴀᴛ."
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ ᴇɴᴀʙʟᴇ",
                    callback_data="autoplay_enable",
                ),
                InlineKeyboardButton(
                    "❌ ᴅɪsᴀʙʟᴇ",
                    callback_data="autoplay_disable",
                ),
            ],
            [
                InlineKeyboardButton(
                    "⌫ ᴄʟᴏsᴇ",
                    callback_data="close",
                )
            ],
        ]
    )

    await cq.edit_message_text(
        text,
        reply_markup=buttons,
    )
