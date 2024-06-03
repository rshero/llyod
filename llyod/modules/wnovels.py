import re
import markdown
from html import unescape
from telethon import events
from llyod import app, ids, queries
from telethon.tl.custom.button import Button
from telethon.tl.custom.message import Message
from llyod.utils.tools import short_names, check_user
from telethon.events.callbackquery import CallbackQuery
from llyod.utils.novels import search_results, get_series

queries = []


@app.on(
    events.NewMessage(pattern="^[/!]([Nn][Oo][Vv][Ee][Ll](@LlyodFronteraBot)?)\s.+")
)
async def novel_search(event: Message):
    args = event.raw_text.split(" ", 1)
    if len(args) == 1:
        await event.reply("Send a query along with the command eg. /comic <query>")
        return
    query = args[1]
    if query.lower() in short_names:
        query = short_names[query.lower()]
    results = await search_results(query)
    results = results["data"]["results"]
    buttons = []
    if not results:
        await event.reply("Nothing found")
        return
    msg = f"Novel Search results for **{query}**:"
    queries.append(query)
    query = queries.index(query)

    for c, result in enumerate(results):
        if c > 5:
            break
        title = result["match"][0][1]
        sid = result["sid"]
        buttons.append([Button.inline(text=title, data=f"{sid}_novels_{query}")])
    x = await event.reply(msg, buttons=buttons)
    ids[f"{x.id}"] = event.sender_id


@app.on(events.CallbackQuery())
@check_user
async def novel_details(event: CallbackQuery.Event):
    data = event.data.decode().split("_")
    if data[1] == "novels":
        sid = int(data[0])
        query = data[2]
        series = await get_series(sid)
        series = series["data"]
        title = series["title"]
        alt_names_list = series.get("alternatenames")
        alt_names = ", ".join(alt_names_list) if alt_names_list else "N/A"
        try:
            unicode_pattern = r"\\u[0-9A-Fa-f]{4}"
            alt_names = re.sub(unicode_pattern, "", alt_names)
        except:
            pass
        authors = ", ".join([author["author"] for author in series["authors"]]) or "N/A"
        try:
            cover = series["covers"][0]["url"]
        except:
            cover = "N/A"
        demographic = series.get("demographic", "N/A")
        description = series.get("description", "N/A")
        try:
            description = markdown.markdown(description, output_format="html")
        except:
            description = "N/A"
        pub_date = series.get("pub_date", "N/A")
        try:
            pub_date = pub_date.split(" ")[3] if pub_date != "N/A" else "N/A"
        except:
            pub_date = "N/A"
        genres = (
            ", ".join([genre["genre"].capitalize() for genre in series["genres"]])
            or "N/A"
        )
        try:
            status = unescape(series.get("orig_status", "N/A"))
        except:
            status = "N/A"
        latest_str = series.get("latest_str", "N/A")
        try:
            rating = round(series["rating"]["avg"], 2)
        except:
            rating = "N/A"
        url = f"https://www.wlnupdates.com/series-id/{sid}"
        msg = f"<b>{title} (<code>{pub_date}</code>)</b>"
        msg += f"\n\n<b>Rating:</b> <code>{rating}</code>"
        msg += f"\n<b>Authors:</b> <code>{authors}</code>"
        msg += f"\n<b>Latest:</b> <code>{latest_str}</code>"
        msg += f"\n<b>Alternative Names:</b> <code>{alt_names}</code>"
        msg += f"\n<b>Demographic:</b> <code>{demographic}</code>"
        msg += f"\n<b>Status:</b> <code>{status}</code>"
        msg += f"\n<b>Genres:</b> <code>{genres}</code>"
        msg += f"\n\n<b>Description:</b>\n{description}"
        msg += f"\n\n<a href='{cover}'>&#xad</a>"

        await event.edit(
            msg,
            parse_mode="html",
            buttons=[
                [Button.url("Info", url=url)],
                [Button.inline("❮", data=f"{sid}_novelb_{query}")],
            ],
        )

    if data[1] == "novelb":
        query = queries[int(data[2])]
        buttons = []
        results = await search_results(query)
        results = results["data"]["results"]
        msg = f"Novel Search results for **{query}**:"
        for c, result in enumerate(results):
            if c > 5:
                break
            title = result["match"][0][1]
            sid = result["sid"]
            buttons.append(
                [Button.inline(text=title, data=f"{sid}_novels_{queries.index(query)}")]
            )
        await event.edit(msg, buttons=buttons)
