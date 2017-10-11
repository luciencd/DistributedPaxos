class event:
    def __init__(self,site):
        self.timestamp = 0
        self.site = site.id
        self.op = ""
        self.data = ""

    def get_tweet():
        #what if a blocking thingy calls get_tweet()?
        if(self.op == "Tweet"):
            return self.data
        else:
            return None

    def get_blocker():
        if(self.op == "Block" or self.op == "Unblock"):
            return self.data.split(",")[0]
        else:
            return None

    def get_blocked():
        if(self.op == "Block" or self.op == "Unblock")
            return self.data.split(",")[1]
        else:
            return None
