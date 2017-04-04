#! python3
# chatbot.py
# Bot to counter the words used in a slack channel

import os
import time
import string
from slackclient import SlackClient



# constants
BOT_NAME = 'count_bot'


WORD_CACHE = {}
#this is used later for striping punctuation
translator = str.maketrans('', '', string.punctuation)

# instantiate SlackClient
slack_client = SlackClient(os.environ.get('BOT_TOKEN'))


def get_bot_id(BOT_NAME):
    """this will grab the ID of the bot"""
    api_call = slack_client.api_call('users.list')
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            if "name" in user and user.get('name') == BOT_NAME:
                print("Bot ID of '"+user['name']+"' is "+user.get('id'))
                BOT_ID = user.get('id')
    if BOT_ID:
        return BOT_ID
    else:
        return None


def find_top_10():
     """ find the top 10 words stored in the WORD_CACHE then print them in the channel """
     global WORD_CACHE
     words_array = [[key, WORD_CACHE[key]] for key in sorted(WORD_CACHE, key=WORD_CACHE.get, reverse=True)]
     message = "Here are the top 10 most common words used by the room in the last 5 minutes. \n\n"
     for word in words_array[:10]:
          message = message + word[0].upper() + ": used " + str(word[1]) + " times. \n "
     slack_client.api_call("chat.postMessage", channel='general',text=message, as_user=True)

     WORD_CACHE = {}

def word_counter(chat_input):
     """take all the words used by everyone not including this bot and put them in a dictionary"""
     words = chat_input.split()
     for word in words:
          #strip the word of punctuation
          word = word.translate(translator)
          #if it's in the dictionary, add the value by one, otherwise add it and set the value as one
          if word.lower() in WORD_CACHE:
               WORD_CACHE[word.lower()] += 1
          else:
               WORD_CACHE[word.lower()] = 1


def parse_slack_output(slack_rtm_output, BOT_ID, starttime):
     """
         The Slack Real Time Messaging API is an events firehose.
         this will read the output and if it sees a message, and it's not from itself, it calls the word_counter function to store the words in the message
     """
     output_list = slack_rtm_output
     if output_list and len(output_list) > 0:
         for output in output_list:
             print(output)
             if output and 'text' in output and BOT_ID not in output['user']:
                 #throw that text into the word_counter
                 word_counter(output['text'])
     # call the top 10 function every 5 min (300 seconds).  It's not EXACTLY 5 min, it's within a second because the start time and when it fires wont line up exactly.
     if (300 -(time.time() - starttime) % 300.0) < 1:
         find_top_10()
     return None

if __name__ == "__main__":
     READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
     BOT_ID = get_bot_id(BOT_NAME)
     starttime = time.time()
     if slack_client.rtm_connect() and BOT_ID is not None:
         print("CountBot connected and running!")
         slack_client.api_call("chat.postMessage", channel='general',text="I'm now listening to this channel. I will report the top 10 words used every 5 minutes.", as_user=True)
         while True:
             parse_slack_output(slack_client.rtm_read(), BOT_ID, starttime)
             time.sleep(READ_WEBSOCKET_DELAY)
     else:
         print("Connection failed. Invalid Slack token or bot ID?")
