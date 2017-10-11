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
            "`op` VARCHAR NOT NULL,"
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

    def receive(message):
        self.start_transaction()
        raise NotImplementedError

        self.end_transaction()

    def block():
        self.start_transaction()

        self._doevent(event)
        self.dict_add(event)

        self.end_transaction()

    def unblock():
        self.start_transaction()

        self._doevent(event)
        self.dict_remove(event)

        self.end_transaction()

    def tweet():
        self.start_transaction()

        self._doevent(event)

        self.end_transaction()

    def _doevent(event):
        try:
            self.log_add(event)
            self.increment_clock()
        except(e):
            #if the log isn't added, we can't increment the timestamp, or send() events in channel.py
            self.fail_transaction()
            raise EventFailedError
            ##tell client gui that tweet was failed.

    def dict_add():
        query = ""
        try:
            #call query

        except(e):
            raise DictFailedError
        #raise NotImplementedError

    def dict_remove():
        raise NotImplementedError

    def log_add(event,cnx):
        #make sure to check for block unblock pairs!
        #Pass in current min timestamp of T i column i

        query = "INSERT INTO Log (timestamp,site,op,data) VALUES (%d, %d, %s, %s)"
        cur = self.cnx.cursor(buffered=True)
        results = cur.execute(query,(event.timestamp,event.site,event.op,event.data))
        #results.fetchone()

        raise NotImplementedError

    def get_clock():
        raise NotImplementedError

    def increment_clock():
        #UPDATE site_id_column,site_id_row =
        raise NotImplementedError

    def update_T_row():
        raise NotImplementedError


    def get_events_to_sent_to_j(j):
        #
        return NP

    def view():
        #SELECT all from the Log table where op=tweet, and where site is not in blocked of where the tweet is coming from.

        #create events
        return list_events

    def start_transaction():
        self.cnx.start_transaction()

    def end_transaction():
        self.cnx.commit()

    def fail_transaction():
        self.cnx.rollback()
