import itertools
import threading
import socket
from channel import Channel

class Communicator:

    def __init__(self, nodes_, binding_):
        #store the list of sites we know about
        self.nodes = nodes_
        #store an inverted lookup table where knowing an addr and port allows us
        #to find a node number -- this will be useful for processing socket data
        self.nodes_by_addr = dict(zip(self.nodes, itertools.count()))
        #look ourselves up in the reversed table to find our Site ID
        self.id = self.nodes_by_addr.get(binding_)
        #create a placeholder array of our communication channels to other sites
        #this will be populated by open_connections() and listener.accept()
        self.channels = [None for _ in self.nodes]
        self.listener = None
        #track a shutdown flag so the socket thread knows when to wrap up
        self.begin_shutdown = False


    '''
    function: start
    Launch the socket thread to begin listening for events from other sites
    '''
    def start(self):
        self.listener_thread = threading.Thread(target=self.message_listener)
        self.listener_thread.start();

    '''
    function: stop
    Toggle the shutdown flag, then close all the socket connections.
    Closing the connections here should wake up the socket thread.
    NOTE: this may cause an ugly data condition if we're in the middle of a read...?
    '''
    def stop(self):
        self.begin_shutdown = True
        for i in range(0, len(self.channels),1):
            channel = self.channels[i]
            if channel != None:
                channel.stop()

        self.listener.close()
        self.listener_thread.join()
    '''
    function: make_socket
    Initialize a new socket with some useful defaults we'll use throughout the program.
    Namely, make it a non-blocking INET TCP socket that doesn't reserve its address after closing.
    '''
    def make_socket(self):
        #declare a new INET (non-local) streaming (TCP) socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #avoid some of the socket bugs mentioned in class
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock


    '''
    function: open_connections
    Attempt to regenerate the list of communication channels to other nodes.
    Each entry in self.channels corresponds to the same-numbered entry in self.nodes
    '''
    def open_connections(self):
        for i in range(0, len(self.channels),1):
            new_socket = None
            if self.channels[i] == None and i != self.id:
                new_socket = self.make_socket()
                try:
                    new_socket.connect(self.nodes[i])
                    self.channels[i] = Channel(i, new_socket)
                    self.channels[i].start(True)
                except OSError as e:
                    if e.errno != 10061:
                        raise e

    '''
    function: message_listener
    The main event loop for the socket ready to accept new connections
    '''
    def message_listener(self):
        #start by fetching our own binding from the loaded config, to get our port
        binding = self.nodes[self.id]
        self.listener = self.make_socket()
        #prepare the socket for listening
        self.listener.bind(('0.0.0.0', binding[1]))
        self.listener.listen(len(self.nodes))
        self.open_connections()

        while False == self.begin_shutdown:
            try:
                new_sock, new_addr = self.listener.accept()
                n = int(new_sock.recv(4096).decode().strip())
                if self.channels[n] != None:
                    self.channels[n].close()
                self.channels[n] = Channel(n, new_sock)
                self.channels[n].start()
            except OSError as e:
                if e.errno != 10038 or not self.begin_shutdown:
                    raise e

        self.listener.close()

        return True

    #def send_message():
    def tweet():
        #get users that are not blocked by this site.
        #for each user, get data from Log and T that correspond to what those users don't know.
            #get T from log
            #get NP from get_events_to_sent_to_j(j)
            #msg = create the send message data (JSON) as (T,NP)
            #call channel.send_msg(msg)
            #
