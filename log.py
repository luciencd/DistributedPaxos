import sqlite3
from event import event
from math import sqrt

class Log:
    tables = {
        "Log": (
            "CREATE TABLE IF NOT EXISTS `Log` ("
            "`timestamp` INT NOT NULL,"
            "`site` INT NOT NULL,"
            "`op` VARCHAR(16) NOT NULL,"
            "`data` VARCHAR(144) NOT NULL,"
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

    cnx = None
    id = -1

    @staticmethod
    def start(nodes_count, id):
        Log.id = id
        Log.cnx = sqlite3.connect("database.db")
        cur = Log.cnx.cursor()
        for _,create_statement in Log.tables.items():
            cur.execute(create_statement)

        Log.initialize_T(nodes_count)
        return True

    @staticmethod
    def stop():
        Log.cnx.commit()
        Log.cnx.close()

    @staticmethod
    def initialize_T(nodes_count):
        all_values = ["("+str(i)+","+str(j)+",0)"
           for i in range(0,nodes_count,1)
              for j in range(0,nodes_count,1)]
        query = "INSERT OR IGNORE into T (site,knows_about,timestamp) VALUES" + (",".join(all_values))

        cur = Log.cnx.cursor()
        results = cur.execute(query)
        Log.cnx.commit()

    @staticmethod
    def receive(message, sender):
        cur = Log.cnx.cursor()

        timestamp_updates = [str((x,y,message.clock[x][y]))
             for x in range(0,len(message.clock),1)
               for y in range(0,len(message.clock),1)]
        cur.execute("CREATE TEMP TABLE T_REMOTE (site int, knows_about int, timestamp int)")
        cur.execute("INSERT INTO T_REMOTE ( site, knows_about, timestamp ) VALUES " + (",".join(timestamp_updates)))
        cur.execute("UPDATE T SET timestamp = max(timestamp,(select timestamp from T_REMOTE where T_REMOTE.site = T.site AND T_REMOTE.knows_about = T.knows_about))")
        cur.execute("UPDATE T SET timestamp = max(timestamp,(select timestamp from T_REMOTE where T_remote.site = :sender AND T_REMOTE.knows_about = T.knows_about)) WHERE T.site = :me",
        {"sender": sender, "me": Log.id})
        cur.execute("DROP TABLE T_REMOTE")

        log_updates = [str((x["site"], x["op"], x["data"], x["timestamp"])) for x in message.events]
        cur.execute("INSERT OR REPLACE INTO Log (site, op, data, timestamp) VALUES " + (",".join(log_updates)))
        #TODO: dictionary
        Log.cnx.commit()

    @staticmethod
    def block(event):
        Log._do_local_event(event)
        Log.dict_add(event)
        Log.cnx.commit()


    @staticmethod
    def unblock(event):
        Log._do_local_event(event)
        Log.dict_remove(event)
        Log.cnx.commit()


    @staticmethod
    def tweet(event):
        Log._do_local_event(event)
        Log.cnx.commit()


    @staticmethod
    def _do_local_event(event):
            Log.increment_clock()
            query = """INSERT INTO Log (timestamp, site, op, data) VALUES (
               (SELECT timestamp from T WHERE site=:id AND knows_about=:id),
               :id,
               :op,
               :body)"""

            cur = Log.cnx.cursor()
            cur.execute(query, {"id": event.site, "op": event.op, "body": event.data})


    @staticmethod
    def dict_add(event):
        query = "INSERT OR REPLACE INTO Blocks (blocker, blocked) VALUES (:blocker,:blocked)"
        cur = Log.cnx.cursor()
        results = cur.execute(query,{"blocker": event.get_blocker(), "blocked": event.get_blocked()})


    @staticmethod
    def dict_remove(event):
        query = "DELETE FROM Blocks WHERE blocker = :blocker AND blocked = :blocked"
        cur = Log.cnx.cursor()
        results = cur.execute(query,{"blocker": event.get_blocker(), "blocked": event.get_blocked()})


    @staticmethod
    def increment_clock():
        query = "UPDATE T SET timestamp = timestamp+1 WHERE site=:me AND knows_about=:me"
        cur = Log.cnx.cursor()
        results = cur.execute(query,{"me": Log.id})

    @staticmethod
    def create_events(result_obj):
        return [ event(site,op,data,time) for time,site,op,data in result_obj.fetchall()]


    @staticmethod
    def get_not_hasRecv(site):
        query = "SELECT Log.* FROM Log JOIN T on T.knows_about = Log.site AND T.site = :target WHERE Log.timestamp > T.timestamp"
        cur = Log.cnx.cursor()
        results = cur.execute(query, { "target": site})
        return Log.create_events(results)

    @staticmethod
    def get_clock():
        query = "SELECT timestamp FROM T ORDER BY site,knows_about"
        cur = Log.cnx.cursor()
        results = cur.execute(query)
        ordered_results = results.fetchall()
        num_sites = int(sqrt(len(ordered_results))) #this should always be a perfect square, because we have a 2d vector clock
        #since data returned row-first, we can split results to rebuild 2d array
        return [ ordered_results[start:start+num_sites] for start in range(0,num_sites**2, num_sites)]

    @staticmethod
    def view():
        #SELECT all from the Log table where op=tweet, and where site is not in blocked of where the tweet is coming from.
        query = "SELECT * FROM Log WHERE op = 'tweet' AND NOT EXISTS (SELECT * FROM Blocks WHERE blocker = Log.site AND blocked = :self)"
        cur = Log.cnx.cursor()
        results = cur.execute(query, {"self": Log.id})
        return Log.create_events(results)
