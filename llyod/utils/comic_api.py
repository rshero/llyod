import asyncio
import cloudscraper
import logging

headers = {
    "Accept": "application/json",
    "Referer": "https://comick.cc",
    "User-Agent": "Tachiyomi Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
}
base_url = "https://api.comick"
domains = [".fun", ".io"]

# Create a cloudscraper session
scraper = cloudscraper.create_scraper()

async def comic_search(query):
    for domain in domains:
        try:
            # Use asyncio.to_thread to make the synchronous cloudscraper request asynchronous
            url = f"{base_url}{domain}/v1.0/search/?type=comic&page=1&limit=8&q={query}&t=false"
            response = await asyncio.to_thread(scraper.get, url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if len(data) > 10:
                    data = data[:8]
                return data
        except Exception as e:
            logging.error(f"Error fetching comick search results: {e}")

async def get_comic(slug):
    for domain in domains:
        try:
            url = f"{base_url}{domain}/comic/{slug}/?t=0"
            response = await asyncio.to_thread(scraper.get, url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data
        except Exception as e:
            logging.error(f"Error fetching comic: {e}")

async def get_latest_comics(qtype, page=1):
    for domain in domains:
        apiurl = f"{base_url}{domain}/v1.0/search/?limit=20&tachiyomi=true&sort=uploaded&showall=true&t=false&page={page}"
        if qtype:
            apiurl += qtype
        try:
            response = await asyncio.to_thread(scraper.get, apiurl, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data
        except Exception as e:
            logging.error(f"Error fetching latest comics: {e}")
