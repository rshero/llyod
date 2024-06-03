from aiohttp import ClientSession

headers = {
    "Accept": "application/json",
    "Referer": "https://comick.cc",
    "User-Agent": "Tachiyomi Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
}
base_url = "https://api.comick"
domains = [".fun", ".io"]


async def comic_search(query):
    for domain in domains:
        async with ClientSession() as session:
            r = await session.get(
                f"{base_url}{domain}/v1.0/search/?type=comic&page=1&limit=8&q={query}&t=false",
                headers=headers,
            )
            if r.status == 200:
                data = await r.json()
                if len(data) > 10:
                    data = data[:8]
                return data


async def get_comic(slug):
    for domain in domains:
        async with ClientSession() as session:
            r = await session.get(
                f"{base_url}{domain}/comic/{slug}/?t=0", headers=headers
            )
            if r.status == 200:
                data = await r.json()
                return data


async def get_latest_comics(qtype, page=1):
    for domain in domains:
        apiurl = f"{base_url}{domain}/v1.0/search/?limit=20&tachiyomi=true&sort=uploaded&showall=true&t=false&page={page}"
        if qtype:
            apiurl += qtype

        async with ClientSession() as session:
            r = await session.get(apiurl, headers=headers)
            if r.status == 200:
                data = await r.json()
                return data
