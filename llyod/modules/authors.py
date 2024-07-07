from html import unescape
from telethon import events
from llyod import app, ids, queries
from llyod.utils.tools import check_user
from telethon.tl.custom.button import Button
from telethon.tl.custom.message import Message
from telethon.events.callbackquery import CallbackQuery
from llyod.utils.manga import search_authors, author_detail, list_series


@app.on(events.NewMessage(pattern=r"^[!/](author(@LlyodFronteraBot)?)\s.+"))
async def authors(event: Message):
    args = event.raw_text.split(" ", 1)
    if len(args) == 1:
        await event.reply("Send a query along with the command eg. /author <query>")
        return
    query = args[1]
    buttons = []
    results = await search_authors(query)
    if not results:
        await event.reply("Nothing found")
        return
    btns = len(results)
    if len(results) > 7:
        btns = 6
    for result in range(btns):
        name = unescape(results[result]["record"]["name"])
        buttons.append(
            [
                Button.inline(
                    text=name,
                    data=f"{results[result]['record']['id']}_authsearch_{query}",
                )
            ]
        )
    x = await event.reply(f"Author search results for **{query}**:", buttons=buttons)
    ids[f"{x.id}"] = event.sender_id


@app.on(events.CallbackQuery())
@check_user
async def author(event: CallbackQuery.Event):
    data = event.data.decode().split("_")
    if data[1] == "authsearch":
        id = data[0]
        query = data[2]
        author_data = await author_detail(id)
        name = author_data["name"]
        url = author_data["url"] or "N/A"
        image = author_data["image"]["url"]["original"]
        act_name = author_data["actualname"] or "N/A"
        birthplace = author_data["birthplace"] or "N/A"
        gender = author_data["gender"] or "N/A"
        comments = author_data["comments"] or "N/A"
        comments = comments.replace("<BR>", "\n")
        genres = ", ".join(author_data["genres"]) or "N/A"
        stats = author_data["stats"]["total_series"]
        msg = f"<b>{name}</b> (<code>{act_name}</code>)\n\n<b>Birthplace:</b> <code>{birthplace}</code>\n<b>Gender:</b> <code>{gender}</code>\n<b>Genres:</b> <code>{genres}</code>\n</b>Total Series:</b> <code>{stats}</code>\n<a href='{image}'>&#xad</a>\n\n{comments}"
        await event.edit(
            msg,
            parse_mode="html",
            buttons=[
                [
                    Button.url("Info", url=url),
                    Button.inline("List Series", data=f"{id}_listseries_{query}"),
                ],
                [Button.inline("❮", data=f"{query}_authback")],
            ],
        )

    if data[1] == "authback":
        query = data[0]
        buttons = []
        results = await search_authors(query)
        btns = len(results)
        if len(results) > 7:
            btns = 6
        for result in range(btns):
            name = unescape(results[result]["record"]["name"])
            buttons.append(
                [
                    Button.inline(
                        text=name,
                        data=f"{results[result]['record']['id']}_authsearch_{query}",
                    )
                ]
            )
        await event.edit(f"Author search results for **{query}**:", buttons=buttons)

    if data[1] == "listseries":
        id = data[0]
        query = data[2]
        series_list = await list_series(id)
        names = ""
        for name in series_list["series_list"]:
            names += f"• {name['title']}\n"

        if names == "":
            names = "Nothing"

        await event.edit(
            f"**List of series for this author:**\n\n{unescape(names)}",
            buttons=Button.inline("❮", data=f"{id}_authsearch_{query}"),
        )
