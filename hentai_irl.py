# Hentai_IRL v1
from json import load
from requests import get

channels = ["378437336712609792"]

def go():
    response = get("https://www.reddit.com/r/hentai_irl/hot/.json?limit=3",
                   headers = {'User-agent':'HentaiBot 2'}).json()
    items = response['data']["children"]
    links = []
    for i in items:
        x = i["data"]
        if not x['is_self']:
            links.append(x["url"])
    return (channels, '\n'.join(links))
