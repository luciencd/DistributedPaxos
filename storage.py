import pickle
import os

class Storage:
    def __init__(self, filename, N,maxindex=0,initStorage = 100):
        self.filename = filename
        self.maxindex = maxindex
        self.N = N
        self.initStorage = initStorage

        self.promises_received = []
        self.acceptances_received = []

        self.current_values = []

        self.min_proposal = []
        self.accepted_proposal = []
        self.accepted_value = []

        self.event_list = []

        self.initializeArrays()
        self.recoverFromFile(self.filename)
        self.commit()


    def initializeArrays(self):
        for i in range(0,self.initStorage):#self.maxindex):
            row1 = []
            row2 = []
            for j in range(self.N):
                row1.append(None)
                row2.append(None)

            self.promises_received.append(row1)
            self.acceptances_received.append(row2)

        for i in range(0,self.initStorage):#self.maxindex):
            #proposers
            self.current_values.append(None)

            #acceptors
            self.min_proposal.append(-1)
            self.accepted_proposal.append(-1)
            self.accepted_value.append(None)

            self.event_list.append(None)

    def createNewRounds(self):
        for i in range(len(self.promises_received),self.maxindex):
            row1 = []
            row2 = []
            for j in range(self.N):
                row1.append(None)
                row2.append(None)

            self.promises_received.append(row1)
            self.acceptances_received.append(row2)

        for i in range(len(self.min_proposal),self.maxindex):
            #proposers
            self.current_values.append(None)

            #acceptors
            self.min_proposal.append(None)
            self.accepted_proposal.append(None)
            self.accepted_value.append(None)

            self.event_list.append(None)

        self.commit()


    def setRound(self,round_):
        self.maxindex = round_
        self.commit()

    def maxIndexise(self,index):
        if(index > self.maxindex):
            createNewRounds()
        self.commit()

    def setPromisesReceived(self,index,p,n,value):
        #self.maxIndexise(index)
        self.promises_received[index][p] = (n,value)
        self.commit()

    def setAcceptancesReceived(self,index,p,n):
        #self.maxIndexise(index)
        self.acceptances_received[index][p] = n
        self.commit()

    def setCurrentValue(self,index,value):
        #self.maxIndexise(index)
        print("sCV: value",value,"index:",index)
        self.current_values[index] = value
        self.commit()

    def setMinProposal(self,index,n):
        #self.maxIndexise(index)
        self.min_proposal[index] = n
        self.commit()

    def setAcceptedProposal(self,index,n):
        #self.maxIndexise(index)
        self.accepted_proposal[index] = n
        self.commit()

    def setAcceptedValue(self,index,value):
        #self.maxIndexise(index)
        self.accepted_value[index] = value
        self.commit()

    def commitEvent(self,index,event):
        #self.maxIndexise(index)
        self.event_list[index] = event
        self.commit()

    def recoverFromFile(self,filename):
        try:
            f =  open( filename, "rb" )
            try:
                 d = pickle.load(f)
                 print(d)
                 self.__dict__ = d
            except EOFError:
                pass

            f.close()
        except FileNotFoundError:
            pass

    def commit(self):
        try:
            f = open(self.filename, "wb" )
            pickle.dump( self.__dict__, f)
            f.close()
        except FileNotFoundError:
            pass

    def view(self):
        return self.__dict__
        #return all data structures in pretty way.

    def erase(self):
        try:
            os.remove(self.filename)
        except FileNotFoundError:
            pass
