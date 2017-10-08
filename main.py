import sys

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


def main():
    own_port = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PORT
    own_addr = "127.0.0.1" #TODO: detecting IP is annoying (open a socket to internet, check hostname)

    nodes = readConfig()




if __name__ == "__main__":
    main()
