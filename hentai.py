# Hentai v1
from json import load
from requests import get

def go(num=3):
    response = get(f"https://www.reddit.com/r/hentai/hot/.json?limit={num}",
                   headers = {'User-agent':'MoreHentaiBot'}).json()
    items = response['data']["children"]
    links = []
    for i in items:
        x = i["data"]
        if not x['is_self']:
            links.append(x["url"])
    return ('\n'.join(links))
