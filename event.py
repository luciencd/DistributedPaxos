from datetime import datetime
from dateutil import tz

class EventTypes:
    BLOCK="block"
    UNBLOCK="unblock"
    TWEET="tweet"

class event:
    DELIM = ","
    def __init__(self,site,op,body,truetime,timestamp=-1):
        self.site = site
        self.op = op
        self.data = body
        self.timestamp = timestamp
        #when constructing this, assume the tweet's time is in UTC, and should be converted in the __str__ "view"
        self.truetime = truetime

    def get_tweet(self):
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

    def related_unblock_exists(self, event_list):
        linked_unblocks = list(filter(lambda e: e.site == self.site \
            and e.data == self.data \
            and e.op == EventTypes.UNBLOCK \
            and self.op == EventTypes.BLOCK, event_list))

        return len(linked_unblocks) > 0


    def __str__(self):
        print(self.truetime)
        utctime = datetime.strptime(self.truetime,'%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=tz.tzutc())
        localtime = utctime.astimezone(tz.tzlocal())
        minute_localtime = localtime.strftime('%Y-%m-%d %H:%M:%S')
        return "{} by {} at {}:\n   {}".format(self.op.title(),self.site,minute_localtime,self.data)
