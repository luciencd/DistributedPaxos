#interacts with MYSQL
import mysql.connector

class Log:
    @staticmethod
    def __init__():
        #create MYSQL instance.

        #MAKE SURE TO CHECK IF DATABASE ALREADY EXISTS IF python crashed!
        self.DB_NAME = "WuuBernstein"
        self.USER = "root"
        self.TABLES = {}
        self.TABLES["Log"] = (
            "CREATE TABLE `Log` ("
            "`timestamp` INT NOT NULL,"
            "`site` INT NOT NULL,"
            "`op` VARCHAR(16) NOT NULL,"
            "`data` VARCHAR(144) NOT NULL,"
            "PRIMARY KEY (timestamp, site)"
        ") ENGINE=InnoDB")

        self.TABLES["Blocks"] = (
            "CREATE TABLE `Blocks` ("
            "`blocker` INT NOT NULL,"
            "`blocked` INT NOT NULL,"
            "PRIMARY KEY (blocker,blocked)"
        ") ENGINE=InnoDB")

        self.TABLES["T"] = (
            "CREATE TABLE `T`("
            "`site_id_row` INT NOT NULL,"
            "`site_id_column` INT NOT NULL,"
            "`timestamp` INT NOT NULL,"
            "PRIMARY KEY (site_id_row,site_id_column)"
        ") ENGINE=InnoDB")

        self.cnx = mysql.connector.connect(user=self.USER, database=self.DB_NAME)


        return True

    def initialize_T(nodes_count):
        self.start_transaction()

        query = ""
        #don't need parametrisation because i and j are not inputs.
        for i in range(nodes_count):
            for j in range(nodes_count):
                single_query = "INSERT (site_id_row,site_id_column,timestamp) VALUES ("+i+","+j+",0)"
                query += single_query

        cur = self.cnx.cursor(buffered=True)
        results = cur.execute(query)

        self.end_transaction()

    @staticmethod
    def receive(message):
        self.start_transaction()
        raise NotImplementedError

        self.end_transaction()

    @staticmethod
    def block():
        self.start_transaction()

        self._doevent(event)
        self.dict_add(event)

        self.end_transaction()

    @staticmethod
    def unblock():
        self.start_transaction()

        self._doevent(event)
        self.dict_remove(event)

        self.end_transaction()

    @staticmethod
    def tweet():
        self.start_transaction()

        self._doevent(event)

        self.end_transaction()

    @staticmethod
    def _doevent(event):
        try:
            self.log_add(event)
            self.increment_clock()
        except(e):
            #if the log isn't added, we can't increment the timestamp, or send() events in channel.py
            self.fail_transaction()
            raise EventFailedError
            ##tell client gui that tweet was failed.

    @staticmethod
    def dict_add(event):
        query = "INSERT INTO Blocks (blocker, blocked) VALUES (%s,%s)"
        cur = self.cnx.cursor(buffered=True)
        results = cur.execute(query,(event.get_blocker(),event.get_blocked()))


    @staticmethod
    def dict_remove():
        query = "DELETE FROM Blocks WHERE blocker = %s AND blocked = %s)"
        cur = self.cnx.cursor(buffered=True)
        results = cur.execute(query,(event.get_blocker(),event.get_blocked()))

    @staticmethod
    def log_add(event,cnx):
        #make sure to check for block unblock pairs!
        #Pass in current min timestamp of T i column i

        query = "INSERT INTO Log (timestamp,site,op,data) VALUES (%d, %d, %s, %s)"
        cur = self.cnx.cursor(buffered=True)
        results = cur.execute(query,(event.timestamp,event.site,event.op,event.data))
        #results.fetchone()

        raise NotImplementedError


    @staticmethod
    def increment_clock(i):
        #UPDATE site_id_column,site_id_row =
        query = "UPDATE T SET timestamp = (1+(SELECT timestamp FROM T WHERE site_id_row=%s AND site_id_column=%s)) WHERE site_id_row=%s AND site_id_column=%s"
        cur = self.cnx.cursor(buffered=True)
        results = cur.execute(query,(i,i,i,i))


    @staticmethod
    def view(site):
        #SELECT all from the Log table where op=tweet, and where site is not in blocked of where the tweet is coming from.
        query = "SELECT * FROM Log WHERE Log.op = 'tweet' AND NOT EXISTS(SELECT * FROM Blocks WHERE Log.site = Blocks.blocked AND Blocks.blocked = %s))"
        #create events
        return list_events

    @staticmethod
    def start_transaction():
        self.cnx.start_transaction()

    @staticmethod
    def end_transaction():
        self.cnx.commit()

    @staticmethod
    def fail_transaction():
        self.cnx.rollback()
