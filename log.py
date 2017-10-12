import sqlite3
from event import event

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
    def receive(message):
        raise NotImplementedError


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
        query = "SELECT * FROM Log JOIN T on T.knows_about = Log.site AND T.site = :target WHERE Log.timestamp > T.timestamp"
        cur = Log.cnx.cursor()
        results = cur.execute(query, { "target": site})
        return create_events(results)


    @staticmethod
    def view():
        #SELECT all from the Log table where op=tweet, and where site is not in blocked of where the tweet is coming from.
        query = "SELECT * FROM Log WHERE op = 'tweet' AND NOT EXISTS (SELECT * FROM Blocks WHERE blocker = Log.site AND blocked = :self)"
        cur = Log.cnx.cursor()
        results = cur.execute(query, {"self": Log.id})
        return create_events(results)
