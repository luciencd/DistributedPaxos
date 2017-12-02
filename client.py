from storage import Storage
from message import Prepare,Promise,AcceptRequest,Accepted,MessageReader,Message

class Agent:
    def __init__(self,id_,N,storage):
        self.id = id_
        self.N = N#number of processes. index equivalent to the position.

        self.storage = storage

    def getServerID():
        return self.id


##should make these agents store their states in stable storage.
class Proposer(Agent):
    def __init__(self,id_,N,storage):
        super().__init__(id_,N,storage)


    def getProposal(self):
        return int(str(self.storage.maxindex)+str(self.id))


    def sendAcceptRequest(self):
        msg = AcceptRequest()
        pass

    #message is a promise request.
    def recvPromise(self,message):
        #if setpromise breaks, return exception.
        self.storage.setPromise(message.i,message.n)

        if(self.isPromiseQuorum(message.i)):
            return True#or new message.
        else:
            return False

    def recvAccepted(self,message):
        #If failed to get majority or contradiction of consensus.
        #create new proposal

        self.storage.setAcceptance(message.i,message.p,message.n)

        if(self.isAcceptedQuorum(message.i)):
            #When the Proposal gets N/2 + 1 Acceptances.
            if(message.v.op == "tweet"):
                #unsure if message.i is necessary or self.i
                self.storage.tweet(message.i,message.v)
            elif(message.v.op == "block"):
                self.storage.block(message.i,message.v)
            elif(message.v.op == "unblock"):
                self.storage.unblock(message.i,message.v)

            return True
            #return sendProposal() #fail!
        else:
            self.storage.setChosenMaxProposal(self.storage.getChosenMaxProposal()+1)
            return False


    def isAcceptedQuorum(self):
        #find out if self.storage.getAcceptances(index) has a majority.
        #no editing of anything

        self.storage.acceptances_received
        return True

    def isPromiseQuorum(self):
        #find out if self.storage.getAcceptances(index) has a majority.

        #for i in range(self.storage.promises_received[self.index]):

        return True
#learner is there to find out when a value has been chosen (by the acceptors)
#and to broadcast that knowledge to all the proposers/clients,
#so that they do not have to keep sending proposals for no reason
class Learner(Agent):
    def sendChosenValue(self,message):
        pass

##should make these agents store their states in stable storage.
class Acceptor(Agent):
    def __init__(self,id_,N,storage):
        super().__init__(id_,N,storage)

    def sendPromise(self):

        return msg

    def sendAcceptance(self):
        pass


    def recvPrepare(self,message):
        print("Acceptor. recvPrepare()")
        print("received Proposal")
        print("p id:",message.v.proposal_id)
        if(message.v.proposal_id > self.storage.minProposal[message.i]):
            self.storage.setMinProposal(message.i,message.v.proposal_id)
            return Promise(self.storage.promised_id,message.v,message.index,self.id)
        else:
            return False

    def recvAcceptRequest(self,message):
        if(message.v.accepted_id >= self.storage.promised_id):
            self.promised_id


class Client:
    def __init__(self, id_, communicator, proposer, acceptor, learner, names, storage):
        self.id = id_
        self.communicator = communicator
        self.proposer = proposer
        self.acceptor = acceptor # Acceptor(self.id)
        self.learner = learner #Learner(self.id)
        #this class references the Log,
        #and encapsulates the proposer, learner and acceptor agents.
        self.event_queue = []

        self.names = names#tells you the name of the processes, so you can print it out.
        self.storage = storage
        #self.crashRecover()##will try to recover the stable storage, and will start learning the new values it missed in the meantime.



    #this has to be an anti-pattern
    def readMessage(self,message):
        print("reading msg class name:",message.__class__.__name__)
        if(message.__class__.__name__ == "Prepare"):##proposal messages are interpreted by the proposal.
            promise = self.acceptor.recvProposal(message)
            if(promise != False):
                self.communicator.send_synod(promise)
        elif(message.__class__.__name__ == "Promise"):
            self.proposer.recvPromise(message)
        elif(message.__class__.__name__ == "AcceptRequest"):
            self.acceptor.recvAcceptRequest(message)
        elif(message.__class__.__name__ == "Accepted"):
            self.proposer.recvAccepted(message)


        ##so on.

    def propose_event(self,new_event):
        n = self.proposer.getProposal()
        msg = Prepare(n,self.storage.maxindex,self.id)

        print("proposing")
        print("setting self value")
        self.storage.setCurrentValue(self.storage.maxindex,new_event)
        self.communicator.propose(msg)
        print("proposed")



    def crashRecover(self):

        #first, messages from static storage must be recreated.
        self.storage.recover()

        #contact learners to see what messages have not been received.

    #########COMMITTING

    #these are to let you know if you are the leader.
    #right now it is 0, but later, we will use more sophisticated algorithm to ensure it works
    #despite the 0 process crashing
    def isLeader(self):
        return self.id == 0

    def view(self):
        return self.storage.view()

    def erase(self):
        self.storage.erase()
