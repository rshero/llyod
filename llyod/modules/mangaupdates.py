import hashlib
from html import unescape
from telethon import events
from llyod import app, ids, queries
from llyod.utils.tools import is_sha1_hashed
from telethon.tl.custom.button import Button
from telethon.tl.custom.message import Message
from llyod.utils.tools import short_names, check_user
from telethon.events.callbackquery import CallbackQuery
from llyod.utils.manga import manga_search, series_detail, release_groups


@app.on(events.NewMessage(pattern="^[/!]([Mm][Uu](@LlyodFronteraBot)?)\s.+"))
async def manga(event: Message):
    args = event.raw_text.split(" ", 1)
    if len(args) == 1:
        await event.reply("Send a query along with the command eg. /mu <query>")
        return
    query = args[1]
    if query.lower() in short_names:
        query = short_names[query.lower()]
    results = await manga_search(query)
    buttons = []
    if not results:
        await event.reply("Nothing found")
        return
    msg = f"Mangaupdates Search results for **{query}**:"
    if len(query) > 43:
        hash = hashlib.sha1(query.encode())
        sha1 = hash.hexdigest()
        queries[sha1] = query
        query = sha1
    btns = len(results)
    if len(results) > 7:
        btns = 6
    for result in range(btns):
        title = unescape(results[result]["record"]["title"])
        buttons.append(
            [
                Button.inline(
                    text=title,
                    data=f"{results[result]['record']['series_id']}_search_{query}",
                )
            ]
        )
    x = await event.reply(msg, buttons=buttons)
    ids[f"{x.id}"] = event.sender_id


@app.on(events.CallbackQuery())
@check_user
async def manga_detail(event: CallbackQuery.Event):
    data = event.data.decode().split("_")
    if data[1] == "search":
        id = data[0]
        query = data[2]
        series = await series_detail(id)
        title = series["title"]
        alt_list = [
            series["associated"][i]["title"] for i in range(len(series["associated"]))
        ]
        alt_titles = ", ".join(alt_list) or "N/A"
        if len(alt_list) > 5:
            alt_titles = ", ".join(alt_list[:4])
        type = series["type"]
        year = series["year"]
        rating = series["bayesian_rating"]
        url = series["url"]
        desc = series["description"] or "N/A"
        desc = desc.replace("<BR>", "\n")
        if len(desc) > 400:
            desc = desc[:345] + "..."
        image = series["image"]["url"]["original"] or "N/A"
        genre_list = [
            series["genres"][i]["genre"] for i in range(len(series["genres"]))
        ]
        genres = ", ".join(genre_list) or "N/A"
        latest = series["latest_chapter"] or "N/A"
        auth_list = [
            series["authors"][i]["name"] for i in range(len(series["authors"]))
        ]
        authors = ", ".join(auth_list)
        status = series["status"] or "N/A"
        status = status.replace("<BR>", "\n")
        if series["anime"]:
            status += f"\n<b>Anime:</b> {series['anime']['start']}, {series['anime']['end'] or 'N/A'}"

        msg = f"<b>{title} ({year})</b>\n<b>Alt Names: </b><code>{alt_titles}</code>\n\n<b>Type:</b> <code>{type}</code>\n<b>Rating:</b> <code>{rating}</code>\n<b>Genres:</b> <code>{genres}</code>\n<b>Latest Chapter:</b> <code>{latest}</code>\n<b>Authors/Artists:</b> <code>{authors}</code>\n<b>Status:</b> {status}\n\n{desc}\n<a href='{image}'>&#xad</a>"
        await event.edit(
            msg,
            parse_mode="html",
            buttons=[
                [
                    Button.url("Info", url=url),
                    Button.inline("Groups", data=f"{id}_groups_{query}"),
                    Button.inline("Tags", data=f"{id}_tags_{query}"),
                ],
                [Button.inline("Recommendations", data=f"{id}_reccom_{query}")],
                [Button.inline("❮", data=f"{query}_back")],
            ],
        )

    if data[1] == "back":
        query = data[0]
        buttons = []
        msg = ""
        if is_sha1_hashed(query):
            fullquery = queries[query]
            results = await manga_search(fullquery)
            msg = f"Mangaupdates Search results for **{fullquery}**:"
        else:
            results = await manga_search(query)
            msg = f"Mangaupdates Search results for **{query}**:"
        btns = len(results)
        if len(results) > 7:
            btns = 6
        for result in range(btns):
            title = unescape(results[result]["record"]["title"])
            buttons.append(
                [
                    Button.inline(
                        text=title,
                        data=f"{results[result]['record']['series_id']}_search_{query}",
                    )
                ]
            )
        await event.edit(msg, buttons=buttons)

    if data[1] == "groups":
        id = data[0]
        query = data[2]
        results = await release_groups(id)
        names = ""
        reals = ""
        for group in results["group_list"]:
            names += f"• {group['name']}\n"
        if results["release_list"]:
            # names += f"\nLatest release for this series:-\n"
            for group in results["release_list"]:
                reals += f"• Ch.{group['chapter']} by {group['groups'][0]['name']} at {group['time_added']['as_string']}\n"
        if names == "":
            names = "Nothing\n"
        if reals == "":
            reals = "Nothing"
        await event.edit(
            f"**Groups related to this series is:-**\n{unescape(names)}\n**Latest release for this series:-**\n{unescape(reals)}",
            buttons=Button.inline("❮", data=f"{id}_search_{query}"),
        )

    if data[1] == "reccom":
        id = data[0]
        query = data[2]
        results = await series_detail(id)
        recc = ""
        for j in results["category_recommendations"]:
            recc += f"• {j['series_name']}\n"
        for i in results["recommendations"]:
            recc += f"• {i['series_name']}\n"
        if recc == "":
            recc = "Nothing"
        await event.edit(
            f"**Recommendations for {results['title']}:**\n\n{unescape(recc)}",
            buttons=Button.inline("❮", data=f"{id}_search_{query}"),
        )

    if data[1] == "tags":
        id = data[0]
        query = data[2]
        series = await series_detail(id)
        ct_list = [
            series["categories"][i]["category"]
            for i in range(len(series["categories"]))
        ]
        categories = ", ".join(ct_list) or "No Tags found"
        categories = categories.replace("/", "")
        await event.edit(
            f"**Tags for {series['title']}:**\n\n`{categories}`",
            buttons=Button.inline("❮", data=f"{id}_search_{query}"),
        )
