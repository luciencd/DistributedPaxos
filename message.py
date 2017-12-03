
import json
from event import event

class MessageNotRecognizedError(ValueError): pass

class Message:
    def toJSON(self):
        return json.dumps(self, default=lambda x: x.__dict__)


class Prepare(Message):

    def __init__(self,proposalNumber,index,process):
        self.msg_type = "prepare"
        self.n = proposalNumber #proposal number.
        self.i = index
        self.p = process

class Promise(Message):

    def __init__(self,acceptedProposal,acceptedValue,index,process):
        self.msg_type = "promise"
        self.n = acceptedProposal #proposal number (n).
        self.v = acceptedValue #consensus choice value (event)
        self.i = index #what index are we consensusing for multi-paxos
        self.p = process

class AcceptRequest(Message):

    def __init__(self,acceptedProposal,acceptedValue,index,process):
        self.msg_type = "acceptRequest"
        self.n = acceptedProposal #proposal number (n).
        self.v = acceptedValue #consensus choice value (event)
        self.i = index #what index are we consensusing for multi-paxos
        self.p = process

class Accepted(Message):

    def __init__(self,minProposal,acceptedValue,index,process):
        self.msg_type = "accepted"
        self.n = minProposal
        self.i = index
        self.p = process
        self.v = acceptedValue
        #unsure if we need to include value v... if proposer(n) can't be < n, and if it is greater than proposer(n), the proposer failed
        ##and if it is equal, the proposer(n), already knows its own value

class Commit(Message):
    def __init__(self,committedValue,index,process):
        self.msg_type = "commit"
        self.v = committedValue
        self.i = index
        self.p = process

class MessageReader:
    @staticmethod
    def fromJSON(payload):
        ##getting data from payload as a dictionary
        dict_data = json.loads(payload)

        if(dict_data["msg_type"] == "prepare"):
            new_msg = Prepare(dict_data["n"],dict_data["i"],dict_data["p"])
        elif(dict_data["msg_type"] == "promise"):
            e = dict_data["v"]
            if(e != None):
                v = event(e["site"], e["op"], e["data"], e["truetime"], e["name"], e["timestamp"])
                new_msg = Promise(dict_data["n"],v,dict_data["i"],dict_data["p"])
            else:
                new_msg = Promise(dict_data["n"],None,dict_data["i"],dict_data["p"])

        elif(dict_data["msg_type"] == "acceptRequest"):
            e = dict_data["v"]
            if(e != None):
                v = event(e["site"], e["op"], e["data"], e["truetime"], e["name"], e["timestamp"])
                new_msg = AcceptRequest(dict_data["n"],v,dict_data["i"],dict_data["p"])
            else:
                new_msg = AcceptRequest(dict_data["n"],None,dict_data["i"],dict_data["p"])
        elif(dict_data["msg_type"] == "accepted"):
            e = dict_data["v"]
            if(e != None):
                v = event(e["site"], e["op"], e["data"], e["truetime"], e["name"], e["timestamp"])
                new_msg = Accepted(dict_data["n"],v,dict_data["i"],dict_data["p"])
            else:
                new_msg = Accepted(dict_data["n"],None,dict_data["i"],dict_data["p"])##not actually possible though
        elif(dict_data["msg_type"] == "commit"):
            e = dict_data["v"]
            if(e != None):
                v = event(e["site"], e["op"], e["data"], e["truetime"], e["name"], e["timestamp"])
                new_msg = Commit(dict_data["n"],v,dict_data["i"],dict_data["p"])
            else:
                new_msg = Commit(dict_data["n"],None,dict_data["i"],dict_data["p"])
        else:
            raise MessageNotRecognizedError

        return new_msg
