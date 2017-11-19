class Proposer(Agent):
    def propose():
        pass

class Learner(Agent):
    def learn():
        pass

class Accepter(Agent):
    def accept():
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

    self.event_queue = []

    def tweet(new_tweet):
        self.event_queue.append(new_tweet)
        #add to queue of proposals you want accepted (ordered) (in memory)

    def block(new_block):
        self.event_queue.append(new_block)
        #add to queue of proposals you want accepted (ordered) (in memory)

    def unblock(new_unblock):
        self.event_queue.append(new_unblock)
        #add to queue of proposals you want accepted (ordered) (in_memory)

    #once your event reaches consensus among all other processes,
    #you can then add it to your own Log.
    def tweet_for_real(new_tweet):
        Log.tweet(new_tweet)
        communicator.tweet()#just sends all messages that have not been recieved by the particular other clients.
        #could be single tweet, single block, single unblock, as long as all the events
        #in there have been the result of consensus. Which they are, as any event in the log has been reached by consensus!!!

    def block_for_real(new_block):
        Log.block(new_block)
        communicator.tweet()#just sends all messages that have not been recieved by the particular other clients.
        #could be single tweet, single block, single unblock

    def unblock_for_real(new_unblock):
        Log.unblock(new_unblock)
        communicator.tweet()#just sends all messages that have not been recieved by the particular other clients.
        #could be single tweet, single block, single unblock

    #these are to let you know if you are the leader.
    def isDistinguishedLearner():
        pass

    def isDistinguishedProposer():
        pass
