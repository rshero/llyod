import re
from telethon import events
from llyod import app, ids, queries
from telethon.tl.custom.button import Button
from telethon.tl.custom.message import Message
from llyod.utils.tools import short_names, check_user
from telethon.events.callbackquery import CallbackQuery
from llyod.utils.mal_tool import mal_anime, get_anime, get_recom

queries = []

@app.on(events.NewMessage(pattern="^[/!]([Aa][Nn][Ii][Mm][Uu](@LlyodFronteraBot)?)\s.+"))
async def mal_anime_search(event: Message):
    args = event.raw_text.split(" ", 1)
    if len(args) == 1:
        await event.reply('Send a query along with the command eg. /animu <query>')
        return
    query = args[1]
    if query.lower() in short_names:
        query = short_names[query.lower()]
    try:
        results = await mal_anime(query)
    except:
        await event.reply('**API Error:** `Try again later`')
        return
    buttons = []
    if not results:
        await event.reply('Nothing found')
        return
    msg = f'MyAnimeList Search results for **{query}**:'
    queries.append(query)
    query = queries.index(query)
    for result in range(len(results)):
        title = results[result]['node']['title']
        buttons.append([Button.inline(text=title, data=f"{results[result]['node']['id']}_mala_{query}")])
    x = await event.reply(msg, file="https://telegra.ph/file/33067bb12f7165f8654f9.mp4", buttons=buttons)
    ids[f"{x.id}"] = event.sender_id

@app.on(events.CallbackQuery())
@check_user
async def mal_detail(event: CallbackQuery.Event):
    data = event.data.decode().split("_")
    if data[1] == 'mala':
        id = data[0]
        query = data[2]
        series = await get_anime(id)
        msg = ""
        title = series['title']
        image = series['main_picture']['large']
        alts = series['alternative_titles'] or "N/A"
        alt_titles = ""
        if alts["synonyms"] != []:
            alt_titles += ", ".join(alts['synonyms'])

        if "en" in alts:
            if alts['en'].lower() != title.lower() and alts['en'] != '':
                alt_titles += f", {alts['en']}"

        if "ja" in alts:
            if alts['ja'].lower() != title.lower() and alts['ja'] != '':
                alt_titles += f", {alts['ja']}"
        try:
            aired = series['start_date']
        except:
            aired = "N/A"
        
        try:
            premiered_y = series['start_season']['year']
            premiered_s = series['start_season']['season'].capitalize()
        except:
            premiered_y = "N/A"
            premiered_s = "N/A"
        
        try:
            broadcast_d = series['broadcast']['day_of_the_week'].capitalize() or "N/A"
            broadcast_t = series['broadcast']['start_time'] or "N/A"
        except:
            broadcast_d = "N/A"
            broadcast_t = "N/A"
            
        source = series['source'].replace("_", " ").capitalize() or "N/A"
        eps_nos = series['num_episodes'] or "No idea"
        eps_dur = round(int(series['average_episode_duration']) / 60) or "N/A"
        dur_txt = f"{eps_dur} min. per ep." or "N/A"
        try:
            if float(eps_dur) > 60:
                left_time = round(float(eps_dur) - 60)
                dur_txt = f"1 hr. {left_time} min."
        except:
            pass
        if "rating" in series:
            rating = series['rating'].upper().replace('_', '-')
        else:
            rating = "N/A"
        list_studios = [i['name'] for i in series['studios']] or "N/A"
        studios = ", ".join(list_studios) or "N/A"
        url = url=f"https://myanimelist.net/anime/{id}"
        desc = series['synopsis'] or "N/A"
        if len(desc) > 400:
            desc = desc[:350] + "..."
        if "mean" in series:
            score = series['mean']
        else:
            score = "N/A"

        try:
            rank = f"#{series['rank']}"
        except:
            rank = ""
        popl = series['popularity'] or "N/A"
        nsfw = series['nsfw']
        if nsfw == "white":
            nsfw = "False"
        elif nsfw == "gray":
            nsfw = "True"
        else:
            nsfw = "N/A"
        type = series['media_type'].upper() or "N/A"
        status = series['status'].replace("_", " ").capitalize() or "N/A"
        genres_list = [i['name'] for i in series['genres']]
        genres = ", ".join(genres_list) or "N/A"
        
        msg += f"**{title}** (`{premiered_s} {premiered_y}`)\n\n"
        if alt_titles != "":
            msg += f"**Alt titles:** `{alt_titles.strip(', ')}`\n"
        if rank != "":
            msg += f"**Rank:** `{rank}`\n"
        msg += f"**NSFW:** `{nsfw}`\n"
        msg += f"**Type:** `{type}`\n"
        msg += f"**Score:** `{score}`\n"
        msg += f"**Source:** `{source}`\n"
        msg += f"**Status:** `{status}`\n"
        msg += f"**Airing Info:** `{aired}`\n"
        if "currently" in status.lower().split(" "):
            msg += f"**Broadcast:** `{broadcast_d} - {broadcast_t} JST`\n"
        if eps_nos == "No idea":
            msg += f"**Episodes:** `{eps_nos}`\n"
        else:
            msg += f"**Episodes:** `{eps_nos} / {dur_txt}`\n"
        msg += f"**Studios:** `{studios}`\n"
        msg += f"**Genres:** `{genres}`\n"
        msg += f"**Rating:** `{rating}`\n"
        msg += f"\n__{desc}__"

        buttons = [[Button.url("More Info",url=url), Button.inline("Recommendations", data=f"{query}_mreco_{id}")], [Button.inline("❮", data=f"{query}_mback")]]
        await event.edit(msg, file=image, buttons=buttons)
    
    if data[1] == 'mback':
        query = queries[int(data[0])]
        buttons = []
        msg = f'MyAnimeList Search results for **{query}**:'
        results = await mal_anime(query)
        for result in range(len(results)):
            title = results[result]['node']['title']
            buttons.append([Button.inline(text=title, data=f"{results[result]['node']['id']}_mala_{queries.index(query)}")])
        x = await event.edit(msg, file="https://telegra.ph/file/33067bb12f7165f8654f9.mp4", buttons=buttons)

    if data[1] == 'mreco':
        id = data[2]
        query = data[0]
        recom = await get_recom(id)
        recoms = ""
        if not recom:
            recoms += "`No Recommendations`"
        else:
            for rec in recom:
                recoms += f"• **[{rec['node']['title']}](https://myanimelist.net/anime/{rec['node']['id']})**\n"
        await event.edit(recoms, buttons=[Button.inline("❮", data=f"{id}_mala_{query}")])

@app.on(events.NewMessage())
async def anime_spier(event: Message):
    match = re.search('{([^>]+)}', event.raw_text)

    if match:
        query = match.group(1)
        if query.lower() in short_names:
            query = short_names[query.lower()]
        try:
            results = await mal_anime(query)
        except:
            return
        buttons = []
        if not results:
            return
        msg = f'MyAnimeList Search results for **{query}**:'
        queries.append(query)
        query = queries.index(query)
        for result in range(len(results)):
            title = results[result]['node']['title']
            buttons.append([Button.inline(text=title, data=f"{results[result]['node']['id']}_mala_{query}")])
        x = await event.reply(msg, file="https://telegra.ph/file/33067bb12f7165f8654f9.mp4", buttons=buttons)
        ids[f"{x.id}"] = event.sender_id