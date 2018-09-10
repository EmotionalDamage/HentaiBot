from requests import get
from json import loads
from math import floor
from threading import Thread
from .discord import Discord
from data import HAnimeConfig, LastEntry, Section

HANIME_URL = "https://hanime.tv"
COL = 12


class HAnime(Thread):
    def __init__(self, discord: Discord, config: HAnimeConfig, last_entry: LastEntry) -> None:
        self.discord = discord
        self.config = config
        self.last_entry = last_entry
        Thread.__init__(self)

    def run(self):
        go(
            discord=self.discord,
            config=self.config,
            last_entry=self.last_entry
        )


def go(discord: Discord, config: HAnimeConfig, last_entry: LastEntry):
    response = get(HANIME_URL)
    if not response.ok:
        return None
    _, src = response.text.split("__NUXT__=")
    src, _ = src.split(";</script>")
    data = loads(src)
    root = data["state"]["data"]["landing"]
    hentai_list = root["sections"][int(config.section)]["hentai_video_ids"]
    video_list = {i['id']: i for i in root["hentai_videos"]}
    output = []
    for i in range(len(hentai_list)):
        if i < config.posts:
            id_ = hentai_list[i]
            video = video_list[id_]
            if id_ == last_entry.ha_before:
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
        print("Info     No New HAnime Entries")
    for e in embs:
        for ch in config.channels:
            sent_msg = discord.send_msg(
                channel=ch,
                content=config.message,
                embed=e
            )
            msg: str = f"To Channel: {ch},    Sent \'{e['title']}\'"
            if sent_msg.ok:
                print(f"Success!", msg)
            else:
                print(f"Error!  ", msg)
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
