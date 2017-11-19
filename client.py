class Proposer(Agent):
    pass

class Learner(Agent):
    pass

class Accepter(Agent):
    pass

class DistinguishedLearner(Learner):
    pass

class DistinguishedProposer(Proposer):
    pass

class Client:
    self.proposer = Proposer()
    self.accepter = Accepter()
    self.learner = Learner()
    #this class references the Log,
    #and encapsulates the proposer, learner and acceptor agents.

    def tweet():

        #add to queue of proposals you want accepted (ordered) (in memory)

    def block():

        #add to queue of proposals you want accepted (ordered) (in memory)

    def unblock():

        #add to queue of proposals you want accepted (ordered) (in_memory)

    #once your event reaches consensus among all other processes,
    #you can then add it to your own Log.
    def tweet_for_real(new_tweet):
        Log.tweet(new_tweet)

    def block_for_real(new_block):
        Log.block(new_block)

    def unblock_for_real(new_unblock):
        Log.unblock(new_unblock)

    #these are to let you know if you are the leader.
    def isDistinguishedLearner():
        pass

    def isDistinguishedProposer():
        pass
