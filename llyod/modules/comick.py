import markdown
from html import unescape
from telethon import events
from llyod import app, ids, queries
from llyod.utils.tools import is_sha1_hashed
from telethon.tl.custom.button import Button
from telethon.tl.custom.message import Message
from llyod.utils.tools import short_names, check_user
from telethon.events.callbackquery import CallbackQuery
from llyod.utils.comic_api import comic_search, get_comic

queries = []
slugs = []


@app.on(
    events.NewMessage(pattern=r"^[/!]([Cc][Oo][Mm][Ii][Cc](@LlyodFronteraBot)?)\s.+")
)
async def comick_search(event: Message):
    args = event.raw_text.split(" ", 1)
    if len(args) == 1:
        await event.reply("Send a query along with the command eg. /comic <query>")
        return
    query = args[1]
    if query.lower() in short_names:
        query = short_names[query.lower()]
    results = await comic_search(query)
    buttons = []
    if not results:
        await event.reply("Nothing found")
        return
    msg = f"Comick Search results for **{query}**:"
    queries.append(query)
    query = queries.index(query)

    for result in range(len(results)):
        title = results[result]["title"]
        slug = results[result]["slug"]
        slugs.append(results[result]["slug"])
        id = slugs.index(slug)
        buttons.append([Button.inline(text=title, data=f"{id}_comics_{query}")])
    x = await event.reply(msg, buttons=buttons)
    ids[f"{x.id}"] = event.sender_id


@app.on(events.CallbackQuery())
@check_user
async def comic_detail(event: CallbackQuery.Event):
    data = event.data.decode().split("_")
    if data[1] == "comics":
        id = data[0]
        query = data[2]
        slug = slugs[int(id)]
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
        # genres_list = [i['name'] for i in series['genres']] # api changes broke this
        genres_list = [
            i["md_genres"]["name"] for i in series["comic"]["md_comic_md_genres"]
        ]
        genres = ", ".join(genres_list) or "N/A"
        alt_titles = [al["title"] for al in series["comic"]["md_titles"]]
        alts = ", ".join(alt_titles) or "N/A"
        # nsfw = series['comic']['hentai'] or "None"
        try:
            desc = series["comic"]["desc"]
            desc = markdown.markdown(desc, output_format="html")
        except:
            desc = "N/A"
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
        # msg += f"<b>NSFW:</b> <code>{nsfw}</code>\n"
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

        await event.edit(
            msg,
            parse_mode="html",
            buttons=[
                [Button.url("Info", url=url)],
                [Button.inline("❮", data=f"{id}_comicb_{query}")],
            ],
        )

    if data[1] == "comicb":
        query = queries[int(data[2])]
        buttons = []
        # msg = ""
        results = await comic_search(query)
        msg = f"Comick Search results for **{query}**:"

        for result in range(len(results)):
            title = results[result]["title"]
            slug = results[result]["slug"]
            id = slugs.index(slug)
            buttons.append(
                [Button.inline(text=title, data=f"{id}_comics_{queries.index(query)}")]
            )
        x = await event.edit(msg, buttons=buttons)
