from requests import get
from threading import Thread
from typing import List, Dict
from data.config import RedditConfig
from .discord import Discord


class Reddit(Thread):
    def __init__(self, discord: Discord, config: RedditConfig) -> None:
        self.discord = discord
        self.config = config
        Thread.__init__(self)

    def run(self):
        go(
            discord=self.discord,
            config=self.config
        )


def go(discord: Discord, config: RedditConfig) -> None:
    response = get(f"https://www.reddit.com/r/{config.name}/hot/.json?limit={config.posts}",
                   headers={'User-agent': 'HentaiBot'})
    if not response.ok:
        print(f"Error in getting subreddit posts\n{' '*4}{response.content}")
        return None
    items: List[Dict] = response.json()['data']['children']
    links: List[str] = []
    for item in items:
        item = item['data']
        if not item['is_self']:
            links.append(item['url'])
    message: str = '\n'.join(links)
    for ch in config.channels:
        sent_msg = discord.send_msg(
            channel=ch,
            content=message,
        )
        output = f"To Channel: {ch},    Sent {config.posts} r/{config.name} Posts"
        if sent_msg.ok:
            print(f"Success!", output)
        else:
            print(f"Error!  ", output)
