import pickle

class Storage:
    def __init__(self, filename, maxindex, N):
        self.filename = filename
        self.maxindex = maxindex
        self.N = N

        self.promises_received = [[]]
        self.acceptances_received = [[]]

        self.current_values = []

        self.min_proposal = []
        self.accepted_proposal = []
        self.accepted_value = []
        
        self.initializeArrays()
        #self.recoverFromFile(filename)


    def initializeArrays(self):
        for i in range(self.maxindex):
            for j in range(self.N):
                row1.append(None)
                row2.append(None)

            self.promises_received.append(row1)
            self.acceptances_received.append(row2)

        for i in range(self.index):
            #proposers
            self.current_values.append(None)

            #acceptors
            self.min_proposal.append(None)
            self.accepted_proposal.append(None)
            self.accepted_value.append(None)

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
        self.accepted_value[index][]
        self.commit()



    def recoverFromFile(self,filename):
        f = read(filename,"r")#pickle file



    def commit(self):

        try:
            #send class data of self to file.
        except CommitFailure:#won't happen.
            revert

    def view(self):
        #return all data structures in pretty way.
