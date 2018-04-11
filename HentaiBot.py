# HentaiBot v2
import feedparser
from yaml import load, dump
from json import dumps as jdump
from requests import post
from sys import exit as sysexit
import xml.etree.ElementTree as ET
BASE_URL = "https://discordapp.com/api"


#  ---------
def get_from_summary(summary):
    root = ET.fromstring(f"<element>{summary}</element>")
    d = f"{root[1].text}\n\n{root[2].text}"
    i = root[0].attrib["src"]
    return d, i


def tag_filter(tags, summary):
    summary = summary.lower()
    for t in tags:
        tag = t.lower()
        if tag in summary:
            return False
    return True
#  ---------


def start():
    # Get data from config file
    with open("config.yaml") as file:
        data = load(file)
        token = str(data["token"])
        channels = data["channels"]
        num = int(data["posts"])
        hentai_haven = data["hentai_haven"]["enabled"]
        hanime_tv = data["hanime_tv"]["enabled"]
    if hentai_haven:
        hentai_haven_num = int(data["hentai_haven"]["posts"])
        hentai_haven_channels = data["hentai_haven"]["channels"]
        hentai_haven_black_list = data["hentai_haven"].get("blacklist", [])
        if hentai_haven_num < 1 or hentai_haven_num is None:
            hentai_haven_num = num
        try:
            hentai_haven_colour = int(data["hentai_haven"]["embed_colour"])
        except ValueError:
            hentai_haven_colour = int(data["hentai_haven"]["embed_colour"], 16)
        if hentai_haven_colour < 0:
            hentai_haven_colour = 16711680
        if len(hentai_haven_channels) == 0:
            hentai_haven_channels = channels
    if hanime_tv:
        hanime_tv_num = int(data["hanime_tv"]["posts"])
        hanime_tv_channels = data["hanime_tv"]["channels"]
        hanime_tv_section = data["hanime_tv"]["section"].lower()
        if hanime_tv_num < 1 or hanime_tv is None:
            hanime_tv_num = num
        try:
            hanime_tv_colour = int(data["hanime_tv"]["embed_colour"])
        except ValueError:
            hanime_tv_colour = int(data["hanime_tv"]["embed_colour"], 16)
        if hanime_tv_colour < 0:
            hanime_tv_channels = int("FF00FF", 16)
        if len(hanime_tv_channels) == 0:
            hanime_tv_channels = channels
        if hanime_tv_section == "new releases":
            from hanime_tv import NEW_RELEASES
            hanime_tv_section = NEW_RELEASES
        elif hanime_tv_section == "trending":
            from hanime_tv import TRENDING
            hanime_tv_section = TRENDING
        elif hanime_tv_section == "random":
            from hanime_tv import RANDOM
            hanime_tv_section = RANDOM
        else:
            from hanime_tv import RECENT_UPLOADS
            hanime_tv_section = RECENT_UPLOADS
    if token == "":
        print("Error! No token written in the config.yaml file")
        sysexit()
    if hentai_haven or hanime_tv:
        with open("last_name.yaml", encoding='utf-8') as file:
            end_names = load(file.read())
            end_name_hh = end_names["hh"]
            end_name_ha = end_names["ha"]
            first_name_hh, first_name_ha = end_name_hh, end_name_ha
    change_name_hh, change_name_ha = False, False


    # HentaiHaven
    if hentai_haven:
        # Get items from the RSS feed
        x = feedparser.parse("http://hentaihaven.org/feed").entries
        new_items = []  # All the new items will be appended into this list
        counter = 0  # Max limit of 5 items per post
        first_name_hh = ""
        for i in range(len(x)):
            if (x[i]['id'] == end_name_hh) or (counter == hentai_haven_num):
                break
            else:
                if tag_filter(hentai_haven_black_list, x[i].summary):
                    new_items.append(x[i])
                    counter += 1
                    if first_name_hh == "":
                        first_name_hh = x[0]['id']
        if first_name_hh == "":
            first_name_hh = end_name_hh

        # The RSS Items will be turned into embedded objects
        new_embs = []
        for i in range(len(new_items)):
            y = new_items[i]
            desc, image = get_from_summary(y.summary)
            emb_obj = {
                "title": y.title,
                "description": desc,
                "url": y.link,
                "color": hentai_haven_colour,
                "image": {
                    "url": image
                }
            }
            new_embs.append(emb_obj)

        # Send the messages out to the discord channels
        if len(new_embs) > 0:
            for ch in channels:
                for emb in new_embs:
                    sent_msg = post(
                        url=f"{BASE_URL}/channels/{ch}/messages",
                        data=jdump({"content": "New Hentai Release!", "embed": emb}),
                        headers={"Authorization": f"Bot {token}", "Content-Type": "application/json"}
                    )
                    output = f"To Channel: {ch},    Sent \'{emb['title']}\'"
                    if sent_msg.ok:
                        print("Success!", output)
                    else:
                        print("Error!", output)
                        print(sent_msg.text)

            # Update config with the newest item
            if first_name_hh != end_name_hh:
                change_name_hh = True
        else:
            print("Info     No New HentaiHaven Entries")

    # HAnime.tv
    if hanime_tv:
        import hanime_tv
        embeds, first_id = hanime_tv.go(
            section=hanime_tv_section,
            colour=hanime_tv_colour,
            limit=hanime_tv_num,
            end_name=end_name_ha
        )
        change_name_ha = first_id[0]
        if change_name_ha:
            first_name_ha = first_id[1]
        else:
            first_name_ha = end_name_ha
        emb_num = len(embeds)
        if emb_num == 0:
            print("Info     No New HAnime.tv Entries")
        for e in embeds:
            for ch in hanime_tv_channels:
                sent_msg = post(
                    url=f"{BASE_URL}/channels/{ch}/messages",
                    data=jdump({"content": "New Hentai Release", "embed": e}),
                    headers={"Authorization": f"Bot {token}", "Content-Type": "application/json"}
                )
                output = f"To Channel: {ch},    Sent \'{e['title']}\'"
                if sent_msg.ok:
                    print(f"Success!", output)
                else:
                    print(f"Error!  ", output)
                    print(sent_msg.text)

    # Reddit Plugins
    for i in data["reddit"].keys():
        import reddit_api
        subred = data["reddit"][i]
        r_num = subred["posts"]
        if r_num is None or r_num < 1:
            r_num = num
        r_chs = subred["channels"]
        if r_chs is None or len(r_chs) == 0:
            r_chs = channels
        links = reddit_api.go(i, r_num)
        for ch in r_chs:
            sent_msg = post(
                url=f"{BASE_URL}/channels/{ch}/messages",
                data=jdump({"content": links}),
                headers={"Authorization": f"Bot {token}", "Content-Type": "application/json"}
            )
            output = f"To Channel: {ch},    Sent {r_num} r/{i} Posts"
            if sent_msg.ok:
                print(f"Success!", output)
            else:
                print(f"Error!  ", output)

    if change_name_hh or change_name_ha:
        with open("last_name.yaml", "w", encoding='utf-8') as file:
            file.write(dump({
                "hh": first_name_hh,
                "ha": first_name_ha
            }))
        if change_name_hh:
            print(f"Info     HentaiHaven id changed to: {first_name_hh}")
        if change_name_ha:
            print(f"Info     Hanime.tv id changed to: {first_name_ha}")


if __name__ == "__main__":
    start()
