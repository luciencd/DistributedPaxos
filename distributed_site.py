import select
import os
import sys

class Site:

    def __init__(self, communicator_):
        #self.log = Log()
        self.communicator = communicator_
        self.id = self.communicator.id
        if self.id == None:
            raise LookupError("%s is not present in the config file." %binding_)

        self.database = ""#create database to hold log.



    def block(self,message):
        #communicate with MySQL instance.
        raise NotImplementedError

    def unblock(self,message):
        raise NotImplementedError


    def tweet(self,message):
        raise NotImplementedError

    def receive(self,message):
        raise NotImplementedError

    def start(self):
        self.communicator.start()

    def stop(self):
        self.communicator.stop()
