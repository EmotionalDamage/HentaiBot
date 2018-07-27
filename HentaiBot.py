# HentaiBot v2
from data import Config, LastEntry
from src import Discord, HentaiHaven, HAnime, Reddit


def start():
    config: Config = Config("./data/config.yaml")
    last_entry: LastEntry = LastEntry("./data/last_entry.yaml")
    discord: Discord = Discord(token=config.token)
    hentai_haven = HentaiHaven(
        discord,
        config.hentai_haven,
        last_entry
    )
    hanime = HAnime(
        discord,
        config.hanime,
        last_entry
    )

    reddit = [Reddit(discord, c) for c in config.reddit]
    hentai_haven.start()
    hanime.start()
    for r in reddit:
        r.start()

    hentai_haven.join()
    hanime.join()
    last_entry.write()
    for r in reddit:
        r.join()


if __name__ == "__main__":
    start()
