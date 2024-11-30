from telethon import events
from llyod import app, ids
from llyod.utils.tools import check_user
from telethon.tl.custom.button import Button
from telethon.tl.custom.message import Message
from llyod.utils.comic_api import get_latest_comics, get_popular, get_trending
from telethon.events.callbackquery import CallbackQuery
import re


@app.on(
    events.NewMessage(
        pattern=r"^[/!]([Ll][Aa][Tt][Ee][Ss][Tt][Cc][Hh][Pp][Ss](@LlyodFronteraBot)?)\s*"
    )
)
async def latest_comics(event: Message):
    "Get the latest chapters of comics"

    query = event.raw_text.split(" ", 1)
    final_type = ""
    qtypes = ""

    if len(query) > 1:
        types = query[1].split(" ")
        for t in types:
            if t == "manhwa":
                final_type += "&country=kr"
            if t == "manhua":
                final_type += "&country=cn"
            if t == "manga":
                final_type += "&country=jp"
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
    if data[0] == "browse":
        if int(data[2]) == 1:
            final_type = data[1]
            data = await get_latest_comics(final_type)
            msg = f"<b>Latest Chapters:-</b>\n"
            for ch in data:
                msg += f"\n📖 <b><a href='https://comick.app/comic/{ch['slug']}'>{ch['title']}</a></b> - <code>{ch['last_chapter']}</code>"

            buttons = [Button.inline("❯", data=f"browse_{final_type}_{2}")]
            await event.edit(
                msg, parse_mode="html", link_preview=False, buttons=buttons
            )

        else:
            final_type = data[1]
            page = int(data[2])
            data = await get_latest_comics(final_type, page)
            msg = f"<b>Latest Chapters:-</b>\n"
            for ch in data:
                msg += f"\n📖 <b><a href='https://comick.app/comic/{ch['slug']}'>{ch['title']}</a></b> - <code>{ch['last_chapter']}</code>"

            buttons = [
                Button.inline("❮", data=f"browse_{final_type}_{page-1}"),
                Button.inline("❯", data=f"browse_{final_type}_{page+1}"),
            ]
            await event.edit(
                msg, parse_mode="html", link_preview=False, buttons=buttons
            )

@app.on(
    events.NewMessage(
        pattern=r"^[/!]([Tt][Oo][Pp](@LlyodFronteraBot)?)\s*"
    )
)
async def popular_comics(event: Message):
    "Get the popular comics"


    query = event.raw_text.split(" ", 1)
    final_type = ""
    genres = ""
    exclude_genres = ""
    types = ""
    comic_type = ["manhwa", "manhua", "manga"]

    if len(query) > 1:
        fquery = re.split(r'\s*,\s*|\s+', query[1].lower())
        if len(fquery) >= 1:
            types = [i for i in fquery if i in comic_type]
        if len(fquery) >= 2:
            genres = [i for i in fquery if not i.startswith("-") and i not in types]
        if len(fquery) >= 2:
            exclude_genres = [i for i in fquery if i.startswith("-")]
  
    
        for t in types:
            if t == "manhwa":
                final_type += "&country=kr"
            elif t == "manhua":
                final_type += "&country=cn"
            elif t == "manga":
                final_type += "&country=jp"
    
    genres_query = "".join([f"&genres={g}" for g in genres if genres])
    exclude_genres_query = "".join([f"&excludes={e}" for e in exclude_genres if exclude_genres]).replace("-", "")

    try:
        data = await get_popular(final_type, 1, genres_query, exclude_genres_query)
    except Exception as e:
        await event.reply(f"Error fetching popular comics: {str(e)}")
        return

    msg = f"<b>Top {', '.join(types)} Comics</b>"
    if genres:
        msg += f" with genres {', '.join(genres)}"
    if exclude_genres:
        msg += f" excluding genres {', '.join(exclude_genres)}"
    msg += ":-\n"
    for ch in data:
        msg += f"\n📖 <b><a href='https://comick.app/comic/{ch['slug']}'>{ch['title']}</a></b>"

    buttons = [Button.url("View More", f"https://comick.io/search?limit=49&sort=user_follow_count{final_type}{genres_query}{exclude_genres_query}")]
    await event.reply(msg, parse_mode="html", link_preview=False, buttons=buttons)

@app.on(
    events.NewMessage(
        pattern=r"^[/!]([Tt][Rr][Ee][Nn][Dd][Ii][Nn][Gg](@LlyodFronteraBot)?)\s*"
    )
)
async def trendings(event: Message):
    "Get the trending comics"

    query = event.raw_text.split(" ", 1)
    tf = "7"
    if len(query) > 1:
        tf = query[1].strip()
        if tf not in ["7", "30", "90"]:
            tf = "7"

    data = await get_trending(tf)

    msg = f"<b>Trending Comics for {tf} days:-</b>\n"
    for ch in data:
        msg += f"\n📖 <b><a href='https://comick.app/comic/{ch['slug']}'>{ch['title']}</a></b>"

    buttons = [Button.url("View More", "https://comick.io/home2")]
    await event.reply(msg, parse_mode="html", link_preview=False, buttons=buttons)