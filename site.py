class Site:

    def __init__(self,id_):

        self.id = id_;
        self.database = ""#create database to hold log.

        self.vector_timestamp =
        self.block_dict =
        self.log =

    def tweet(self,event):
        self._doevent(event)

    def block(self,event):
        self._doevent(event)
        self.dict_add(event)

    def unblock(self,event):
        self._doevent(event)
        self.dict_remove(event)

    def _doevent(self,event):
        self.increment_clock()
        self.matrix_timestamp.s
        #communicate with MySQL instance.
        self.log_add()

    def dict_add(self,event):
        #add to MySQL - block table
        self.block_dict.add(event)

    def dict_remove(self,event):
        #remove to MySQL - block table


    def log_add(self,event):
        #add to MySQL - log table.


    def matrix_timestamp(self):
        #get from MySQL matrix timestamp table.


    def send(self,message):

    def receive(self,message):
        #make sure that the data is translated to JSON form before we do anything in this class,
        #so we can use mock object testing before posting it to AWS.
