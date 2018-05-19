# Hanime.tv API ~ Uses web scraping so don't use it too much.
from requests import get
from json import loads
from math import floor

URL = "https://staging.hanime.tv"
RECENT_UPLOADS = 0
NEW_RELEASES = 1
TRENDING = 2
RANDOM = 3


def go(section=RECENT_UPLOADS, limit=5, end_name=0, colour=0):
    response = get(URL)
    if response.status_code != 200:
        return None
    _, response = response.text.split("__NUXT__=")
    response, _ = response.split(";")
    response = loads(response)
    if 0 > section > 4:
        section = RECENT_UPLOADS
    root = response["state"]["data"]["landing"]
    hentai_list = root["sections"][section]["hentai_video_ids"]
    video_list = map_list(root["hentai_videos"])
    first_video = end_name
    output = []
    for i in range(len(hentai_list)):
        if i <= (limit-1):
            id_ = hentai_list[i]
            video = video_list[id_]
            if id_ == end_name:
                break
            elif i == 0:
                first_video = id_
            output.append({
                "id": id_,
                "name": video["name"],
                "url": f"{URL}/hentai-videos/{video['slug']}",
                "image": video["cover_url"],
                "poster": video["poster_url"],
                "subbed": video["is_hard_subtitled"],
                "censored": video["is_censored"],
                "duration": video["duration_in_ms"],
            })
        else:
            break
    if first_video != end_name:
        end_video_changed = True
    else:
        end_video_changed = False
    return embed_format(output, colour), (end_video_changed, first_video)


def embed_format(videos, embed_colour):
    COL = 12
    output = []
    for v in videos:
        try:
            if v["duration"] == 0: raise AttributeError
            minutes = floor(v["duration"] / 60_000)
            seconds = floor((v["duration"] % 60_000) / 1_000)
        except:
            minutes = "??"
            seconds = "??"
        try:
            desc = "Duration:".ljust(COL) + f"{minutes}:{seconds:02d}\n"
            desc += "Subbed:".ljust(COL) + ("Yes" if v["subbed"] else "No")+ "\n"
            desc += "Censored:".ljust(COL) + ("Yes" if v["censored"] else "No")
        except:
            desc = ""
        output.append({
            "title": v["name"],
            "description": desc,
            "url": v["url"],
            "color": embed_colour,
            "thumbnail": {
                "url": v["image"]
            },
            "image": {
                "url": v["poster"]
            },
        })
    return output


def map_list(video_list):
    mapped = {}
    for i in video_list:
        mapped[i["id"]] = i
    return mapped


if __name__ == "__main__":
    result = go()
    if result is not None:
        for i in result:
            print("====================")
            print(i["name"])
            print(i["id"])
            print(i["url"])
            print(i["image"])
            print(i["subbed"])
            print(i["censored"])
            print(i["duration"])
            print("====================")
    else:
        print(result.content)
