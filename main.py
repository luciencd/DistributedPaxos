import sys
import os
from communicator import Communicator
from log import Log
from event import event, EventTypes


DEFAULT_FILENAME = "config.txt"
DEFAULT_PORT = 8923

def readConfig():
    configFile = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILENAME

    nodes = []
    with open(configFile) as f:
        file_lines = f.readlines()
        nodes = [(addr, int(port))
                   for line in file_lines
                    for addr,port in [line.strip().split(":")]]

    return nodes


def collect_tweet(site):
    tweet_text = input("Enter your tweet: ")
    return event(site, EventTypes.TWEET, tweet_text)

def collect_block(site):
    blocked_text = input("Enter your block: ")
    if not blocked_text.isdigit():
        return None
    return event(site, EventTypes.BLOCK, str(site) + event.DELIM + blocked_text)

def collect_unblock(site):
    unblocked_text = input("Enter your unblock: ")
    if not unblocked_text.isdigit():
        return None
    return event(site, EventTypes.UNBLOCK, str(site) + event.DELIM + unblocked_text)


def main():
    own_port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    own_addr = "127.0.0.1" #TODO: detecting IP is annoying (open a socket to internet, check hostname)
    own_binding = (own_addr,own_port);

    nodes = readConfig()

    communicator = Communicator(nodes,own_binding)
    communicator.start()

    Log.start(len(nodes), communicator.id)

    user_option = ""
    while user_option != "quit":
        user_option = input("Select an option: ")

        if user_option == "tweet":
            new_tweet = collect_tweet(communicator.id)
            Log.tweet(new_tweet)
            communicator.tweet()

        elif user_option =="view":
            list_tweets = Log.view()
            print()
            print(*list_tweets, sep="\n\n", end = "\n\n")

        elif user_option =="block":
            new_block = collect_block(communicator.id)
            if new_block != None:
                Log.block(new_block)
            else:
                print("Invalid block, doing nothing.")

        elif user_option =="unblock":
            new_unblock = collect_unblock(communicator.id)
            if new_unblock != None:
                Log.unblock(new_unblock)
            else:
                print("Invalid unblock, doing nothing.")
                
        elif user_option == "reset":
            ##to make sure the system is fault tolerant.
            print("Deleting entire database.")
            Log.reset()
        elif user_option =="quit":
            print("Shutting down...")

        else:
            print("Invalid operation.")

    communicator.stop()
    Log.stop()




if __name__ == "__main__":
    main()
