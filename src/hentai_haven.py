from typing import Optional, List, Tuple
from threading import Thread
from feedparser import parse
import xml.etree.ElementTree as ET
from requests import Response
from data import HentaiHavenConfig, LastEntry
from .discord import Discord


class HentaiHaven(Thread):
    def __init__(self, discord: Discord, config: HentaiHavenConfig, last_entry: LastEntry) -> None:
        self.discord = discord
        self.config = config
        self.last_entry = last_entry
        Thread.__init__(self, name="HentaiHaven")

    def run(self):
        go(
            discord=self.discord,
            config=self.config,
            last_entry=self.last_entry
        )


def go(discord: Discord, config: HentaiHavenConfig, last_entry: LastEntry):
    # Get items from the RSS feed
    items = parse("http://hentaihaven.org/feed").entries
    new_items = []
    counter: int = 0
    first_name_hh: Optional[int] = None
    for item in items:
        id_: int = int(item['id'].replace("http://hentaihaven.org/?p=", ""))
        if (id_ == last_entry.hh) or (counter == config.posts):
            break
        elif tag_filter(config.black_list, item.summary):
            new_items.append(item)
            counter += 1
            if first_name_hh is None:
                first_name_hh = id_
    if first_name_hh is not None:
        last_entry.hh = first_name_hh

    # Turn RSS items into embed objects
    embs: List = []
    for item in new_items:
        desc, image = get_from_summary(item.summary)
        emb_obj = {
            "title": item.title,
            "description": desc,
            "url": item.link,
            "color": config.embed_colour,
            "image": {
                "url": image
            }
        }
        embs.append(emb_obj)

    if len(embs) == 0:
        print("Info     No New HentaiHaven Entries")

    for e in embs:
        for ch in config.channels:
            response: Response = discord.send_msg(
                channel=ch,
                content=config.message,
                embed=e
            )
            output: str = f"To Channel: {ch},    Sent \'{e['title']}\'"
            if response.ok:
                print("Success!", output)
            else:
                print("Error!", output)
                print(response.text)


def tag_filter(tags: List[str], summary: str) -> bool:
    summary = summary.lower()
    for t in tags:
        tag = t.lower()
        if tag in summary:
            return False
    return True


def get_from_summary(summary: str) -> Tuple[str, str]:
    root = ET.fromstring(f"<element>{summary}</element>")
    d = f"{root[1].text}\n\n{root[2].text}"
    i = root[0][0].attrib["src"]
    return d, i
