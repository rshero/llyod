from llyod import app
from llyod.modules import *
from telethon import events, tl
from telethon.tl.custom.button import Button
from telethon.tl.custom.message import Message
from telethon.events.callbackquery import CallbackQuery

start_msg = """
Hello {}!

I'm an advanced bot for Anime & Manga. Currently in developement :D
Read The Greatest Estate Developer for my stupid lore."
"""
help_msg = """
Some of the working commands right now:-

• /mu <query> to get manga result from mangaupdates.
• /author <query> to search for authors.
• /comic <query> to get manga result from Comick.
• /dex <query> to get manga result from MangaDex.
• /animu <query> to get anime result from MyAnimeList.
• /novel <query> to get novel search results.
• /sauce <reply/img url> to get saucenao results.
• /latestchps type (manhwa manga manhua) shows latest released chapters from comick

• **<**manga title**>** Adding something like this will reply to the first result fom mangadex.
• **{**anime title**}** Adding something like this will reply with MyAnimeList search results.
"""

@app.on(events.NewMessage(pattern="^[!/]start$"))
async def main(event: Message):
    sender = await event.get_sender()
    x = await event.reply(start_msg.format(sender.first_name), buttons=[Button.url('Help', url='http://t.me/LlyodFronteraBot?start=help')])

@app.on(events.NewMessage())
async def help(event: Message):
    args = event.raw_text.split(" ", 1)
    if (len(args) == 1 and args[0].lower() in ["/help", "/help@llyodfronterabot"]) or \
        (len(args) == 2 and args[0].lower() == "/start" and args[1] == "help"):
        await event.reply(help_msg, buttons=[Button.switch_inline('Try inline', query=' ', same_peer=True)])




app.run_until_disconnected()