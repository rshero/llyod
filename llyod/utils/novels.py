import asyncio
from aiohttp import ClientSession

base_url = "https://www.wlnupdates.com/api"
headers = {
	'Accept': 'application/json',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

async def search_results(query):
	data = {'title': query, 'mode': 'search-title'}
	async with ClientSession() as session:
		r = await session.post(base_url, json=data, headers=headers)
		return await r.json()

async def get_series(sid):
	data = {'id': sid, 'mode': 'get-series-id'}
	async with ClientSession() as session:
		r = await session.post(base_url, json=data, headers=headers)
		return await r.json()
