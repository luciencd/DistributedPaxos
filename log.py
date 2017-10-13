import sqlite3
from event import event, EventTypes
from math import sqrt
import sys

class Log:
    DATABASE_FILE = "database.db"

    tables = {
        "Log": (
            "CREATE TABLE IF NOT EXISTS `Log` ("
            "`timestamp` INT NOT NULL,"
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
        "T": (
            "CREATE TABLE IF NOT EXISTS `T`("
            "`site` INT NOT NULL,"
            "`knows_about` INT NOT NULL,"
            "`timestamp` INT NOT NULL,"
            "PRIMARY KEY (site,knows_about)"
        ")")
    }

    id = -1

    @staticmethod
    def start(nodes_count, id):
        Log.id = id
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
        #Log.cnx.close()

    @staticmethod
    def __initialize_T(cnx, nodes_count):
        all_values = ["("+str(i)+","+str(j)+",0)"
           for i in range(0,nodes_count,1)
              for j in range(0,nodes_count,1)]
        query = "INSERT OR IGNORE into T (site,knows_about,timestamp) VALUES" + (",".join(all_values))

        cur = cnx.cursor()
        results = cur.execute(query)

    @staticmethod
    def receive(message, sender):
        sys.stdout.flush()
        cnx = sqlite3.connect(Log.DATABASE_FILE)
        cur = cnx.cursor()

        timestamp_updates = [str((x,y,message.clock[x][y]))
             for x in range(0,len(message.clock),1)
               for y in range(0,len(message.clock),1)]

        cur.execute("CREATE TEMP TABLE T_REMOTE (site int, knows_about int, timestamp int)")
        cur.execute("INSERT INTO T_REMOTE (site,knows_about,timestamp) VALUES" + (",".join(timestamp_updates)))
        cur.execute("UPDATE T SET timestamp = max(timestamp,(select timestamp from T_REMOTE where T_REMOTE.site = T.site AND T_REMOTE.knows_about = T.knows_about))")
        cur.execute("UPDATE T SET timestamp = max(timestamp,(select timestamp from T_REMOTE where T_REMOTE.site = :sender AND T_REMOTE.knows_about = T.knows_about)) WHERE T.site = :me",
        {"sender": sender, "me": Log.id})
        cur.execute("DROP TABLE T_REMOTE")

        log_updates = [str((e.site, e.op, e.data, e.timestamp, e.truetime)) for e in message.events]
        cur.execute("INSERT OR REPLACE INTO Log (site, op, data, timestamp, truetime) VALUES" + (",".join(log_updates)))

        dict_new_blocks = list(filter(lambda e: e.op == EventTypes.BLOCK \
                                  and not e.related_unblock_exists(message.events),
                                  message.events))

        if len(dict_new_blocks) > 0:
            dict_block_values = [str((e.get_blocker(), e.get_blocked())) for e in dict_new_blocks]
            cur.execute("INSERT OR REPLACE INTO Blocks (blocker, blocked) VALUES" + ",".join(dict_block_values))

        dict_new_unblocks = list(filter(lambda e: e.op == EventTypes.UNBLOCK, message.events))
        unblock_statement = "DELETE FROM Blocks where blocker = :blocker and blocked = :blocked"
        for e in dict_new_unblocks:
            cur.execute(unblock_statement, {"blocker": e.get_blocker(), "blocked": e.get_blocked()})

        cnx.commit()
        cnx.close()

    @staticmethod
    def trim_old_blocks():
        raise NotImplementedError


    @staticmethod
    def block(event):
        cnx = sqlite3.connect(Log.DATABASE_FILE)
        Log._do_local_event(cnx, event)
        Log.__dict_add(cnx, event)
        cnx.commit()
        cnx.close()


    @staticmethod
    def unblock(event):
        cnx = sqlite3.connect(Log.DATABASE_FILE)
        Log._do_local_event(cnx, event)
        Log.__dict_remove(cnx, event)
        cnx.commit()
        cnx.close()


    @staticmethod
    def tweet(event):
        cnx = sqlite3.connect(Log.DATABASE_FILE)
        Log._do_local_event(cnx, event)
        cnx.commit()
        cnx.close()


    @staticmethod
    def _do_local_event(cnx, event):
            Log.__increment_clock(cnx)
            query = """INSERT INTO Log (timestamp, site, op, data, truetime) VALUES (
               (SELECT timestamp from T WHERE site=:id AND knows_about=:id),
               :id,
               :op,
               :body,
               :truetime)"""

            cur = cnx.cursor()
            cur.execute(query, {"id": event.site, "op": event.op, "body": event.data, "truetime":event.time})


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
    def __increment_clock(cnx):
        query = "UPDATE T SET timestamp = timestamp+1 WHERE site=:me AND knows_about=:me"
        cur = cnx.cursor()
        results = cur.execute(query,{"me": Log.id})

    @staticmethod
    def create_events(result_obj):
        return [ event(site,op,data,time) for time,site,op,data in result_obj ]


    @staticmethod
    def get_not_hasRecv(site):
        cnx = sqlite3.connect(Log.DATABASE_FILE)
        query = "SELECT Log.* FROM Log JOIN T on T.knows_about = Log.site AND T.site = :target WHERE Log.timestamp > T.timestamp"
        cur = cnx.cursor()
        results = cur.execute(query, { "target": site}).fetchall()
        cnx.close()
        return Log.create_events(results)

    @staticmethod
    def get_clock():
        cnx = sqlite3.connect(Log.DATABASE_FILE)
        query = "SELECT timestamp FROM T ORDER BY site,knows_about"
        cur = cnx.cursor()
        results = cur.execute(query)
        ordered_results = results.fetchall()
        cnx.close()
        num_sites = int(sqrt(len(ordered_results))) #this should always be a perfect square, because we have a 2d vector clock
        #since data returned row-first, we can split results to rebuild 2d array
        return [ ordered_results[start:start+num_sites] for start in range(0,num_sites**2, num_sites)]

    @staticmethod
    def view():
        cnx = sqlite3.connect(Log.DATABASE_FILE)
        #SELECT all from the Log table where op=tweet, and where site is not in blocked of where the tweet is coming from.
        query = "SELECT * FROM Log WHERE op = 'tweet' AND NOT EXISTS (SELECT * FROM Blocks WHERE blocker = Log.site AND blocked = :self)"
        cur = cnx.cursor()
        results = cur.execute(query, {"self": Log.id}).fetchall()
        cnx.close()
        return Log.create_events(results)
