from llyod import mu_token
from aiohttp import ClientSession


async def manga_search(query):
    async with ClientSession() as sess:
        r = await sess.post("https://api.mangaupdates.com/v1/series/search", json={'search': query}, headers={'Authorization':'Bearer '+ mu_token})
        data = await r.json()
        results = data['results']
        return results

async def series_detail(id):
    async with ClientSession() as msess:
        r = await msess.get(f'https://api.mangaupdates.com/v1/series/{id}', headers={'Authorization':'Bearer '+ mu_token})
        data = await r.json()
        return data

async def release_groups(id):
    async with ClientSession() as ress:
        r = await ress.get(f'https://api.mangaupdates.com/v1/series/{id}/groups', headers={'Authorization':'Bearer '+ mu_token})
        data = await r.json()
        return data

async def search_authors(query):
    async with ClientSession() as ress:
        r = await ress.post("https://api.mangaupdates.com/v1/authors/search", json={'search': query}, headers={'Authorization':'Bearer '+ mu_token})
        data = await r.json()
        results = data['results']
        return results

async def author_detail(id):
    async with ClientSession() as ress:
        r = await ress.get(f'https://api.mangaupdates.com/v1/authors/{id}', headers={'Authorization':'Bearer '+ mu_token})
        data = await r.json()
        return data

async def list_series(id):
    async with ClientSession() as ress:
        r = await ress.post(f'https://api.mangaupdates.com/v1/authors/{id}/series', json={'orderby': 'year'}, headers={'Authorization':'Bearer '+ mu_token})
        data = await r.json()
        return data