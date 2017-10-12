
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
        new_msg.clock = [[x[0], y[0], z[0]] for x,y,z in new_msg.clock]
        new_msg.events = [event(e["site"], e["op"], e["data"], e["timestamp"]) for e in new_msg.events]
        return new_msg
