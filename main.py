import sys
from distributed_site import Site
from communicator import Communicator

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


def collect_tweet():
    tweet_text = input("Enter your tweet:")
    return tweet_text


def main():
    own_port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    own_addr = "127.0.0.1" #TODO: detecting IP is annoying (open a socket to internet, check hostname)
    own_binding = (own_addr,own_port);

    nodes = readConfig()

    this_site = Site(Communicator(nodes,own_binding))
    this_site.start()

    user_option=""
    while user_option != "quit":
        user_option = input("Select an option: ")
        if user_option == "tweet":
            new_tweet = collect_tweet()
            this_site.tweet(new_tweet)
        elif user_option == "quit":
            this_site.stop()
        else:
            print("Invalid operation.")





if __name__ == "__main__":
    main()
