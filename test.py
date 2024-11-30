import cloudscraper
import pprint

headers = {
    "Accept": "application/json",
    "Referer": "https://comick.cc",
    "User-Agent": "Tachiyomi Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
}
base_url = "https://api.comick"
domains = [".fun", ".io"]

scraper = cloudscraper.create_scraper()

res = scraper.get("https://api.comick.io/v1.0/search/?limit=20&tachiyomi=true&sort=user_follow_count&showall=true&t=false&page=1", headers=headers)
pprint.pprint(res.status_code)