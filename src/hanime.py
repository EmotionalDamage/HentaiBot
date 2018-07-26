from requests import get
from json import loads
from math import floor
from enum import Enum
from .discord import Discord
from data import HAnimeConfig, LastEntry

HANIME_URL = "https://hanime.tv"
COL = 12


def go(discord: Discord, config: HAnimeConfig, last_entry: LastEntry):
    response = get(HANIME_URL)
    if not response.ok:
        return None
    _, response = response.text.split("__NUXT__=")
    response, _ = response.split(";")
    response = loads(response)
    root = response["state"]["data"]["landing"]
    hentai_list = root["sections"][int(config.section)]["hentai_video_ids"]
    video_list = {i['id']: i for i in root["hentai_videos"]}
    output = []
    for i in range(len(hentai_list)):
        if i < config.posts:
            id_ = hentai_list[i]
            video = video_list[id_]
            if id_ == last_entry.ha:
                break
            elif i == 0:
                last_entry.ha = id_
            output.append({
                "id": id_,
                "name": video["name"],
                "url": f"{HANIME_URL}/hentai-videos/{video['slug']}",
                "image": video["cover_url"],
                "poster": video["poster_url"],
                "subbed": video["is_hard_subtitled"],
                "censored": video["is_censored"],
                "duration": video["duration_in_ms"],
            })
        else:
            break
    embs = embed_format(output, config.embed_colour)
    if len(embs) == 0:
        print("Info     No New HAnime.tv Entries")
    for e in embs:
        for ch in config.channels:
            with discord:
                sent_msg = discord.send_msg(
                    channel=ch,
                    content=config.message,
                    embed=e
                )
                output = f"To Channel: {ch},    Sent \'{e['title']}\'"
                if sent_msg.ok:
                    print(f"Success!", output)
                else:
                    print(f"Error!  ", output)
                    print(sent_msg.text)


def embed_format(videos, embed_colour):
    output = []
    for v in videos:
        try:
            if v["duration"] == 0:
                raise AttributeError
            minutes = floor(v["duration"] / 60_000)
            seconds = floor((v["duration"] % 60_000) / 1_000)
            desc = "Duration:".ljust(COL) + f"{minutes}:{seconds:02d}\n"
        except AttributeError or KeyError:
            desc = "Duration:".ljust(COL) + "??:??\n"
        try:
            desc += "Subbed:".ljust(COL) + ("Yes" if v["subbed"] else "No") + "\n"
            desc += "Censored:".ljust(COL) + ("Yes" if v["censored"] else "No")
        except KeyError:
            desc += ""
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


class Section(Enum):
    RECENT_UPLOADS = 0
    NEW_RELEASES = 1
    TRENDING = 2
    RANDOM = 3

    def __int__(self) -> int:
        return self.value
