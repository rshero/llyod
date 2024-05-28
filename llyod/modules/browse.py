from telethon import events
from llyod import app, ids, queries
from llyod.utils.tools import check_user
from telethon.tl.custom.button import Button
from telethon.tl.custom.message import Message
from llyod.utils.comic_api import get_latest_comics
from telethon.events.callbackquery import CallbackQuery

@app.on(events.NewMessage(pattern="^[/!]([Ll][Aa][Tt][Ee][Ss][Tt][Cc][Hh][Pp][Ss](@LlyodFronteraBot)?)\s*"))
async def latest_comics(event: Message):
    "Get the latest chapters of comics"

    query = event.raw_text.split(" ", 1)
    final_type = ''
    qtypes = ''

    if len(query) > 1:
        types = query[1].split(" ")
        for t in types:
            if t == 'manhwa':
                final_type += '&country=kr'
            if t == 'manhua':
                final_type += '&country=cn'
            if t == 'manga':
                final_type += '&country=jp'
    data = await get_latest_comics(final_type)

    msg = f"<b>Latest Chapters:-</b>\n"
    for ch in data:
        msg += f"\n📖 <b><a href='https://comick.app/comic/{ch['slug']}'>{ch['title']}</a></b> - <code>{ch['last_chapter']}</code>"

    buttons = [Button.inline("❯", data=f"browse_{final_type}_{2}")]
    x = await event.reply(msg, parse_mode="html", link_preview=False, buttons=buttons)
    ids[f"{x.id}"] = event.sender_id


@app.on(events.CallbackQuery())
@check_user
async def comic_detail(event: CallbackQuery.Event):
    data = event.data.decode().split("_")
    if data[0] == 'browse':
        if int(data[2]) == 1:
            final_type = data[1]
            data = await get_latest_comics(final_type)
            msg = f"<b>Latest Chapters:-</b>\n"
            for ch in data:
                msg += f"\n📖 <b><a href='https://comick.app/comic/{ch['slug']}'>{ch['title']}</a></b> - <code>{ch['last_chapter']}</code>"

            buttons = [Button.inline("❯", data=f"browse_{final_type}_{2}")]
            await event.edit(msg, parse_mode="html", link_preview=False, buttons=buttons)
            
        else:
            final_type = data[1]
            page = int(data[2])
            data = await get_latest_comics(final_type, page)
            msg = f"<b>Latest Chapters:-</b>\n"
            for ch in data:
                msg += f"\n📖 <b><a href='https://comick.app/comic/{ch['slug']}'>{ch['title']}</a></b> - <code>{ch['last_chapter']}</code>"

            buttons = [Button.inline("❮", data=f"browse_{final_type}_{page-1}"), Button.inline("❯", data=f"browse_{final_type}_{page+1}")]
            await event.edit(msg, parse_mode="html", link_preview=False, buttons=buttons)
