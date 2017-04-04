# eh-chatbot


This is a bot that is written in Python 3 for your Slack Channel.  I wrote this in a few hours one afternoon.

Once running, it will save all the words used in the channel to a dictionary. Then after 5 minutes, it will output the top 10 most used words.  It will reset the dictionary after it prints the list.

It will repeat this until the process is killed.

# Configuration
Install the slack client API package (`pip3 install slackclient`) or install the requirements.txt (`pip3 install -r requirements.txt`)

You will need a [custom bot](http://my.slack.com/apps/manage/custom-integrations) integration token for your Slack team.
Once you have created the bot, invite it to the general channel.  If you want to use a different channel, you will have to modify the lines with "slack_client.api_call" to whatever channel you invited it to.

Set that token as a local environment variable named `BOT_TOKEN`.

Make sure the name of your bot matches the name of the BOT_NAME in the count_bot.py file

# Usage

If all the configuraton is done properly, you should be able to just run it with `python3 count_bot.py`

It should send a message in the terminal and in the slack channel to let you know that it's working.  

To stop it, hit `control-c`
