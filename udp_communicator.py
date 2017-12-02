import itertools
import threading
import socket
from message import Message,MessageReader

#subclass communicator into UDP communicator and TCP communicator.
class Communicator:
    DELIM = "\n"
    def __init__(self, nodes_):
        #store the list of sites we know about
        self.nodes = nodes_

        #store an inverted lookup table where knowing an addr allows us
        #to find a node number -- this will be useful for processing socket data
        self.nodes_by_addr = dict(zip(map(lambda x:x[0],self.nodes), itertools.count()))
        #self.id = self.nodes_by_addr.get(str(binding_[0])+str(binding_[1]))
        #track a shutdown flag so the socket thread knows when to wrap up
        self.begin_shutdown = False

        self.partial_received = {site[0]: "" for site in self.nodes}


    def addClient(self,client):
        self.client = client
    '''
    function: start
    Launch the socket thread to begin listening for events from other sites
    '''
    def start(self, id):
        print("Starting",id)
        self.id = id
        self.listener_thread = threading.Thread(target=self.message_listener)
        self.listener_thread.start();

    '''
    function: stop
    Toggle the shutdown flag, then close the socket connection.
    Closing the connections here should wake up the socket thread.
    '''
    def stop(self):
        self.begin_shutdown = True
        self.listener.close()
        self.listener_thread.join()

    '''
    function: make_socket
    Initialize a new socket with some useful defaults we'll use throughout the program.
    Namely, make it a non-blocking INET UDP socket that doesn't reserve its address after closing.
    '''
    def make_socket(self):
        #declare a new INET (non-local) dgram (UDP) socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #avoid some of the socket bugs mentioned in class
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock



    '''
    function: message_listener
    The main event loop for the socket ready to receive messages
    '''
    def message_listener(self):
        #start by fetching our own binding from the loaded config, to get our port
        binding = self.nodes[self.id]
        self.listener = self.make_socket()
        #prepare the socket for listening
        self.listener.bind(('0.0.0.0', binding[1]))

        while False == self.begin_shutdown:
            try:
                data,sender = self.listener.recvfrom(4096)

                sender_addr = sender[0]


                if sender_addr != self.nodes[self.id] and self.partial_received.get(sender_addr) != None: #when we send to ourselves or don't get a valid addr, we've been shut down

                    self.partial_received[sender_addr] = self.partial_received[sender_addr] + data.decode()
                    sender_id = self.nodes_by_addr.get(sender_addr)

                    if sender_id != None:
                        while Communicator.DELIM in self.partial_received[sender_addr]:
                            split = self.partial_received[sender_addr].split(Communicator.DELIM)
                            next_msg = split[0]

                            self.partial_received[sender_addr] = Communicator.DELIM.join(split[1:])

                            received_message = MessageReader.fromJSON(next_msg.strip())
                            print("Message Received:",received_message.__dict__,"from:",sender_addr)
                            ##now we have the message object

                            self.client.readMessage(received_message)
                            #Log.receive(message_converted, sender_id)

            except OSError as e:
                if e.errno != 10038 or not self.begin_shutdown:
                    raise e

        self.listener.close()

        return True

    def propose(self,propose_message):
        broadcaster = threading.Thread(target=self.broadcast_synod,args= (propose_message,))
        broadcaster.daemon = True #implicitly detach thread in start (we don't care about return or joining)
        broadcaster.start()

    def promise(self,promise_message):
        sender = threading.Thread(target=self.send_synod,args= (promise_message,))
        sender.daemon = True #implicitly detach thread in start (we don't care about return or joining)
        sender.start()

    def acceptRequest(self,accept_request_message):
        broadcaster = threading.Thread(target=self.broadcast_synod,args= (accept_request_message,))
        broadcaster.daemon = True #implicitly detach thread in start (we don't care about return or joining)
        broadcaster.start()

    def accept(self,accept_message):
        sender = threading.Thread(target=self.send_synod,args= (accept_message,))
        sender.daemon = True #implicitly detach thread in start (we don't care about return or joining)
        sender.start()

    ##when we want to send a message from the proposers to everyone (all nodes) (because all nodes/clients are acceptors)
    def broadcast_synod(self,message):#will send out proposals and acceptRequests to all processes.
        print("broadcasting Synod algorithm.")
        sites = set(range(0,len(self.nodes)))
        sites.remove(self.id)
        ##this will be a quorum of sites, all of them

        #figure out what this does.
        outgoing_sock = self.make_socket()
        outgoing_sock.settimeout(2)
        for site in sites:
            m = message.toJSON() + Communicator.DELIM
            print("sending to:",self.nodes[site])
            outgoing_sock.sendto(m.encode(), self.nodes[site])

        outgoing_sock.close()

    ##when we want to send a single message from an acceptor back to the proposer.
    def send_synod(self,message):
        outgoing_sock = self.make_socket()
        outgoing_sock.settimeout(2)

        m = message.toJSON() + Communicator.DELIM
        outgoing_sock.sendto(m.encode(), self.nodes[message.p])

        outgoing_sock.close()
