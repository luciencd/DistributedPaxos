
import json

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
        return new_msg
