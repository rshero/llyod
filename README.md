<div align="center">
<img src="https://i.ibb.co/PskGP8H/image.png" alt="llyod" height="300" widht="300"/>
<h1>Llyod</h1>

**[<kbd> <br>Mangaite<br> </kbd>][Mangaite]** 
**[<kbd> <br>Llyod<br> </kbd>][Llyod]** 
**[<kbd> <br>AniStash<br> </kbd>][stash]** 

<p>An advance telegram bot for manga, comic, novels etc.</p>

[![Stars]][Stargazer] [![Forks]][Fork] [![Repo-Size]][Size] 
[![License]][License-url] [![Python]][Python-url]
</div>

Llyod is a telegram bot that displays information related to any manga, comic, novel etc. It also displays about it's release, author, adaptation and more. You can find it here [@LlyodFronteraBot][Llyod] Support is [@mangaite][Mangaite].

It's built on python using telethon also utilizing some other libraries and APIs. Credits below.

# Features
### Llyod commands and what they do
```

• /start: Get a friendly hello message.
• /help: get this message below with the commands.
• /mu <query>: to get manga result from mangaupdates.
• /author <query>: to search for authors.
• /comic <query>: to get manga result from Comick.
• /dex <query>: to get manga result from MangaDex.
• /animu <query>: to get anime result from MyAnimeList.
• /novel <query>: to get novel search results.
• /sauce <reply/img url>: to get saucenao results.
• /latestchps: type (manhwa manga manhua) shows latest released chapters from comick

• <manga title> Adding something like this will reply to the first result fom mangadex.
• {anime title} Adding something like this will reply with MyAnimeList search results.
```
### Inline Usage
#### Copy and paste the bot username into your msg box as shown below
```
@LlyodFronteraBot  to show the menu
@LlyodFronteraBot  .dex for mangadex search
@LlyodFronteraBot  .comic for comick.app search
```

# Deploy
### If you want to deploy the bot for yourself follow the instructions below
> Note: Currently you can only deploy it on a vps.

- `git clone https://github.com/rshero/llyod`
- `cd llyod`
- `pip install -U -r rerquirements.txt`
- `cd llyod` (Bot Directory)
- `cp sample_config.py config.py`
- Fill all your variables inside config.py. Variable guide is below
- `cd ..` (come out of the bot directory)
- `python3 -m llyod` (Run the bot as a module) 
- 😎 Enjoy!

> Tip: Depending on your system these commands may need some alteration.

# Variables
- To get `api_id` and `api_hash` for telegram - https://my.telegram.org/auth sign in here.
- To get `bot_token` [@botfather](https://t.me/BotFather) pm this bot and create a new bot and copy the token from here.
- For `mu_token` short for mangaupdates follow the guide here [Mangaupdates API](https://api.mangaupdates.com/#tag/account/operation/login) 
- For `mal_client_id` follow the guide here [MAL](https://myanimelist.net/clubs.php?cid=13727)
- For `SAUCE_KEY` [Go Here](https://saucenao.com/user.php?page=search-api) Create a saucenao account if you haven't

> You can ask for help about these on our support chat.

# Credits
* [Llyod Reference](https://comic.naver.com/webtoon/list?titleId=777767)
* [Lonami](https://github.com/LonamiWebs/) for [Telethon.](https://github.com/LonamiWebs/Telethon)
* [MyAnimeList](https://myanimelist.net/)
* [MangaDex](https://mangadex.org)
* [Comick](https://comick.cc)
* [MangaUpdates](https://mangaupdates.com)
* [Saucenao](https://saucenao.com)
* [WLN](https://www.wlnupdates.com)

<hr>

# LICENSE
[![License](https://www.gnu.org/graphics/agplv3-155x51.png)](LICENSE)   
Llyod is licensed under [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html) v3 or later.

<!--------{Badges}--------->

[Stars]: https://img.shields.io/github/stars/rshero/llyod?style=flat-square&logo=coveralls&color=C9A0D3
[Forks]: https://img.shields.io/github/forks/rshero/llyod?style=flat-square&logo=trailforks&color=C9A0D3
[Repo-Size]: https://img.shields.io/github/repo-size/rshero/llyod?style=flat-square&logo=liquibase&color=C9A0D3
[License]: https://img.shields.io/github/license/rshero/llyod?style=flat-square&logo=bookstack&color=C9A0D3
[Python]: https://img.shields.io/badge/Python-v3.12.12-blue?style=flat-square&logo=python&color=C9A0D3

<!--------{Links}--------->
[Stargazer]: https://github.com/rshero/llyod/stargazers
[Python-url]: https://www.python.org/
[Fork]: https://github.com/rshero/llyod/fork
[Size]: https://github.com/rshero/llyod/
[License-url]: https://github.com/rshero/llyod/blob/main/LICENSE
[Mangaite]: https://t.me/mangaite
[stash]: https://t.me/ItsStash
[Llyod]: https://t.me/LlyodFronteraBot