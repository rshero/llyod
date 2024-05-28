from aiohttp import ClientSession

async def dex_search(query):
    async with ClientSession() as session:
        r = await session.get(f'https://api.mangadex.org/manga?limit=10&title={query}&includedTagsMode=AND&excludedTagsMode=OR&contentRating%5B%5D=safe&contentRating%5B%5D=suggestive&contentRating%5B%5D=erotica&contentRating%5B%5D=pornographic&order%5Brelevance%5D=desc')
        data = await r.json()
        return data["data"]

async def dex_manga(id):
    async with ClientSession() as session:
        r = await session.get(f'https://api.mangadex.org/manga/{id}?includes%5B%5D=cover_art&includes%5B%5D=author&includes%5B%5D=artist&includes%5B%5D=tag', params="includes[]=cover_art author artist tag")
        data = await r.json()
        return data["data"]

# async def get_chapters(id):
#     async with ClientSession() as session:
#         r = await session.get(f'https://api.mangadex.org/manga/{id}/aggregate?translatedLanguage%5B%5D=en')
#         data = await r.json()
#         chaps = ""
#         try:
#         # chaps = data['volumes']['none']['chapters']
#             vol = data['volumes']
#             key = next(iter(vol))
#             chaps = data['volumes'][key]['chapters']
#         except:
#             chaps += "Nothing"
#         return chaps

async def get_chapters(id):
    async with ClientSession() as session:
        r = await session.get(f'https://api.mangadex.org/chapter/{id}')
        data = await r.json()
        return data['data']['attributes']['chapter']
        
async def dex_stats(id):
    async with ClientSession() as session:
        r = await session.get(f'https://api.mangadex.org/statistics/manga/{id}')
        data = await r.json()
        stats = data['statistics'][id]
        return stats
