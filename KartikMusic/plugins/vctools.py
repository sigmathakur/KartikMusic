from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.enums import ParseMode
from KartikMusic import app


@app.on_message(filters.video_chat_started)
async def vc_started(_, message: Message):
    chat_name = message.chat.title or "this group"

    text = (
        f"<b>❖ 🎙 Video Chat Started in {chat_name}</b>\n\n"
        f"<b>⏤͟͟͞͞★ Join Fast And Start Gossip 🙊</b>"
    )

    add_link = f"https://t.me/{app.username}?startgroup=true"

    await message.reply(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    text="✙ ʌᴅᴅ ϻє ɪη ʏσυʀ ɢʀσυᴘ ✙",
                    url=add_link
                )
            ]]
        )
    )


@app.on_message(filters.video_chat_ended)
async def vc_ended(_, message: Message):
    chat_name = message.chat.title or "this group"

    text = (
        f"<b>❖ 🔇 Video Chat Ended in {chat_name}</b>\n\n"
        f"<b>⏤͟͟͞͞★ Bye Bye Friends, See You Soon 💔</b>"
    )

    add_link = f"https://t.me/{app.username}?startgroup=true"

    await message.reply(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    text="✙ ʌᴅᴅ ϻє ɪη ʏσυʀ ɢʀσυᴘ ✙",
                    url=add_link
                )
            ]]
        )
    )


@app.on_message(filters.video_chat_members_invited)
async def vc_invited(client, message: Message):

    if not message.from_user:
        return

    inviter = message.from_user.mention(style="html")

    users = message.video_chat_members_invited.users
    if not users:
        return

    invited = ", ".join(
        user.mention(style="html")
        for user in users
    )

    text = (
        f"<b>❖ {inviter} invited {invited} on Video Chat ⚡</b>\n\n"
        f"<b>⏤͟͟͞͞★ Join Fast Baby 🙊</b>"
    )

    add_link = f"https://t.me/{client.username}?startgroup=true"

    await message.reply(
        text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    text="✙ ʌᴅᴅ ϻє ɪη ʏσυʀ ɢʀσυᴘ ✙",
                    url=add_link
                )
            ]]
        )
    )
