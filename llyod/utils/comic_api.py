from aiohttp import ClientSession

headers = {
    "Accept": "application/json",
    "Referer": "https://comick.cc",
    "User-Agent": "Tachiyomi Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
}
base_url = "https://api.comick"
domains = [".fun", ".io"]

async def comic_search(query):
    async with ClientSession() as session:
        for domain in domains:
            try:
                async with session.get(
                    f"{base_url}{domain}/v1.0/search/?type=comic&page=1&limit=8&q={query}&t=false",
                    headers=headers,
                ) as r:
                    if r.status == 200:
                        data = await r.json()
                        if len(data) > 10:
                            data = data[:8]
                        print(data)
                        return data
            except Exception as e:
                print(f"Error fetching comick search results: {e}")

async def get_comic(slug):
    async with ClientSession() as session:
        for domain in domains:
            try:
                async with session.get(
                    f"{base_url}{domain}/comic/{slug}/?t=0", headers=headers
                ) as r:
                    if r.status == 200:
                        data = await r.json()
                        return data
            except Exception as e:
                print(f"Error fetching comic: {e}")

async def get_latest_comics(qtype, page=1):
    async with ClientSession() as session:
        for domain in domains:
            apiurl = f"{base_url}{domain}/v1.0/search/?limit=20&tachiyomi=true&sort=uploaded&showall=true&t=false&page={page}"
            if qtype:
                apiurl += qtype
            try:
                async with session.get(apiurl, headers=headers) as r:
                    if r.status == 200:
                        data = await r.json()
                        return data
            except Exception as e:
                print(f"Error fetching latest comics: {e}")
