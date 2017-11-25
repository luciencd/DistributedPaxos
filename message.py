
import json
from event import event

class Message:
    def toJSON(self):
        return json.dumps(self, default=lambda x: x.__dict__)


class Prepare(Message):
    self.msg_type = "prepare"
    def __init__(self,n,index):
        self.n = n #proposal number.
        self.index = index #what index are we consensusing for multi-paxos

class Promise(Message):
    self.msg_type = "promise"
    def __init__(self,acceptedProposal,acceptedValue,index):
        self.acceptedProposal = acceptedProposal #proposal number.
        self.acceptedValue = acceptedValue #consensus choice value
        self.index = index #what index are we consensusing for multi-paxos

class AcceptRequest(Message):
    self.msg_type = "acceptRequest"
    def __init__(self,n,events):
        self.n = n
        self.value = events#really a list of size one

class Accepted(Message):
    self.msg_type = "accepted"
    def __init__(self,minProposal):
        self.minProposal = minProposal

class MessageReader:
    @staticmethod
    def fromJSON(payload):
        dict_data = json.loads(payload)
        if(dict_data["msg_type"]=="prepare"):
            Prepare(dict_data["n"],dict_data["index"])
        #json.loads deserializes the object incorrectly
        for row in range(0,len(new_msg.clock),1):
            new_msg.clock[row] = [x[0] for x in new_msg.clock[row]]
        new_msg.events = [event(e["site"], e["op"], e["data"], e["truetime"], e["name"], e["timestamp"]) for e in new_msg.events]
        return new_msg

class Data(Message)
    def __init__(self,clock,events):
        self.clock = clock
        self.events = events

    def toJSON(self):
        return json.dumps(self, default=lambda x: x.__dict__)
