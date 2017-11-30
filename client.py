class Agent:
    def __init__(self,id_,N):
        self.id = id_
        self.N = N#number of processes. index equivalent to the position.
        self.promises_received = []
        self.acceptances_received = []

        self.initializeArrays()

    def initializeArrays(self):
        for i in range(self.N):
            for j in range(self.N):
                row1.append(None)
                row2.append(None)

            self.promises_received.append(row1)
            self.acceptances_received.append(row2)


    def getServerID():
        return self.id

##should make these agents store their states in stable storage.
class Proposer(Agent):
    def __init__(self,id_,N):
        super().__init__(self,id_,N)

        self.highest_accepted_id = 0

        ##list of promises received, which is not stored in stable storage.

        #get chosen value



    def getMaxRound(self):
        #Log.getMaxRound()
        pass

    def setMaxRound(self):#reference the Log to maintain safe storage on change.
        #Log.setMaxRound()
        pass


    def sendProposal(self):
        msg = Prepare(int(str(self.getMaxRound())+str(self.id_)),self.id_)
        return msg

    def sendAcceptRequest(self):
        msg = AcceptRequest()
        pass

    #message is a promise request.
    def recvPromise(self,message):
        if(message)
        pass

    def recvAccepted(self,message):
        #If failed to get majority or contradiction of consensus.
        #create new proposal

        if(message != self.value):
            self.setMaxRound(self.getMaxRound()+1)
            #return sendProposal() #fail!
        else:

            if()
            #When the Proposal gets N/2 + 1 Acceptances.
            if(message.v.op == "tweet"):
                tweet(message.v)
            elif(message.v.op == "block"):
                block(message.v)
            elif(message.v.op == "unblock"):
                unblock(message.v)


#learner is there to find out when a value has been chosen (by the acceptors)
#and to broadcast that knowledge to all the proposers/clients,
#so that they do not have to keep sending proposals for no reason
class Learner(Agent):
    def sendChosenValue(self,message):
        pass

##should make these agents store their states in stable storage.
class Acceptor(Agent):
    def __init__(self,id_,N):
        super().__init__(self,id_,N)
        self.promised_id = 0


    def sendPromise(self):

        return msg

    def sendAcceptance(self):
        pass


    def recvProposal(self,message):

        if(message.v.proposal_id >= self.promised_id):
            self.promised_id = message.v.proposal_id
            return Promise(self.promised_id,message.v,message.index,self.id)
        #else:
            #return NACK, to tell the proposer, its proposal failed.


    def recvAcceptRequest(self,message):
        if(message.v.accepted_id >= self.promised_id):
            self.promised_id


class Client:
    def __init__(self, proposer, acceptor, learner):
        self.id = id_
        self.proposer = proposer
        self.acceptor = acceptor # Acceptor(self.id)
        self.learner = learner #Learner(self.id)
        #this class references the Log,
        #and encapsulates the proposer, learner and acceptor agents.
        self.event_queue = []



    #this has to be an anti-pattern
    def readMessage(self,message):

        if(type(message) is Proposal):##proposal messages are interpreted by the proposal.
            self.acceptor.recvProposal(message)
        elif(type(message) is Promise):
            self.proposer.recvPromise(message)
        elif(type(message) is AcceptRequest):
            self.acceptor.recvAcceptRequest(message)
        elif(type(message) is Accepted):
            self.proposer.recvAccepted(message)

        ##so on.

    def tweet(self,new_tweet):
        self.event_queue.append(new_tweet)
        #add to queue of proposals you want accepted (ordered) (in memory)

    def block(self,new_block):
        self.event_queue.append(new_block)
        #add to queue of proposals you want accepted (ordered) (in memory)

    def unblock(self,new_unblock):
        self.event_queue.append(new_unblock)
        #add to queue of proposals you want accepted (ordered) (in_memory)


    ########COMMITTING
    #once your event reaches consensus among all other processes,
    # i.e. the proposer learns a majority, or the learner tells you they learned the majority, then
    # commit to Log!
    def event_at_index_commit(self,event):
        if(event.name)
        Log.tweet(new_tweet)
        #communicator.tweet()#just sends all messages that have not been recieved by the particular other clients.
        #could be single tweet, single block, single unblock, as long as all the events
        #in there have been the result of consensus. Which they are, as any event in the log has been reached by consensus!!!

    def block_for_real(self,new_block):
        Log.block(new_block)
        #communicator.tweet()#just sends all messages that have not been recieved by the particular other clients.
        #could be single tweet, single block, single unblock

    def unblock_for_real(self,new_unblock):
        Log.unblock(new_unblock)
        #communicator.tweet()#just sends all messages that have not been recieved by the particular other clients.
        #could be single tweet, single block, single unblock

    #########COMMITTING

    #these are to let you know if you are the leader.
    #right now it is 0, but later, we will use more sophisticated algorithm to ensure it works
    #despite the 0 process crashing
    def isLeader(self):
        return self.id == 0
