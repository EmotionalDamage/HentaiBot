# HentaiBot
Well... a bot that checks HentaiHaven.org for new hentai and if it finds a new one, sends the info as a message to a Discord channel(s)

\[WARNING: All Links Are NSFW]

It uses the RSS feed at www.hentaihaven.org/feed to check for new releases, if it finds a new one then it will send a discord message to the channels specified in the config.yaml file.

It can also go on www.reddit.com/r/{subreddit_name} and post the top posts. (By default, it posts the top 3 but this can be changed in the config.yaml file). (e.g. you can post the top posts from [r/hentai_irl](https://www.reddit.com/r/hentai_irl))
This feature can be added/edited in the config.yaml file.

## Dependencies:
- [feedparser](https://github.com/kurtmckee/feedparser)  (For reading the RSS feed)
- [pyYAML](https://github.com/yaml/pyyaml)  (For reading and writing to the config file)
- [requests](http://python-requests.org)  (For writing a POST request to Discord)
- json <b>\[Standard Library]</b>  (For writing the information sent to Discord)
- xml <b>\[Standard Library]</b>  (For reading some of the XML text)

## Setup:
### 1. Make sure that the dependencies not in the standard library are installed using <b>pip</b> or some other method<br>
e.g.
  to install "feedparser" write ```pip install feedparser``` in the command line,<br>
  to install "yaml" write ```pip install pyYAML```,<br>
  and to install "requests" write ```pip install requests```.<p>
### 2. Configure the config.yaml by:
  * Adding the token which you obtain by creating your bot with Discord.
  * Add the channel(s) that you wish for you bot to send the message to.
    <b>NOTE: Your bot must have permission to write in the channel. This is done when adding the bot to the Discord server or through roles.</b>
  * Add any subreddits you wish to use.<p>
### 3. If you wish for the program to do it automatically then look into a way of scheduling a task for your specific OS. (For Windows use Task Scheduler, for Linux use Cron(? haven't used Linux a lot)). Then schedule the execution of the "start.bat" script whenever you wish.<p>
If you don't want to schedule it using the start.bat file or you're on linux then schedule the command ``python -m HentaiBot.py`` instead but be sure to change the working directory to the folder in which this is located in or else you'll get an error due to the bot not being able to find "config.yaml".
 
If you are doing this on Linux then make an [issue](https://github.com/HiruNya/HentaiBot/issues) so that I can make a bash script.
### 4. If you wish to run the program manually just, run the "start.bat" script.
- Tip: just create a shortcut of the start.bat and move it in your autostart folder if you use windows. It will always check for new hentai when you start your pc.

## The Config File:
### The whole bot works depending on what you put in the [config file](https://github.com/HiruNya/HentaiBot/blob/master/config.yaml).
This is how it starts off as. Feel free to add/edit values that you see fit.
(Text after the # are counted as comments and wont be read by the bot).
```yaml
channels: [] # The channel id that you wish to send this to e.g. channels: ['12345', '64789'] (Quotation Marks Necessary)
token: # e.g. token: 12345 (No Quotation Marks Necessary)
posts: 3 # The default number of posts to make
hentai_haven: {
  enabled: True, # Set to True if you wish to use the /r/hentai_irl feature
  posts: 0, # Number of posts to post, if the value is below 1 then it will use the default post number
  channels: [], # The channels in the same format as above. Leave empty if you wish to use the same channels.
  embed_colour: FF0000, # The Hexadecimal (RRGGBB) or Decimal value for the embed colour of the post. (Red by default)
    # Red = FF0000 or 16711680
    # Green = 00FF00 or 65280
    # Blue = 0000FF  or 255 etc.
  blacklist: [ # A blacklist where you can enter tags that you don't want to appear
    # e.g.
    # "netorare",
    # "cheating", etc. (Tags do not have to be case-sensitive)
    # In this case videos with the tags "netorare" and "cheating" would not be posted.
    # Adding "" is probably not required but is recommended especially if you want to block a tag like "Big Boobs", which has a space in the middle.
  ],
}
reddit: { # You can add as many subreddits as you want just make an entry using the template below.  
  # Example:
  # Uncomment (remove the hashtags at the start) the text below to make the bot post reddit.com/r/hentai_irl posts
  # hentai_irl: { # This is the name of the subreddit. e.g. www.reddit.com/r/{subreddit_name}
  #  posts: 0, # Number of posts to post, if the value is below 1 then it will use the default post number
  #  channels: [], # The channels in the same format as above. Leave empty if you wish to use the same channels.
  # }, <- Remember to add the comma at the end.
}
```
Having trouble with certain settings? Want to make a suggestion? Feel free to create an [issue](https://github.com/HiruNya/HentaiBot/issues).
