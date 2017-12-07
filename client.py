from storage import Storage
from message import Prepare,Promise,AcceptRequest,Accepted,MessageReader,Message,Commit
import json

class Agent:
    def __init__(self,id_,N,storage,names):
        self.id = id_
        self.N = N#number of processes. index equivalent to the position.

        self.storage = storage
        self.names = names

    def getServerID():
        return self.id


##should make these agents store their states in stable storage.
class Proposer(Agent):
    def __init__(self,id_,N,storage,names):
        super().__init__(id_,N,storage,names)
        self.leader = False


    def getProposal(self,index):##should work.
        if(self.isLeader(index)):
            return -1
        else:
            return self.id
        #return int(str(self.storage.maxindex)+str(self.id))

    def isLeader(self,index):
        if(self.storage.event_list[index-1] == None):
            return False

        if(self.storage.event_list[index-1].site == self.id):
            return True
        else:
            return False

    #make sure the process whose chosen proposal matches his initial proposal becomes leader, and the converse for the others.
    def setLeader(self,leaderize=False):
        self.leader = leaderize


    def highest_value_of_proposals(self,index):
        counts = self.getTotalCounts(index)
        #print("COUNTS",counts)
        max_proposal = -1
        max_value = None
        for key, value in counts.items():
            if(key != None):
                if(key > max_proposal):
                    max_value = value[2]

        return max_value
    #message is a promise request.
    def recvPromise(self,message):
        #if setpromise breaks, return exception.
        #(self,index,p,n,value):
        print("RECV PROMISE from",self.names[message.p])
        value = message.v

        if(value == None):
            value = self.storage.current_values[message.i]
            #print("value at index",message.i,value)
        else:
            value = message.v

        self.storage.setPromisesReceived(message.i,message.p,message.n,value)

        if(self.isPromiseQuorum(message.i)>=0):
            high_value = self.highest_value_of_proposals(message.i)

            if(high_value != None):#what happens when you got any promise with a value.
                self.storage.setCurrentValue(message.i,high_value)
            #else, you just use your own value.

            #find the highest proposal number and create an acceptedRequest with it
            acc = AcceptRequest(self.getProposal(message.i),self.storage.current_values[message.i],message.i,self.id)#or new message.
            #print(acc)
            return acc
        else:
            return False

    def recvAccepted(self,message):
        #If failed to get majority or contradiction of consensus.
        #create new proposal
        print("RECV ACCEPTED from",self.names[message.p])

        self.storage.setAcceptancesReceived(message.i,message.p,message.n)

        if(self.isAcceptedQuorum(message.i)):
            print("MESSAGE COMMITTING:",message.v,type(message.v))
            #print("MESSAGE dict",message.v.op)
            #When the Proposal gets N/2 + 1 Acceptances.

                #unsure if message.i is necessary or self.i
            self.storage.commitEvent(message.i,message.v)

            return True
            #return sendProposal() #fail!
        else:
            #self.storage.setChosenMaxProposal(self.storage.getChosenMaxProposal()+1)
            return False

    def numProcesses(self):
        return len(self.storage.promises_received[0])

    def isAcceptedQuorum(self,index):
        #find out if self.storage.getAcceptances(index) has a majority.
        #no editing of anything
        maj = 0
        for i in range(len(self.storage.acceptances_received[index])):
            if(self.storage.acceptances_received[index][i] != None):
                maj += 1
        return maj == (len(self.storage.acceptances_received[index])//2 + 1)

    def getTotalCounts(self,index):
        #find out if self.storage.getAcceptances(index) has a majority.
        #print(self.storage.promises_received[index])
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
                    counts[None] = (counts[None][0]+1,None,None)
                else:
                    counts[None] = (1,None,None)
        return counts

    def isPromiseQuorum(self,index):
        counts = self.getTotalCounts(index)
        for key, value in counts.items():
            if(value[0] == self.numProcesses()//2 + 1):
                return value[1]
            else:
                pass
        return -1
#learner is there to find out when a value has been chosen (by the acceptors)
#and to broadcast that knowledge to all the proposers/clients,
#so that they do not have to keep sending proposals for no reason
class Learner(Agent):
    def sendChosenValue(self,message):
        pass

##should make these agents store their states in stable storage.
class Acceptor(Agent):
    def __init__(self,id_,N,storage,names):
        super().__init__(id_,N,storage,names)

    def recvPrepare(self,message):
        print("RECV PREPARE from",self.names[message.p])
        #figure out what leader should send. if its 0, that's not gonna work right.
        if(message.n > self.storage.min_proposal[message.i]):#along with leader election and no 0 process but the leader.
            self.storage.setMinProposal(message.i,message.n)

            return Promise(self.storage.min_proposal[message.i],self.storage.accepted_value[message.i],message.i,self.id)
        else:
            return False

    def recvAcceptRequest(self,message):
        print("RECV ACCEPT REQUEST from",self.names[message.p])
        if(message.n >= self.storage.min_proposal[message.i]):
            self.storage.setMinProposal(message.i,message.n)
            self.storage.setAcceptedProposal(message.i,self.storage.min_proposal[message.i])
            self.storage.setAcceptedValue(message.i,message.v)
            return Accepted(self.storage.min_proposal[message.i],message.v,message.i,self.id)

        else:
            #don't think I need to do anything, although I could send a Nack.

            return False


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
        self.storage = storage##will try to recover the stable storage, but not our responsibility
        self.block_dictionary = {}
        self.crashRecover()## will start learning the new values it missed in the meantime.




    #this has to be an anti-pattern
    def readMessage(self,message):
        #print("reading msg class name:",message.__class__.__name__)
        if(message.__class__.__name__ == "Prepare"):##proposal messages are interpreted by the proposal.
            promise = self.acceptor.recvPrepare(message)
            if(promise == False):
                if(self.storage.event_list[message.i] != None):
                    commit = Commit(self.storage.event_list[message.i],message.i,self.id)
                    self.communicator.send_synod(commit,message.p)
            else:
                self.communicator.send_synod(promise,message.p)

        elif(message.__class__.__name__ == "Promise"):

            accept_request = self.proposer.recvPromise(message)
            if(accept_request != False):#when you have a quorum

                #obviously send accept request to yourself when you do this.
                accept = self.acceptor.recvAcceptRequest(accept_request)
                self.proposer.recvAccepted(accept)
                ##hope this always works.
                #print("Current Accept Requests. should have [none, 1]",self.storage.acceptances_received)
                #print("gonna send out accept request! for message value")
                #print(accept_request)
                #send accepts to all other processes but yourself.
                self.communicator.broadcast_synod(accept_request)
        elif(message.__class__.__name__ == "AcceptRequest"):
            accept = self.acceptor.recvAcceptRequest(message)
            if(accept == False):#as in, you failed to send the right accept(could be you recovering.)
                #didn't accept value

                #if the value has been chosen though, send it back!! #this is some pseudo learner stuff here.
                if(self.storage.event_list[message.i] != None):
                    commit = Commit(self.storage.event_list[message.i],message.i,self.id)
                    self.communicator.send_synod(commit,message.p)

            else:#send Accepts back to the proposers.
                self.communicator.send_synod(accept,message.p)

        elif(message.__class__.__name__ == "Accepted"):
            commit_bool = self.proposer.recvAccepted(message)
            if(commit_bool):#if you have a perfect accept quorum (1ce for all indices)
                self.commit(message)
                #only after you yourself are committing, not getting a commit from somewhere else.
                self.storage.setRound(self.storage.maxindex+1)

                #send commit message to others.
                commit_message = Commit(message.v,message.i,message.p)
                self.communicator.broadcast_synod(commit_message)


        elif(message.__class__.__name__ == "Commit"):
            commit_message = self.recvCommit(message)#if you are getting a commit message from someone, and you haven't already committed.
            #return false, if you have already committed.

            if(commit_message):#if you are told my someone else to commit.(might get more than one message here.)
                self.commit(message)
                self.storage.setRound(message.i+1)#don't want to try committing something when its gonna fail.



        ##so on.
    def twitterEvent(self,new_event):#make sure maxindex is in storage and what that means.
        if(self.storage.current_values[self.storage.maxindex] == None):
            if(self.proposer.isLeader(self.storage.maxindex)):
                acceptal = self.accept_event(new_event,self.storage.maxindex)
            else:
                proposal = self.propose_event(new_event,self.storage.maxindex)
            #print("PROPOSAL: ",proposal)
        else:
            self.storage.setRound(self.storage.maxindex+1)
            return False

    def accept_event(self,new_event,index):
        print("ACCEPTED EVENT AS LEADER")

        #self.storage.setCurrentValue(index,new_event)
        acc = AcceptRequest(self.proposer.getProposal(index),new_event,index,self.id)
        ##self accept request
        accept = self.acceptor.recvAcceptRequest(acc)
        self.proposer.recvAccepted(accept)

        #send accept request to all others.
        self.communicator.acceptRequest(acc)

    #when you tweet for the first tme
    def propose_event(self,new_event,index):
        print("PROPOSE EVENT")
        n = self.proposer.getProposal(index)
        msg = Prepare(n,index,self.id)

        #print("setting self value")
        #make sure to initially set the promise values and all that.
        print("NEW EVENT:",new_event)
        self.storage.setCurrentValue(index,new_event)
        self.storage.setPromisesReceived(index,self.id,self.proposer.getProposal(index),new_event)
        #figure out if this can be better abstracted though similar function to when you send it to a different
        #client's acceptor.

        #print("proposing message sending")
        self.communicator.propose(msg)
        #print("proposed sent")

    #accept commit message.
    def recvCommit(self,message):
        print("RECEIVED COMMIT from",message.p)
        return self.storage.event_list[message.i] == None

    def commit(self,message):
        print("COMMIT")
        self.storage.commitEvent(message.i,message.v)

        #blocks and
        print("block?",message.v.op,(message.v.get_blocker(),message.v.get_blocked()))

        if(message.v.op == "block"):
            self.block_dictionary[(message.v.get_blocker(),message.v.get_blocked())] = True
        elif(message.v.op == "unblock"):
            self.block_dictionary[(message.v.get_blocker(),message.v.get_blocked())] = False


    def crashRecover(self):

        #first, messages from static storage must be recreated.
        #self.storage.recover()
        print("RECREATING DICTIONARY OF BLOCKS FROM DISK LOG.")
        for i in range(len(self.storage.event_list)):
            e = self.storage.event_list[i]
            if(e != None):

                if(e.op == "block"):
                    self.block_dictionary[(e.get_blocker(),e.get_blocked())] = True
                elif(e.op == "unblock"):
                    self.block_dictionary[(e.get_blocker(),e.get_blocked())] = False

        #contact learners to see what messages have not been received.
        print("FINISHED DICT BUILDING AND RECOVERY.")
    #########COMMITTING

    #these are to let you know if you are the leader.
    #right now it is 0, but later, we will use more sophisticated algorithm to ensure it works
    #despite the 0 process crashing

    def isBlocked(self,other_site):
        try:
            return self.block_dictionary[(other_site,self.id)]
        except KeyError:
            return False

    #printing out all events properly.
    def view(self):
        tweets_list_string = []

        for i in range(self.storage.maxindex):#self.storage.event_list:
            event = self.storage.event_list[i]
            if(event == None):
                tweets_list_string.append("EMPTY LOG ENTRY")
            elif(event.op == "tweet"):
                if(not self.isBlocked(event.site)):
                    tweets_list_string.append(event.__str__())

        return "\n".join(tweets_list_string)

    def blocks(self):
        print("printing block dictionary:")
        lines = []
        for key in self.block_dictionary:
            if(self.block_dictionary[key] == True):
                lines.append(self.names[key[0]]+" is blocking "+self.names[key[1]])
        return "\n".join(lines)

    def view_log(self):
        log_view = []

        for i in range(self.storage.maxindex):#self.storage.event_list:
            event = self.storage.event_list[i]
            if(event == None):
                log_view.append("EMPTY LOG ENTRY")
            else:
                data = ""
                if(event.op == "block"):
                    data = self.names[int(event.data.split(",")[0])]+" blocks "+self.names[int(event.data.split(",")[1])]
                elif(event.op == "unblock"):
                    data = self.names[int(event.data.split(",")[0])]+" unblocks "+self.names[int(event.data.split(",")[1])]
                else:
                    data = event.data

                log_view.append(event.prefix()+" "+data)

        return "\n".join(log_view)

    #showing the internal stable state.
    def data(self):
        #make prettier.
        return self.storage.view()

    def nicedata(self):
        return json.dumps(self.storage.view(), indent=4, sort_keys=True)

    #incase we want to reset everything on all nodes to revert without messing with indiviudal files.
    def erase(self):
        self.storage.erase()
