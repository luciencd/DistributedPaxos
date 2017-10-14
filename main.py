import sys
import os
from communicator import Communicator
from log import Log
from event import event, EventTypes
from datetime import datetime, date
from dateutil import tz

DEFAULT_FILENAME = "config.txt"
DEFAULT_PORT = 8923

def readConfig():
    configFile = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILENAME

    nodes = []
    with open(configFile) as f:
        file_lines = f.readlines()
        nodes = [(addr, int(port),name)
                   for line in file_lines
                    for addr,port,name in [line.strip().split(":")]]
    return (list(map(lambda x: x[:-1],nodes)),list(map(lambda x: x[-1],nodes)))


def collect_tweet(site,now_time,self_name):
    tweet_text = input("Enter your tweet: ")

    #print(now_time.astimezone(tz.tzlocal()))
    return event(site, EventTypes.TWEET, tweet_text,now_time,self_name)

def collect_block(site,now_time,self_name):
    blocked_text = input("Enter your block: ")
    if not blocked_text.isdigit():
        return None
    return event(site, EventTypes.BLOCK, str(site) + event.DELIM + blocked_text,now_time,self_name)

def collect_unblock(site,now_time,self_name):
    unblocked_text = input("Enter your unblock: ")
    if not unblocked_text.isdigit():
        return None
    return event(site, EventTypes.UNBLOCK, str(site) + event.DELIM + unblocked_text,now_time,self_name)


def main():
    own_port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    own_addr = "127.0.0.1" #TODO: detecting IP is annoying (open a socket to internet, check hostname)
    own_binding = (own_addr,own_port);

    nodes,names = readConfig()

    communicator = Communicator(nodes,names,own_binding)
    communicator.start()


    Log.start(len(nodes), communicator.id)

    user_option = ""
    while user_option != "quit":
        user_option = input("Select an option: ")
        #get current time.
        now_time = datetime.utcnow()
        now_time = now_time.replace(tzinfo=tz.tzutc()).replace(microsecond=0)
        #print(now_time.replace(microsecond=0))
        if user_option == "tweet":
            new_tweet = collect_tweet(communicator.id,now_time,communicator.name)
            Log.tweet(new_tweet)
            communicator.tweet()

        elif user_option =="view":
            list_tweets = Log.view()
            print()
            print(*list_tweets, sep="\n\n", end = "\n\n")

        elif user_option =="block":
            new_block = collect_block(communicator.id,now_time,communicator.name)
            if new_block != None:
                Log.block(new_block)
            else:
                print("Invalid block, doing nothing.")

        elif user_option =="unblock":
            new_unblock = collect_unblock(communicator.id,now_time,communicator.name)
            if new_unblock != None:
                Log.unblock(new_unblock)
            else:
                print("Invalid unblock, doing nothing.")
        elif user_option == "name":
            print("My name is:",communicator.name)

        elif user_option =="quit":
            print("Shutting down...")

        else:
            print("Invalid operation.")

    communicator.stop()
    Log.stop()




if __name__ == "__main__":
    main()
