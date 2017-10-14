import sys
import threading
import socket
from message import Message
from log import Log

class Channel:
    DELIM = "\n"

    def __init__(self, id_, sock_):
        self.id = id_
        self.socket = sock_
        self.thread = None
        self.closed = False


    def start(self, announce_self=-1):
        self.thread = threading.Thread(target=self.channel_thread)
        self.thread.start();
        if announce_self > 0:
            #if this is greater than zero, it represents my parent site id, and
            #I should tell the foreign communicator who I am (because I'm initiating)
            self.send_msg(str(announce_self))

    def stop(self):
        if self.socket != None:
           self.socket.shutdown(socket.SHUT_RDWR)
           self.socket.close()
           self.socket = None
        if self.thread != None:
            self.thread.join()

        self.closed = True

    def send_msg(self, msg):
        delimited_message = str(msg) + Channel.DELIM
        try:
            if self.socket != None:
                print("sending message",delimited_message)
                self.socket.send(delimited_message.encode())

        except Exception as e:
            #writing on the pipe failed, there was probably a crash...
            #kill the thread so we can regen it when they come back
            self.stop()

    def channel_thread(self):
        message = "init"
        while message != "":
            try:
                message = self.socket.recv(4096).decode()

                while message != "" and not Channel.DELIM in message:
                    message = message + self.socket.recv(4096).decode()

                if message != "":
                    print("received message")
                    message_converted = Message.fromJSON(message.strip())
                    Log.receive(message_converted, self.id)

            except OSError as e:
                if e.errno == 10053 or e.errno == 10054:
                    #the socket has been closed, flee this thread
                    message = ""
                else:
                    raise e
