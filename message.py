
import json
from event import event

class Message:
    def __init__(self,clock,events):
        self.clock = clock
        self.events = events

    def toJSON(self):
        return json.dumps(self, default=lambda x: x.__dict__)

    @staticmethod
    def fromJSON(payload):
        new_msg = Message([],[])
        new_msg.__dict__ = json.loads(payload)
        #json.loads deserializes the object incorrectly
        for row in range(0,len(new_msg.clock),1):
            new_msg.clock[row] = [x[0] for x in new_msg.clock[row]]
        new_msg.events = [event(e["site"], e["op"], e["data"], e["truetime"], e["timestamp"]) for e in new_msg.events]
        return new_msg
