from aiohttp import ClientSession
from llyod.config import mal_client_id

base_url = "https://api.myanimelist.net/v2"
headers = {"X-MAL-CLIENT-ID": mal_client_id}


async def mal_anime(query):
    async with ClientSession() as session:
        anime_search = await session.get(
            url=base_url + f"/anime?q={query}&limit=7&nsfw=true", headers=headers
        )
        data = await anime_search.json()
        return data["data"]


async def get_anime(id):
    async with ClientSession() as session:
        anime = await session.get(
            url=base_url
            + f"/anime/{id}?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios",
            headers=headers,
        )
        data = await anime.json()
        return data


async def get_recom(id):
    async with ClientSession() as session:
        anime = await session.get(
            url=base_url + f"/anime/{id}?fields=recommendations", headers=headers
        )
        data = await anime.json()
        return data["recommendations"]
