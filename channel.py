import sys
import threading
import socket

class Channel:
    DELIM = "\n"

    def __init__(self, id_, sock_):
        self.id = id_
        self.socket = sock_
        self.thread = None


    def start(self, announce=False):
        self.thread = threading.Thread(target=self.channel_thread)
        self.thread.start();
        if announce:
            self.send_msg(str(self.id))

    def stop(self):
        if self.socket != None:
           self.socket.shutdown(socket.SHUT_RDWR)
           self.socket.close()
           self.socket = None
        if self.thread != None:
            self.thread.join()

    def send_msg(self, msg):
        delimited_message = str(msg) + Channel.DELIM
        self.socket.send(delimited_message.encode())

    def channel_thread(self):
        message = "init"
        while message != "":
            try:
                message = self.socket.recv(4096).decode().strip()
                #TODO: might need to split on delim instead of strip()
                #TODO: signal that a tweet should be recorded... might need to pass a handle to the DB down here
            except OSError as e:
                if e.errno == 10053 or e.errno == 10054:
                    #the socket has been closed, flee this thread
                    message = ""
                else:
                    raise e
