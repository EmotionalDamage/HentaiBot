from yaml import load
from typing import List
from sys import exit as sys_exit
from src import Section

DEFAULT_HH_COLOUR: int = 16711680


class Config:
    def __init__(self, path: str) -> None:
        with open(path, mode="r") as file:
            data = load(file)
        self.token: str = str(data.get("token", ""))
        if self.token == "":
            print('"token" is a required field')
            sys_exit()
        self.channels: List[str] = [str(i) for i in data.get("channels", [])]
        if len(self.channels) == 0:
            print('"channels" must have at least one item')
            sys_exit()
        self.posts: int = int(data.get("posts", 3))
        self.message: str = str(data.get("message", "New Hentai Release"))
        self.hentai_haven: HentaiHavenConfig = HentaiHavenConfig(self, data.get("hentai_haven", {}))
        self.reddit: List[RedditConfig] = [RedditConfig(self, name, item) for (name, item) in data.get("reddit", {}).items()]


class HentaiHavenConfig:
    def __init__(self, parent: Config, data) -> None:
        self.enabled: bool = data.get("enabled", False)
        self.posts: int = data.get("posts", parent.posts)
        if self.posts == 0:
            self.posts = parent.posts
        self.channels: List[str] = [str(i) for i in data.get("channels", parent.channels)]
        if len(self.channels) == 0:
            self.channels = parent.channels
        self.embed_colour: int = parse_colour(data.get("embed_colour", DEFAULT_HH_COLOUR), DEFAULT_HH_COLOUR)  # Default: Red
        self.black_list: List[str] = data.get("blacklist", [])
        self.message: str = parent.message


class HAnimeConfig:
    def __init__(self, parent: Config, data) -> None:
        self.enabled: bool = data.get("enabled", False)
        self.posts: int = data.get("posts", parent.posts)
        self.message: str = parent.message
        if self.posts == 0:
            self.posts = parent.posts
        self.channels: List[str] = [str(i) for i in data.get("channels", parent.channels)]
        if len(self.channels) == 0:
            self.channels = parent.channels
        self.embed_colour: int = parse_colour(data.get("embed_colour", DEFAULT_HH_COLOUR), DEFAULT_HH_COLOUR)  # Default: Red
        self.section: Section = section_from_str(data.get("section"), Section.RECENT_UPLOADS)


class RedditConfig:
    def __init__(self, parent: Config, name: str, data):
        self.name: str = name
        self.posts: int = data.get("posts", parent.posts)
        self.channels: List[str] = [str(i) for i in data.get("channels", parent.channels)]
        if len(self.channels) == 0:
            self.channels = parent.channels


def parse_colour(data, default: int) -> int:
    col: int = default
    try:
        col = int(data)
    except ValueError:
        try:
            col = int(data, 16)
        except ValueError:
            pass
    if col < 0:
        col = default
    return col


def section_from_str(text: str, default: Section) -> Section:
    text = text.lower()
    section: Section = default
    if text == "recent_uploads":
        section = Section.RECENT_UPLOADS
    elif text == "new releases":
        section = Section.NEW_RELEASES
    elif text == "trending":
        section = Section.TRENDING
    elif text == "random":
        section = Section.RANDOM
    return section
