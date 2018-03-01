# Hentai_IRL v1
from json import load
from requests import get

def go(num=3):
    response = get(f"https://www.reddit.com/r/hentai_irl/hot/.json?limit={num}",
                   headers = {'User-agent':'HentaiBot 2'}).json()
    items = response['data']["children"]
    links = []
    for i in items:
        x = i["data"]
        if not x['is_self']:
            links.append(x["url"])
    return ('\n'.join(links))
