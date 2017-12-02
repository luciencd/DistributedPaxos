import pickle
import os

class Storage:
    def __init__(self, filename, N,maxindex=1):
        self.filename = filename
        self.maxindex = maxindex
        self.N = N

        self.promises_received = []
        self.acceptances_received = []

        self.current_values = []

        self.min_proposal = []
        self.accepted_proposal = []
        self.accepted_value = []

        self.initializeArrays()
        self.recoverFromFile(self.filename)
        self.commit()


    def initializeArrays(self):
        for i in range(self.maxindex+1):
            row1 = []
            row2 = []
            for j in range(self.N):
                row1.append(None)
                row2.append(None)

            self.promises_received.append(row1)
            self.acceptances_received.append(row2)

        for i in range(self.maxindex+1):
            #proposers
            self.current_values.append(None)

            #acceptors
            self.min_proposal.append(None)
            self.accepted_proposal.append(None)
            self.accepted_value.append(None)

    def createNewRounds(self):
        for i in range(len(self.promises_received),self.maxindex+1):
            row1 = []
            row2 = []
            for j in range(self.N):
                row1.append(None)
                row2.append(None)

            self.promises_received.append(row1)
            self.acceptances_received.append(row2)

        for i in range(len(self.min_proposal),self.maxindex+1):
            #proposers
            self.current_values.append(None)

            #acceptors
            self.min_proposal.append(None)
            self.accepted_proposal.append(None)
            self.accepted_value.append(None)

        self.commit()


    def setRound(self,round_):
        self.maxindex = round_
        self.commit()

    def setPromisesReceived(self,index,p,n,value):
        self.promises_received[index][p] = (n,value)
        self.commit()

    def setAcceptancesReceived(self,index,p,n):
        self.acceptances_received[index][p] = n
        self.commit()

    def setCurrentValue(self,index,value):
        self.current_values[index] = value
        self.commit()

    def setMinProposal(self,index,n):
        self.min_proposal[index] = n
        self.commit()

    def setAcceptedProposal(self,index,n):
        self.accepted_proposal[index] = n
        self.commit()

    def setAcceptedValue(self,index,value):
        self.accepted_value[index] = value
        self.commit()

    def recoverFromFile(self,filename):
        try:
            f =  open( filename, "rb" )
            try:
                 d = pickle.load(f)
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
