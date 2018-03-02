
# HentaiBot
Well... a bot that checks HentaiHaven.org for new hentai and if it finds a new one, sends the info as a message to a Discord channel(s)

It uses the RSS feed at www.hentaihaven.org/feed \[WARNING: NSFW] to check for new releases, if it finds a new one then it will send a discord message to the channels specified in the config.yaml file.

It can also go on https://www.reddit.com/r/hentai_irl/ and/or /r/hentai and post the top posts. (By default posts the top 3 but this can be changed in the config.yaml file).
This feature can be enabled in the config.yaml file.

# Dependencies:
- feedparser  (For reading the RSS feed)
- yaml  (For reading and writing to the config file)
- requests  (For writing a POST request to Discord)
- json <b>\[Standard Library]</b>  (For writing the information sent to Discord)
- xml <b>\[Standard Library]</b>  (For reading some of the XML text)

# Setup:
1. Make sure that the dependencies not in the standard library are installed using <b>pip</b> or some other method<br>
e.g. to install "feedparser" write ```pip install feedparser``` in the command prompt,<br>
  to install "yaml" write ```pip install pyYAML```,<br>
  and to install "requests" write ```pip install requests```.
2. Configure the config.yaml by:
  - Adding the token which you obtain by creating your bot with Discord.
  - Add the channel(s) that you wish for you bot to send the message to.
    <b>NOTE: Your bot must have permission to write in the channel. This done when adding the bot to the Discord server or through roles.</b>
3. If you wish for the program to do it automatically then look into a way of scheduling a task for your specific OS. (For Windows use Task Scheduler, for Linux use Cron(? haven't used Linux a lot)). Then schedule the execution of the "start.bat" script whenever you wish.
4. If you wish to run the program manually just, run the "start.bat" script.
- Tip: just create a shortcut of the start.bat and move it in your autostart folder if you use windows. It will always check for new hentais when you start your pc.

# Source \[ALL NSFW!]:
- https://www.reddit.com/r/hentai_irl/
- https://www.reddit.com/r/hentai/
- http://hentaihaven.org/feed/
