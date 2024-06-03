import re
import hashlib
import markdown
from html import unescape
from telethon import events
from llyod import app, ids, queries
from llyod.utils.tools import is_sha1_hashed
from telethon.tl.custom.button import Button
from telethon.tl.custom.message import Message
from llyod.utils.tools import short_names, check_user
from telethon.events.callbackquery import CallbackQuery
from llyod.utils.dex import dex_search, dex_manga, get_chapters, dex_stats

queries = []


@app.on(events.NewMessage(pattern="^[/!]([Dd][Ee][Xx](@LlyodFronteraBot)?)\s.+"))
async def mangadex_search(event: Message):
    args = event.raw_text.split(" ", 1)
    if len(args) == 1:
        await event.reply("Send a query along with the command eg. /dex <query>")
        return
    query = args[1]
    if query.lower() in short_names:
        query = short_names[query.lower()]
    results = await dex_search(query)
    buttons = []
    if not results:
        await event.reply("Nothing found")
        return
    msg = f"Mangadex Search results for **{query}**:"
    queries.append(query)
    query = queries.index(query)
    # if len(query) > 20:
    #     hash = hashlib.sha1(query.encode())
    #     sha1 = hash.hexdigest()
    #     queries[sha1] = query
    #     query = sha1
    btns = len(results)
    if len(results) > 7:
        btns = 6
    for result in range(btns):
        what_title = results[result]["attributes"]["title"]
        if "en" in what_title:
            title = unescape(what_title["en"])
        if "ja" in what_title:
            title = unescape(what_title["ja"])
        if "ja-ro" in what_title:
            title = unescape(what_title["ja-ro"])
        buttons.append(
            [Button.inline(text=title, data=f"{results[result]['id']}_dexs_{query}")]
        )
    x = await event.reply(msg, buttons=buttons)
    ids[f"{x.id}"] = event.sender_id


@app.on(events.CallbackQuery())
@check_user
async def manga_detail(event: CallbackQuery.Event):
    data = event.data.decode().split("_")
    if data[1] == "dexs":
        id = data[0]
        query = data[2]
        series = await dex_manga(id)
        what_title = series["attributes"]["title"]
        if "en" in what_title:
            main_title = what_title["en"]
        if "ja" in what_title:
            main_title = what_title["ja"]
        if "ja-ro" in what_title:
            main_title = what_title["ja-ro"]
        # type = series['type']
        alt_titles = series["attributes"]["altTitles"] or "N/A"
        titles = []
        try:
            for i in alt_titles:
                title = None
                for lang in i:
                    if i[lang] and lang == "en":
                        title = i[lang]
                        break
                if title:
                    titles.append(title)
        except:
            pass
        alttitles = ", ".join(titles) or "N/A"
        if main_title == alttitles:
            alttitles = "N/A"
        try:
            desc = series["attributes"]["description"]["en"]
            desc = markdown.markdown(desc)
        except:
            desc = "N/A"
        demographic = series["attributes"]["publicationDemographic"] or "N/A"
        content = series["attributes"]["contentRating"] or "N/A"
        if len(desc) > 500:
            desc = desc[:500] + "..."
        genres_list = [
            tag["attributes"]["name"]["en"] for tag in series["attributes"]["tags"]
        ] or "N/A"
        genres = ", ".join(genres_list) or "N/A"
        status = series["attributes"]["status"] or "N/A"
        year = series["attributes"]["year"] or "N/A"
        for i in range(len(series["relationships"])):
            if series["relationships"][i]["type"] == "author":
                author = series["relationships"][i]["attributes"]["name"]
            if series["relationships"][i]["type"] == "cover_art":
                cover_file = series["relationships"][i]["attributes"]["fileName"]
        latest = await get_chapters(id)
        # latest = next(iter(chaps))
        cover = f"https://mangadex.org/covers/{id}/{cover_file}"
        url = f"https://mangadex.org/title/{id}"
        stats = await dex_stats(id)

        try:
            ratings = round(stats["rating"]["average"], 2)
        except:
            ratings = "N/A"
        follows = stats["follows"]
        # anilist = f"https://anilist.co/manga/{series['attributes']['links']['al']}"

        msg = f"<b>{main_title} ({year})</b>\n<b>Alt Names: </b><code>{alttitles}</code>\n\n<b>Rating:</b> <code>{ratings}</code>\n<b>Follows:</b> <code>{follows}</code>\n<b>Content Type:</b> <code>{content}</code>\n<b>Demographic:</b> <code>{demographic}</code>\n<b>Genres:</b> <code>{genres}</code>\n<b>Latest Chapter:</b> <code>{latest}</code>\n<b>Authors/Artists:</b> <code>{author}</code>\n<b>Status:</b> <code>{status}</code>\n<a href='{cover}'>&#xad</a>\n{desc}"
        await event.edit(
            msg,
            parse_mode="html",
            buttons=[
                [Button.url("Info", url=url)],
                [Button.inline("❮", data=f"{query}_dexb")],
            ],
        )

    if data[1] == "dexb":
        query = queries[int(data[0])]
        buttons = []
        # msg = ""
        results = await dex_search(query)
        msg = f"Mangdex Search results for **{query}**:"
        # if is_sha1_hashed(query):
        #     fullquery = queries[query]
        #     results = await dex_search(fullquery)
        #     msg = f'Mangdex Search results for **{fullquery}**:'
        # else:
        #     results = await dex_search(query)
        #     msg = f'Mangdex Search results for **{query}**:'
        btns = len(results)
        if len(results) > 7:
            btns = 6
        for result in range(btns):
            what_title = results[result]["attributes"]["title"]
            if "en" in what_title:
                title = unescape(what_title["en"])
            if "ja" in what_title:
                title = unescape(what_title["ja"])
            if "ja-ro" in what_title:
                title = unescape(what_title["ja-ro"])
            buttons.append(
                [
                    Button.inline(
                        text=title,
                        data=f"{results[result]['id']}_dexs_{queries.index(query)}",
                    )
                ]
            )
        await event.edit(msg, buttons=buttons)


@app.on(events.NewMessage())
async def manga_spier(event: Message):
    match = re.search("<([^>]+)>", event.raw_text)

    if match:
        query = match.group(1)
        if query.lower() in short_names:
            query = short_names[query.lower()]
        results = await dex_search(query)
        if not results:
            return
        id = results[0]["id"]
        series = await dex_manga(id)
        what_title = series["attributes"]["title"]
        if "en" in what_title:
            main_title = what_title["en"]
        if "ja" in what_title:
            main_title = what_title["ja"]
        if "ja-ro" in what_title:
            main_title = what_title["ja-ro"]
        # type = series['type']
        alt_titles = series["attributes"]["altTitles"] or "N/A"
        titles = []
        try:
            for i in alt_titles:
                title = None
                for lang in i:
                    if i[lang] and lang == "en":
                        title = i[lang]
                        break
                if title:
                    titles.append(title)
        except:
            pass
        alttitles = ", ".join(titles) or "N/A"
        if main_title == alttitles:
            alttitles = "N/A"
        try:
            desc = series["attributes"]["description"]["en"]
            desc = markdown.markdown(desc)
        except:
            desc = "N/A"
        demographic = series["attributes"]["publicationDemographic"] or "N/A"
        content = series["attributes"]["contentRating"] or "N/A"
        if len(desc) > 500:
            desc = desc[:500] + "..."
        genres_list = [
            tag["attributes"]["name"]["en"] for tag in series["attributes"]["tags"]
        ] or "N/A"
        genres = ", ".join(genres_list) or "N/A"
        status = series["attributes"]["status"] or "N/A"
        year = series["attributes"]["year"] or "N/A"
        for i in range(len(series["relationships"])):
            if series["relationships"][i]["type"] == "author":
                author = series["relationships"][i]["attributes"]["name"]
            if series["relationships"][i]["type"] == "cover_art":
                cover_file = series["relationships"][i]["attributes"]["fileName"]
        latest = await get_chapters(id)
        cover = f"https://mangadex.org/covers/{id}/{cover_file}"
        url = f"https://mangadex.org/title/{id}"
        stats = await dex_stats(id)
        try:
            ratings = round(stats["rating"]["average"], 2)
        except:
            ratings = "N/A"
        follows = stats["follows"]
        btns = [Button.url("More Info", url=url)]
        links = series["attributes"]["links"]
        if links:
            if "al" in links:
                btns.append(
                    Button.url(
                        "AniList",
                        url=f"https://anilist.co/manga/{series['attributes']['links']['al']}",
                    )
                )
            if "mal" in links:
                btns.append(
                    Button.url(
                        "MyAnimeList",
                        url=f"https://myanimelist.net/manga/{series['attributes']['links']['mal']}",
                    )
                )
            # anilist = f"https://anilist.co/manga/{series['attributes']['links']['al']}"

        msg = f"<b>{main_title} ({year})</b>\n<b>Alt Names: </b><code>{alttitles}</code>\n\n<b>Rating:</b> <code>{ratings}</code>\n<b>Follows:</b> <code>{follows}</code>\n<b>Content Type:</b> <code>{content}</code>\n<b>Demographic:</b> <code>{demographic}</code>\n<b>Genres:</b> <code>{genres}</code>\n<b>Latest Chapter:</b> <code>{latest}</code>\n<b>Authors/Artists:</b> <code>{author}</code>\n<b>Status:</b> <code>{status}</code>\n<a href='{cover}'>&#xad</a>\n{desc}"
        await event.reply(msg, parse_mode="html", buttons=[btns])
