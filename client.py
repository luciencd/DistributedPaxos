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
        self.leader = False


    def getProposal(self):##should work.
        if(self.isLeader()):
            return 0
        else:
            return self.id+1
        #return int(str(self.storage.maxindex)+str(self.id))

    def isLeader(self):
        return self.leader

    #make sure the process whose chosen proposal matches his initial proposal becomes leader, and the converse for the others.
    def setLeader(self,leaderize=False):
        self.leader = leaderize

    def sendAcceptRequest(self):
        msg = AcceptRequest()
        pass

    #message is a promise request.
    def recvPromise(self,message):
        #if setpromise breaks, return exception.
        #(self,index,p,n,value):
        value = message.v
        print("incoming value:",value)
        print(message.i)

        if(value == None):
            value = self.storage.current_values[message.i]
        print("storing Value:",value.data)
        self.storage.setPromisesReceived(message.i,message.p,message.n,value)

        if(self.isPromiseQuorum(message.i)>=0):
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

    def numProcesses(self):
        return len(self.storage.current_values[0])

    def isAcceptedQuorum(self):
        #find out if self.storage.getAcceptances(index) has a majority.
        #no editing of anything

        self.storage.acceptances_received
        return True

    def isPromiseQuorum(self,index):
        #find out if self.storage.getAcceptances(index) has a majority.
        print(self.storage.promises_received[index])
        counts = dict()

        for i in range(len(self.storage.promises_received[index])):
            if(self.storage.promises_received[index][i] != None):
                promise_number = self.storage.promises_received[index][i][0]
                promise_value = self.storage.promises_received[index][i][1]

                if(promise_number in counts):
                    counts[promise_number] = (counts[promise_number][0]+1,promise_number,promise_value)
                else:
                    counts[promise_number] = (1,promise_number,promise_value)
            else:
                if(None in counts):
                    counts[None] = (counts[promise_number][0]+1,None,None)
                else:
                    counts[None] = (1,None,None)

        for key, value in counts.items():
            if(value[0] > self.numProcesses()//2):
                print("QUROUM reached! accept proposal",value[1],"tweet",value[2])
                return value[1]
            else:
                print("not a quorum for proposal",value[1])


        return -1
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
        print("proposal id:",message.n)
        #figure out what leader should send. if its 0, that's not gonna work right.
        if(message.n > self.storage.min_proposal[message.i]):#along with leader election and no 0 process but the leader.
            self.storage.setMinProposal(message.i,message.n)

        return Promise(self.storage.min_proposal[message.i],self.storage.accepted_value[message.i],message.i,message.p)


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

        #and encapsulates the proposer, learner and acceptor agents.
        self.event_queue = []

        self.names = names#tells you the name of the processes, so you can print it out.
        self.storage = storage
        #self.crashRecover()##will try to recover the stable storage, and will start learning the new values it missed in the meantime.



    #this has to be an anti-pattern
    def readMessage(self,message):
        print("reading msg class name:",message.__class__.__name__)
        if(message.__class__.__name__ == "Prepare"):##proposal messages are interpreted by the proposal.
            promise = self.acceptor.recvPrepare(message)
            if(promise != False):
                self.communicator.send_synod(promise)
        elif(message.__class__.__name__ == "Promise"):
            accept_request = self.proposer.recvPromise(message)
            if(accept_request != False):
                print("gonna send out accept request! for message value")
                #self.communicator.broadcast_synod(accept_request)
        elif(message.__class__.__name__ == "AcceptRequest"):
            self.acceptor.recvAcceptRequest(message)
        elif(message.__class__.__name__ == "Accepted"):
            self.proposer.recvAccepted(message)


        ##so on.
    def twitterEvent(self,new_event):
        self.propose_event(new_event,self.maxindex)

    #when you tweet for the first tme
    def propose_event(self,index,new_event):
        n = self.proposer.getProposal()
        msg = Prepare(n,self.proposal.getProposal(index),self.id)

        print("setting self value")
        #make sure to initially set the promise values and all that.
        self.storage.setCurrentValue(index,self.proposal.getProposal(index),new_event)
        self.storage.setPromisesReceived(index,self.id,self.proposal.getProposal(index),new_event)

        print("proposing message sending")
        self.communicator.propose(msg)
        print("proposed sent")



    def crashRecover(self):

        #first, messages from static storage must be recreated.
        self.storage.recover()

        #contact learners to see what messages have not been received.

    #########COMMITTING

    #these are to let you know if you are the leader.
    #right now it is 0, but later, we will use more sophisticated algorithm to ensure it works
    #despite the 0 process crashing

    #printing out all events properly.
    def view(self):
        return self.storage.view()

    #showing the internal stable state.
    def datadump(self):
        data = self.storage.view()
        #make prettier.
        return data

    #incase we want to reset everything on all nodes to revert without messing with indiviudal files.
    def erase(self):
        self.storage.erase()
