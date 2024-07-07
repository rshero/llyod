import os
import re
import shlex
import asyncio
import traceback
from typing import Tuple
from telethon import events
from llyod import app, logger
from llyod.config import SAUCE_KEY
from telethon.tl.custom.button import Button
from telethon.tl.custom.message import Message
from pysaucenao.containers import TwitterSource
from pysaucenao import (
    SauceNao,
    PixivSource,
    AnimeSource,
    MangaSource,
    VideoSource,
    BooruSource,
)

saucenao = SauceNao(api_key=SAUCE_KEY, min_similarity=60, results_limit=2)
media_types = (".jpeg", ".jpg", ".png", ".gif", ".webp")


@app.on(
    events.NewMessage(pattern=r"^[/!][Ss][Aa][Uu][Cc][Ee](@LlyodFronteraBot)?(\s.*)?")
)
async def get_sauce(event: Message):
    args = event.raw_text.split(" ", 1)
    if event.is_reply:
        reply = await event.get_reply_message()
        if reply.media:
            try:
                media = await reply.download_media()
                if media.endswith(".mp4"):
                    new_media = media.replace("mp4", "gif")
                    await runcmd(f"ffmpeg -y -i {media} {new_media}")
                    os.remove(media)
                    media = new_media
            except:
                await event.reply(
                    "Reply to an image or send an url with it. eg. `/sauce <image url>`"
                )
                return
        else:
            await event.reply(
                "Reply to an image or send an url with it. eg. `/sauce <image url>`"
            )
            return

    elif len(args) == 2:
        if args[1].endswith(media_types):
            media = args[1]
        else:
            await event.reply(
                "Reply to an image or send an url with it. eg. `/sauce <image url>`"
            )
            return
    else:
        await event.reply(
            "Reply to an image or send an url with it. eg. `/sauce <image url>`"
        )
        return

    tm = await event.reply("`Searching for sauce...🍝`")
    msg = ""
    btns = []
    try:
        if os.path.isfile(media):
            sauce = await saucenao.from_file(media)
        else:
            sauce = await saucenao.from_url(media)

        if sauce.results:
            result = sauce.results[0]
            if isinstance(result, PixivSource):
                msg += f"**{result.title}**\n\n"
                msg += f"**Artist:** `{result.author_name}`\n"
                if "characters" in result.data:
                    msg += f"**Characters:** `{result.characters}`\n"
                if "material" in result.data:
                    msg += f"**Material:** `{result.material}`\n"
                if urls := result.urls:
                    for url in urls:
                        url_name = re.search(r"https://(.*?)/", url)
                        names = url_name.group(1).split(".")
                        name = (
                            names[1]
                            if len(names) > 2 and names[0] == "www"
                            else names[0]
                        )
                        btns.append(
                            Button.url(
                                name.replace("yande", "yandere").capitalize(), url
                            )
                        )

            elif isinstance(result, AnimeSource):
                msg += f"**{result.title} - Ep. {result.episode}**\n\n"
                msg += f"**Est. Time:** `{result.timestamp}`\n"
                msg += f"**year:** `{result.year}`\n"
                if urls := result.urls:
                    for url in urls:
                        url_name = re.search(r"https://(.*?)/", url)
                        names = url_name.group(1).split(".")
                        name = (
                            names[1]
                            if len(names) > 2 and names[0] == "www"
                            else names[0]
                        )
                        btns.append(
                            Button.url(
                                name.replace("yande", "yandere").capitalize(), url
                            )
                        )
            elif isinstance(result, MangaSource):
                msg += f"**Title: {result.title} {result.chapter}**\n\n"
                msg += f"**Author:** `{result.author_name}`\n"
                if urls := result.urls:
                    for url in urls:
                        url_name = re.search(r"https://(.*?)/", url)
                        names = url_name.group(1).split(".")
                        name = (
                            names[1]
                            if len(names) > 2 and names[0] == "www"
                            else names[0]
                        )
                        btns.append(
                            Button.url(
                                name.replace("yande", "yandere").capitalize(), url
                            )
                        )
            elif isinstance(result, VideoSource):
                msg += f"**{result.title} - Ep. {result.episode}**\n\n"
                msg += f"**Est. Time:** `{result.timestamp}`\n"
                msg += f"**year:** `{result.year}`\n"
                if urls := result.urls:
                    for url in urls:
                        url_name = re.search(r"https://(.*?)/", url)
                        names = url_name.group(1).split(".")
                        name = (
                            names[1]
                            if len(names) > 2 and names[0] == "www"
                            else names[0]
                        )
                        btns.append(
                            Button.url(
                                name.replace("yande", "yandere").capitalize(), url
                            )
                        )
            elif isinstance(result, BooruSource):
                msg += f"**{result.title}**\n\n"
                msg += f"**Author:** `{result.author_name}`\n"
                if urls := result.urls:
                    for url in urls:
                        url_name = re.search(r"https://(.*?)/", url)
                        names = url_name.group(1).split(".")
                        name = (
                            names[1]
                            if len(names) > 2 and names[0] == "www"
                            else names[0]
                        )
                        btns.append(
                            Button.url(
                                name.replace("yande", "yandere").capitalize(), url
                            )
                        )
            elif isinstance(result, TwitterSource):
                msg += f"**{result.title}**\n\n"
                msg += f"**Author:** `{result.author_name}`\n"
                if urls := result.urls:
                    for url in urls:
                        url_name = re.search(r"https://(.*?)/", url)
                        names = url_name.group(1).split(".")
                        name = (
                            names[1]
                            if len(names) > 2 and names[0] == "www"
                            else names[0]
                        )
                        btns.append(
                            Button.url(
                                name.replace("yande", "yandere").capitalize(), url
                            )
                        )
            else:
                msg += f"**Title:** {result.title}\n\n"
                # msg += f"**Author:** {result.data.get('author') if result.data.get('author') else result.data.get('artist')}\n"
                if result.data.get("author"):
                    msg += f"**Author:** {result.data.get('author')}\n"
                else:
                    msg += f"**Artist:** {result.data.get('artist')}\n"
                if urls := result.urls:
                    for url in urls:
                        url_name = re.search(r"https://(.*?)/", url)
                        names = url_name.group(1).split(".")
                        name = (
                            names[1]
                            if len(names) > 2 and names[0] == "www"
                            else names[0]
                        )
                        btns.append(
                            Button.url(
                                name.replace("yande", "yandere").capitalize(), url
                            )
                        )
            if len(sauce.results) > 1:
                second_result = sauce.results[1]
                if isinstance(second_result, BooruSource):
                    if second_result.similarity >= 80:
                        msg += f"**Characters:** `{', '.join(second_result.characters) or 'Original'}`\n"
                        msg += f"**Material:** `{', '.join(second_result.material) or 'None'}`"
                        if urls := second_result.urls:
                            for url in urls:
                                url_name = re.search(r"https://(.*?)/", url)
                                names = url_name.group(1).split(".")
                                name = (
                                    names[1]
                                    if len(names) > 2 and names[0] == "www"
                                    else names[0]
                                )
                                btns.append(
                                    Button.url(
                                        name.replace("yande", "yandere").capitalize(),
                                        url,
                                    )
                                )
        else:
            msg += "**No results found.**"

    except Exception as e:
        logger.error(traceback.format_exc())
        msg += f"**Error:** `API ERROR TRY AGAIN LATER`"

    if btns:
        await tm.edit(msg, buttons=btns)
    else:
        await tm.edit(msg)

    try:
        if os.path.isfile(media):
            os.remove(media)
    except:
        pass


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """run command in terminal"""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )
