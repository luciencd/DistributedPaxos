import sys
from distributed_site import Site
from communicator import Communicator
import log

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
    tweet_text = input("Enter your tweet:")
    return event(site,"tweet",tweet_text)

def collect_block(site,blocker,blocked):
    blocked_text = input("Enter your block:")
    return event(site,"block",blocked_text)

def collect_unblock(site,blocker,blocked):
    unblocked_text = input("Enter your unblock:")
    return event(site,"unblock",unblocked_text)

def pretty_print_tweets(list_tweets):
    string = ""
    #pretty print
    return string

def main():
    own_port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    own_addr = "127.0.0.1" #TODO: detecting IP is annoying (open a socket to internet, check hostname)
    own_binding = (own_addr,own_port);

    nodes = readConfig()

    #communicator = Communicator(nodes,own_binding)
    #communicator.start()

    Log.start()

    user_option = ""
    while user_option != "quit":
        user_option = input("Select an option: ")

        if user_option == "tweet":
            new_tweet = collect_tweet()
            Log.tweet(new_tweet)
            #communicator.tweet()

        elif user_option =="view":
            list_tweets = Log.view()

        elif user_option =="block":
            new_block = collect_block()
            Log.block(new_block)

        elif user_option =="unblock":
            new_unblock = collect_unblock()
            Log.unblock(new_unblock)

        else:
            print("Invalid operation.")

    communicator.stop()
    Log.stop()




if __name__ == "__main__":
    main()
