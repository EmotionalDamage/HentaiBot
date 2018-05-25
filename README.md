# HentaiBot
A Discord Bot that posts from HentaiHaven, Hanime.tv, and Reddit Subreddits. This branch runs on AWS.

## Note: (for only this branch)
This specific branch is meant to be able to run on AWS (Amazon Web Services). This requires access to DynamoDb and runs as an AWS Lambda.
If you would like to know how to set this up (as this was only meant for me), please make an issue and I'll try help you. Changes in the code WILL be needed to get this working for you as I can't be bothered making some special API like I did with the original version. This is meant to be used with a HTTPs trigger and it will return info as a HTML file.

\[WARNING: All Links Are NSFW]

It uses the RSS feed at www.hentaihaven.org/feed to check for new releases, if it finds a new one then it will send a discord message to the channels specified in the config.yaml file.

It also scrapes the [hanime.tv](https://staging.hanime.tv) website to check for new releases, and does the same as above. You can also choose what list to use (Recent Uploads, Trending, etc.)

It can also go on www.reddit.com/r/{subreddit_name} and post the top posts. (e.g. you can post the top posts from [r/hentai_irl](https://www.reddit.com/r/hentai_irl))

These features can all be edited in the config.yaml file.

For those who first run the program, you may notice that you get an error because you're being 'rate limited'. This just means that since your bot is sending all these posts at the same time, Discord thinks you're spamming and so has decided to block the bot from posting for a few seconds. After waiting for a few seconds, the next time the bot runs should work fine as the bot would have kept a record of all the latest posts it saw and therefore will stop posting when it reaches them.
If this error keeps popping up a lot make an [issue](https://github.com/HiruNya/HentaiBot/issues) as I might be able to implement a feature that pauses between different kinds of posts to ensure that you don't get rate limited.

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
  enabled: True, # Set to True if you wish to use the HentaiHaven feature
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
hanime_tv: {
  enabled: False, # Set to True if you wish to use the HAnime.tv feature
  posts: 0, # Number of posts to post, if the value is below 1 then it will use the default post number
  channels: [], # The channels in the same format as above. Leave empty if you wish to use the same channels.
  embed_colour: FF00FF, # The Hexadecimal (RRGGBB) or Decimal value for the embed colour of the post. (Purple by default)
  section: "Recent Uploads" # Which list you want to use. (If you go on the site, you will see multiple lists.)
  # The sections are: (Case does not matter)
  # - Recent Uploads
  # - New Releases
  # - Trending
  # - Random
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
