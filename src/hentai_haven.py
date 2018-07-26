from typing import Optional, List
from feedparser import parse
import xml.etree.ElementTree as ET
from requests import Response
from data import HentaiHavenConfig, LastEntry
from .discord import Discord


def go(discord: Discord, config: HentaiHavenConfig, last_entry: LastEntry):
    # Get items from the RSS feed
    items = parse("http://hentaihaven.org/feed").entries
    new_items = []
    counter: int = 0
    first_name_hh: Optional[str] = None
    for item in items:
        if (item['id'] == last_entry.hh) or (counter == config.posts):
            break
        elif tag_filter(config.black_list, item.summary):
            new_items.append(item)
            counter += 1
            if first_name_hh is None:
                first_name_hh = item['id']
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

    for e in embs:
        for ch in config.channels:
            with discord:
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


def get_from_summary(summary: str) -> (str, str):
    root = ET.fromstring(f"<element>{summary}</element>")
    d = f"{root[1].text}\n\n{root[2].text}"
    i = root[0][0].attrib["src"]
    return d, i
