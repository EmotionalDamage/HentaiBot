from bs4 import BeautifulSoup as BS
from bs4.element import Tag as BSTag
from requests import get, post
from yaml import load, dump
from json import dumps as jdump
from sys import exit as sysexit

with open("config.yaml") as file:
    data = load(file)
    token = data["token"]
    if token == "":
        print("No token written in the config.yaml file")
        sysexit()
    if len(data["channels"]) == 0:
        print("No channels written in the config.yaml file")
        sysexit()
base_url = "https://discordapp.com/api"

def get_list():
##    sauce = get(
##        "https://www.hentaihaven.org",
##        headers = {
##            "user-agent": "HentaiBot (https://github.com/NightShadeNeko/HentaiBot)"
##        })
##    if sauce.status_code != 200:
##        print("Error: {}\n\n{}".format(sauce.status_code, sauce.content))
##        return "", []
##    soup = BS(sauce.content, "lxml")
##    del sauce
    with open("source.txt", "r") as f:
        text = f.read()
        soup = BS(text,"lxml")
    names = []
    links = []
    tags = []
    imgs = []
    titles = soup.find_all("a", class_="brick-title")
    tag_groups = soup.find_all("span", class_="tags")
    for title in titles:
        names.append(title.text)
        links.append(title["href"])
    for tag in tag_groups:
        tag_group = []
        for single_tag in tag.children:
            if type(single_tag) == BSTag:
                tag_str = single_tag.string
                if tag_str != None:
                    tag_group.append(tag_str)
                    tags.append(tag_group)
    for img in soup.find_all("img", class_="lazy attachment-medium post-image"):
        imgs.append(img["data-src"])
    end_name = ""
    with open("config.yaml") as file:
        data = load(file)
        end_name = data["last_name"]
        channels = data["channels"]
    message = ""
    first_name = ""
    counter = 0
    limit_counter = 0 # Limit is 3 per post
    embs = []
    for i in range(len(names)):
        if limit_counter == 3:
            break
        name = names[i]
        if name == end_name:
            break
        link = links[i]
        tag = ', '.join(tags[i])
        img = imgs[i]
        emb_obj = embed_object(name, link, tag, img)
        embs.append(emb_obj.output())
        if first_name == "":
            first_name = name
        limit_counter += 1
    if first_name != "" and first_name != end_name:
        with open("config.yaml", "w") as file:
            file.write(dump({
                "last_name" : first_name,
                "channels" : channels,
            }))
    return embs, channels

class embed_object:
    def __init__(self, title, link, tag, img):
        self.title = title
        self.link = link
        self.tag = tag
        self.img = img
    def output(self):
        embed = {
            "title": self.title,
            "description": self.tag,
            "url": self.link,
            "color": 16711680,
            "image": {
                "url": self.img,
            }
        }
        return embed

embs, chs = get_list()
if len(embs) != 0:
    for ch in chs:
        for emb in embs:
            x = post(
                url = "{}/channels/{}/messages".format(base_url, ch),
                data = jdump({"content": "New Hentai Release!", "embed": emb}),
                headers = {"Authorization": "Bot {}".format(token), "Content-Type":"application/json"}
            )
        print(x.content)
else:
    print("None")
