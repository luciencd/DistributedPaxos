import sqlite3
from event import event, EventTypes
from math import sqrt
import sys

#this log class shouldn't change, but it will be called from the client
class Log:
    DATABASE_FILE = "database.db"

    tables = {
        "Log": (
            "CREATE TABLE IF NOT EXISTS `Log` ("
            "`index` INT NOT NULL,"
            "`site` INT NOT NULL,"
            "`op` VARCHAR(16) NOT NULL,"
            "`data` VARCHAR(144) NOT NULL,"
            "`truetime` DATETIME NOT NULL,"
            "PRIMARY KEY (timestamp, site)"
        ")"),
        "Blocks": (
            "CREATE TABLE IF NOT EXISTS `Blocks` ("
            "`blocker` INT NOT NULL,"
            "`blocked` INT NOT NULL,"
            "PRIMARY KEY (blocker,blocked)"
        ")"),
        "Variables": (
            "CREATE TABLE IF NOT EXISTS `T`("
            "`index` INT NOT NULL,"
            "`proposed_value` INT NOT NULL,"##will probably need to be the same variables as in the message. #or will they? as soon as accepted value is confirmed, we can just add it to the Log so why bother?
            "`accepted_value` INT NOT NULL,"
            "`proposed_id` INT NOT NULL,"
            "`accepted_id` INT NOT NULL,"
            "PRIMARY KEY (index)"
        ")")
    }

    id = -1

    @staticmethod
    def start(nodes_count, id, names):
        Log.id = id
        Log.names = names
        cnx = sqlite3.connect(Log.DATABASE_FILE,detect_types=sqlite3.PARSE_DECLTYPES)
        cur = cnx.cursor()
        for _,create_statement in Log.tables.items():
            cur.execute(create_statement)

        Log.__initialize_T(cnx, nodes_count)
        cnx.commit()
        cnx.close()
        return True

    @staticmethod
    def stop():
        pass

    #message should be an accept message, which pushed the total messages to a quorum.
    @staticmethod
    def receive(message, sender):
        sys.stdout.flush()
        cnx = sqlite3.connect(Log.DATABASE_FILE)
        cur = cnx.cursor()

        e = message.v

        log_update = str((message.i, e.site, e.op, e.data, e.timestamp, e.truetime))
        cur.execute("INSERT OR REPLACE INTO Log (index, site, op, data, timestamp, truetime) VALUES" + (",".join(log_update)))

        #adding/removing from block table.
        if(e.op == BLOCK):
            dict_block_value =str((e.get_blocker(), e.get_blocked()))
            cur.execute("INSERT OR REPLACE INTO Blocks (blocker, blocked) VALUES" + ",".join(dict_block_values))
        elif(e.op == UNBLOCK):
            dict_unblock_value =str((e.get_blocker(), e.get_blocked()))
            cur.execute("INSERT OR REPLACE INTO Blocks (blocker, blocked) VALUES" + ",".join(dict_unblock_values))

        cnx.commit()
        cnx.close()

    @staticmethod
    def block(event,index):
        cnx = sqlite3.connect(Log.DATABASE_FILE)
        Log._do_local_event(cnx, event,index)
        Log.__dict_add(cnx, event)
        cnx.commit()
        cnx.close()


    @staticmethod
    def unblock(event,index):
        cnx = sqlite3.connect(Log.DATABASE_FILE)
        Log._do_local_event(cnx, event,index)
        Log.__dict_remove(cnx, event)
        cnx.commit()
        cnx.close()


    @staticmethod
    def tweet(event,index):
        cnx = sqlite3.connect(Log.DATABASE_FILE)
        Log._do_local_event(cnx, event,index)
        cnx.commit()
        cnx.close()


    @staticmethod
    def _do_local_event(cnx, event):
            Log.__increment_clock(cnx)
            query = """INSERT INTO Log (index,timestamp, site, op, data, truetime) VALUES (
               (SELECT timestamp from T WHERE site=:id AND knows_about=:id),
               :index,
               :id,
               :op,
               :body,
               :truetime)"""

            cur = cnx.cursor()
            cur.execute(query, {"id": event.site, "op": event.op, "body": event.data, "truetime":event.truetime})


    @staticmethod
    def __dict_add(cnx, event):
        query = "INSERT OR REPLACE INTO Blocks (blocker, blocked) VALUES (:blocker,:blocked)"
        cur = cnx.cursor()
        results = cur.execute(query,{"blocker": event.get_blocker(), "blocked": event.get_blocked()})


    @staticmethod
    def __dict_remove(cnx, event):
        query = "DELETE FROM Blocks WHERE blocker = :blocker AND blocked = :blocked"
        cur = cnx.cursor()
        results = cur.execute(query,{"blocker": event.get_blocker(), "blocked": event.get_blocked()})


    @staticmethod
    def __trim_log(cnx):
        query = "DELETE FROM Log WHERE op in ('block', 'unblock') and timestamp <= (select MIN(timestamp) from T where knows_about = Log.site)"
        cur = cnx.cursor()
        cur.execute(query)

    @staticmethod
    def create_events(results_obj):
        return [ event(site,op,data,truetime,Log.names[site],time) for time,site,op,data,truetime in results_obj ]


    @staticmethod
    def get_blocks():
        cnx = sqlite3.connect(Log.DATABASE_FILE)
        query = "SELECT blocked FROM Blocks where blocker = :me"
        cur = cnx.cursor()
        results = cur.execute(query, {"me": Log.id}).fetchall()
        cnx.close()
        return [result[0] for result in results] #sqlite stupid enough to return a tuple of 1 element for single column queries, so we unpack


    @staticmethod
    def view():
        cnx = sqlite3.connect(Log.DATABASE_FILE)
        #SELECT all from the Log table where op=tweet, and where site is not in blocked of where the tweet is coming from.
        query = "SELECT * FROM Log WHERE op = 'tweet' AND NOT EXISTS (SELECT * FROM Blocks WHERE blocker = Log.site AND blocked = :self) ORDER BY truetime DESC"
        cur = cnx.cursor()
        results = cur.execute(query, {"self": Log.id}).fetchall()
        cnx.close()
        return Log.create_events(results)


    @staticmethod
    def commitPAXOSLogEntry(message):
        #cnx = sqlite3.connect(Log.DATABASE_FILE)
        #query = "INSERT INTO Log VALUES (:index,:site,:op,:data,:truetime) AS (index,site,op,data,truetime)"
