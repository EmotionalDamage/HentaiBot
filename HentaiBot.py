# HentaiBot v2
import feedparser
from yaml import load, dump
from json import dumps as jdump
from requests import post
import xml.etree.ElementTree as ET
BASE_URL = "https://discordapp.com/api"

def get_from_summary(summary):
    root = ET.fromstring(f"<element>{summary}</element>")
    d = f"{root[1].text}\n\n{root[2].text}"
    i = root[0].attrib["src"]
    return (d, i)

#Get data from config file
with open("config.yaml") as file:
    data = load(file)
    token = data["token"]
    end_name = data["last_name"]
    channels = data["channels"]
    if token == "":
        print("No token written in the config.yaml file")
        sysexit()
    if len(channels) == 0:
        print("No channels written in the config.yaml file")
        sysexit()

#Get items from the RSS feed
x = feedparser.parse("http://hentaihaven.org/feed").entries
new_items = [] #All the new items will be appended into this list
counter = 0 #Max limit of 5 items per post
for i in range(len(x)):
    if (x[i].title == end_name) or (counter == 5):
        break
    else:
        new_items.append(x[i])
        counter += 1

#The RSS Items will be turned into embedded objects
new_embs = []
for i in range(len(new_items)):
    y = new_items[i]
    desc, image = get_from_summary(y.summary)
    emb_obj = {
        "title": y.title,
        "description": desc,
        "url": y.link,
        "color": 16711680,
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
        print(sent_msg.content)
        
    #Update config with the newest item
    first_name = new_embs[0]["title"]
    if first_name != end_name:
        with open("config.yaml", "w") as file:
                file.write(dump({
                    "last_name" : first_name,
                    "channels" : channels,
                    "token" : token
                }))
else:
    print("None")
