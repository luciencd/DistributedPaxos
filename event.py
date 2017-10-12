
class EventTypes:
    BLOCK="block"
    UNBLOCK="unblock"
    TWEET="tweet"

class event:
    DELIM = ","
    def __init__(self,site,op,body,timestamp=-1):
        self.site = site
        self.op = op
        self.data = body
        self.timestamp = timestamp

    def get_tweet(self):
        #what if a blocking thingy calls get_tweet()?
        if(self.op == EventTypes.TWEET):
            return self.data
        else:
            return None

    def get_blocker(self):
        if(self.op == EventTypes.BLOCK or self.op == EventTypes.UNBLOCK):
            return int(self.data.split(event.DELIM)[0])
        else:
            return None

    def get_blocked(self):
        if(self.op == EventTypes.BLOCK or self.op == EventTypes.UNBLOCK):
            return int(self.data.split(event.DELIM)[1])
        else:
            return None


    def __str__(self):
        return "{} by {} at {}:\n   {}".format(self.op.title(),self.site,self.timestamp,self.data)
