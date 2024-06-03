import markdown
from llyod import app
from asyncio import sleep
from html import unescape
from telethon import events
from llyod.utils.tools import short_names
from llyod.utils.tools import is_sha1_hashed
from telethon.tl.custom.button import Button
from telethon.tl.custom.message import Message
from telethon.tl.types import InputWebDocument
from telethon.tl.types import DocumentAttributeImageSize
from telethon.events.inlinequery import InlineQuery
from telethon.events.callbackquery import CallbackQuery
from llyod.utils.comic_api import comic_search, get_comic
from llyod.utils.dex import dex_search, dex_manga, get_chapters, dex_stats


@app.on(events.InlineQuery)
async def inlinequery(event: InlineQuery.Event):
    "Inline handlers for llyod"

    query = event.text
    if query:
        return

    results: List = []
    inline_help_dicts = [
        {
            "title": "dex",
            "description": "MangaDex Search",
            "message_text": "Click the button below to get search manga on MangaDex",
            "thumb_urL": "https://telegra.ph/file/8bf8527dfd77de0034c65.jpg",
            "keyboard": ".dex ",
        },
        {
            "title": "comic",
            "description": "Comick Search",
            "message_text": "Click the button below to get search manga on Comick",
            "thumb_urL": "http://telegra.ph/file/abd02b50ba0c6cd2fe70d.jpg",
            "keyboard": ".comic ",
        },
    ]
    for ihelp in inline_help_dicts:
        results.append(
            await event.builder.article(
                title=ihelp["title"],
                description=ihelp["description"],
                text=ihelp["message_text"],
                thumb=InputWebDocument(
                    ihelp["thumb_urL"], size=50, mime_type="image/jpeg", attributes=[]
                ),
                buttons=Button.switch_inline(
                    text="Click Here", query=ihelp["keyboard"], same_peer=True
                ),
            )
        )
    await event.answer(
        results, cache_time=5, switch_pm="More Options?", switch_pm_param="help"
    )


@app.on(events.InlineQuery(pattern="^[.]([Dd][Ee][Xx])\s.+"))
async def dex(event: InlineQuery.Event):
    "MangaDex Inline Search"

    query = event.text
    # if not query:
    #     return
    # if not query.startswith(".dex"):
    #     return
    try:
        query = query.split(" ", 1)[1]
    except:
        return
    if not query:
        return
    if query.lower() in short_names:
        query = short_names[query.lower()]

    results = await dex_search(query)
    mangaa = []

    if not results:
        return

    btns = len(results)
    if len(results) > 7:
        btns = 4

    for result in range(btns):
        id = results[result]["id"]
        what_title = results[result]["attributes"]["title"]
        if "en" in what_title:
            title = unescape(what_title["en"])
        if "ja" in what_title:
            title = unescape(what_title["ja"])
        if "ja-ro" in what_title:
            title = unescape(what_title["ja-ro"])
        # title = unescape(results[result]['title'])
        series = await dex_manga(id)
        alt_titles = series["attributes"]["altTitles"] or "N/A"

        desc = series["attributes"]["description"]
        if not "en" in desc:
            desc = "N/A"
            sdesc = "N/A"
        else:
            desc = desc["en"]
            sdesc = desc[:100]
            desc = markdown.markdown(desc)
        # try:
        #     desc = series['attributes']['description']['en']
        #     desc = markdown.markdown(desc)
        # except:
        #     desc = "N/A"

        titles = []
        try:
            for i in alt_titles:
                ttle = None
                for lang in i:
                    if i[lang] and lang == "en":
                        ttle = i[lang]
                        break
                if ttle:
                    titles.append(ttle)
        except:
            pass
        alttitles = ", ".join(titles) or "N/A"
        if title == alttitles:
            alttitles = "N/A"

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
        # anilist = f"https://anilist.co/manga/{series['attributes']['links']['al']}"
        msg = f"<b>{title} ({year})</b>\n<b>Alt Names: </b><code>{alttitles}</code>\n\n<b>Rating:</b> <code>{ratings}</code>\n<b>Follows:</b> <code>{follows}</code>\n<b>Content Type:</b> <code>{content}</code>\n<b>Demographic:</b> <code>{demographic}</code>\n<b>Genres:</b> <code>{genres}</code>\n<b>Latest Chapter:</b> <code>{latest}</code>\n<b>Authors/Artists:</b> <code>{author}</code>\n<b>Status:</b> <code>{status}</code>\n<a href='{cover}'>&#xad</a>\n{desc}"
        mangaa.append(
            await event.builder.article(
                title=title,
                thumb=InputWebDocument(cover, 0, "image/jpeg", []),
                description=sdesc,
                text=msg,
                parse_mode="html",
                buttons=[
                    [
                        Button.url("Info", url=url),
                        Button.switch_inline(
                            "Search again", query=".dex ", same_peer=True
                        ),
                    ]
                ],
            )
        )
    try:
        await event.answer(mangaa, cache_time=5)
    except:
        return


@app.on(events.InlineQuery(pattern="^[.]([Cc][Oo][Mm][Ii][Cc])\s.+"))
async def comick(event: InlineQuery.Event):
    "Comick Inline Search"

    query = event.text

    try:
        query = query.split(" ", 1)[1]
    except:
        return

    if not query:
        return
    if query.lower() in short_names:
        query = short_names[query.lower()]

    results = await comic_search(query)
    comics = []

    if not results:
        return

    btns = len(results)
    if len(results) > 7:
        btns = 4

    for result in range(btns):
        title = results[result]["title"]
        slug = results[result]["slug"]
        series = await get_comic(slug)
        title = series["comic"]["title"]
        status = series["comic"]["status"]
        status = {1: "Ongoing", 2: "Completed", 3: "Cancelled", 4: "On Hiatus"}.get(
            status, "N/A"
        )
        rating = series["comic"]["bayesian_rating"]
        file_key = series["comic"]["md_covers"][0]["b2key"]
        cover = f"https://meo.comick.pictures/{file_key}"
        url = f"https://comick.app/comic/{slug}"
        genres_list = [
            i["md_genres"]["name"] for i in series["comic"]["md_comic_md_genres"]
        ]
        genres = ", ".join(genres_list) or "N/A"
        alt_titles = [al["title"] for al in series["comic"]["md_titles"]]
        alts = ", ".join(alt_titles) or "N/A"
        try:
            desc = series["comic"]["desc"]
            sdesc = desc[:100]
            desc = markdown.markdown(desc, output_format="html")
        except:
            desc = "N/A"
            sdesc = "N/A"
        last_chap = series["comic"]["last_chapter"] or "N/A"
        content_rating = series["comic"]["content_rating"].capitalize() or "N/A"
        demographic = series["comic"]["demographic"] or "N/A"
        demographic = {1: "Shonen", 2: "Shojo", 3: "Seinen", 4: "Josei"}.get(
            demographic, "N/A"
        )
        year = series["comic"]["year"] or "N/A"
        authors_list = [a["name"] for a in series["authors"]]
        authors = ", ".join(authors_list) or "N/A"
        artist_list = [a["name"] for a in series["artists"]]
        artists = ", ".join(artist_list) or "N/A"

        msg = f"<b>{title} (<code>{year}</code>)</b>\n\n"
        msg += f"<b>Alt Names:</b> <code>{alts}</code>\n"
        msg += f"<b>Rating:</b> <code>{rating}</code>\n"
        msg += f"<b>Content Type:</b> <code>{content_rating}</code>\n"
        msg += f"<b>Demographic:</b> <code>{demographic}</code>\n"
        msg += f"<b>Genres:</b> <code>{genres}</code>\n"
        msg += f"<b>Last Chapter:</b> <code>{last_chap}</code>\n"
        msg += f"<b>Status:</b> <code>{status}</code>\n"
        msg += f"<b>Authors:</b> <code>{authors}</code>\n"
        if authors != artists:
            msg += f"<b>Artists:</b> <code>{artists}</code>\n"
        msg += f"\n<a href='{cover}'>&#xad</a>"
        msg += f"{desc}"

        comics.append(
            await event.builder.article(
                title=title,
                thumb=InputWebDocument(cover, 0, "image/jpeg", []),
                description=sdesc,
                text=msg,
                parse_mode="html",
                buttons=[
                    [
                        Button.url("Info", url=url),
                        Button.switch_inline(
                            "Search again", query=".comic ", same_peer=True
                        ),
                    ]
                ],
            )
        )
    try:
        await event.answer(comics, cache_time=5)
    except:
        return


# todo
# add more inline search options
# and make separate functions for each search
