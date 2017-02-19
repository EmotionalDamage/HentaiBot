from bs4 import BeautifulSoup as BS
from bs4.element import Tag as BSTag
from requests import get, post
from yaml import load, dump

token = "MTkzNjQzMjQyODcxNDU1NzQ0.CkaX6g.4cMhAG02Ra0aq3sIy6eActKwnEA"
base_url = "https://discordapp.com/api"

def get_list():
    sauce = get(
        "https://www.hentaihaven.org",
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        })
    if sauce.status_code != 200:
        print("Error: {}\n\n{}".format(sauce.status_code, sauce.content))
        return "", []
    soup = BS(sauce.content, "lxml")
    del sauce
    names = []
    links = []
    tags = []
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
    end_name = ""
    with open("config.yaml") as file:
        data = load(file)
        end_name = data["last_name"]
        channels = data["channels"]
    message = ""
    first_name = ""
    counter = 0
    limit_counter = 0 # Limit is 3 per post
    for i in range(len(names)):
        if limit_counter == 3:
            break
        name = names[i]
        if name == end_name:
            break
        link = links[i]
        tag = ', '.join(tags[i])
        message += "{}:\nTags: {}\n{}\n".format(name, tag, link)
        if first_name == "":
            first_name = name
        limit_counter += 1
    if first_name != "" and first_name != end_name:
        with open("config.yaml", "w") as file:
            file.write(dump({
                "last_name" : first_name,
                "channels" : channels,
            }))
    return message, channels

msg, chs = get_list()
if msg != "":
    output = "New Hentai Release:\n{}".format(msg)
    for ch in chs:
        x = post(
            url = "{}/channels/{}/messages".format(base_url, ch),
            data = {"content": msg},
            headers = {"Authorization": "Bot {}".format(token)}
        )
    print(msg)
else:
    print("None")
