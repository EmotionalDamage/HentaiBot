# HentaiBot v2
import feedparser
from yaml import load, dump
from json import dumps as jdump
from requests import post
from sys import exit as sysexit
import xml.etree.ElementTree as ET
BASE_URL = "https://discordapp.com/api"

# ---------
def get_from_summary(summary):
    root = ET.fromstring(f"<element>{summary}</element>")
    d = f"{root[1].text}\n\n{root[2].text}"
    i = root[0].attrib["src"]
    return (d, i)
# ---------

def start():
    #Get data from config file
    with open("config.yaml") as file:
        data = load(file)
        token = str(data["token"])
        channels = data["channels"]
        num = int(data["posts"])
        hentai_haven = data["hentai_haven"]["enabled"]
    if hentai_haven:
        hentai_haven_num = int(data["hentai_haven"]["posts"])
        hentai_haven_channels = data["hentai_haven"]["channels"]
        hentai_haven_black_list = data["hentai_haven"].get("blacklist", [])
        try:
            hentai_haven_colour = int(data["hentai_haven"]["embed_colour"])
        except ValueError:
            hentai_haven_colour = int(data["hentai_haven"]["embed_colour"], 16)
        if hentai_haven_colour < 0:
            hentai_haven_colour = 16711680
        if len(hentai_haven_channels) == 0:
            hentai_haven_channels = channels
    if token == "":
        print("Error! No token written in the config.yaml file")
        sysexit()
    with open("last_name", encoding='utf-8') as file:
        end_name = file.read()


    #HentaiHaven
    if hentai_haven:
        #Get items from the RSS feed
        x = feedparser.parse("http://hentaihaven.org/feed").entries
        new_items = [] #All the new items will be appended into this list
        counter = 0 #Max limit of 5 items per post
        for i in range(len(x)):
            if (x[i]['id'] == end_name) or (counter == hentai_haven_num):
                break
            else:
                new_items.append(x[i])
                counter += 1
                if i == 0:
                    first_name = x[0]['id']

        #The RSS Items will be turned into embedded objects
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

        #Send the messages out to the discord channels
        if len(new_embs) > 0:
            for ch in channels:
                for emb in new_embs:
                    sent_msg = post(
                        url = f"{BASE_URL}/channels/{ch}/messages",
                        data = jdump({"content":"New Hentai Release!", "embed":emb}),
                        headers = {"Authorization": f"Bot {token}", "Content-Type":"application/json"}
                    )
                    output = f"To Channel: {ch},    Sent \'{emb['title']}\'"
                    if sent_msg.ok:
                        print("Success!", output)
                    else:
                        print("Error!", output)

            #Update config with the newest item
            if first_name != end_name:
                with open("last_name", "w", encoding='utf-8') as file:
                        file.write(first_name)
        else:
            print("Info     No New HentaiHaven Entries")

    #Reddit Plugins
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
                url = f"{BASE_URL}/channels/{ch}/messages",
                data = jdump({"content":links}),
                headers = {"Authorization": f"Bot {token}", "Content-Type":"application/json"}
            )
            output = f"To Channel: {ch},    Sent {r_num} r/{i} Posts"
            if sent_msg.ok:
                print(f"Success!", output)
            else:
                print(f"Error!  ", output)

if __name__ == "__main__":
    start()
