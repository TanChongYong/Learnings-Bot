import sqlite3


class DBHelper:
    def __init__(self, dbname="todo.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, date text, duration text,owner text, ownerName text)" 
        statusStmt = "CREATE TABLE IF NOT EXISTS status (status text, checkinTime DATETIME, owner text)"
        itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)" 
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)" 
        statusidx = "CREATE INDEX IF NOT EXISTS ownIndex ON status (owner ASC)" 
        self.conn.execute(tblstmt)
        self.conn.execute(itemidx)
        self.conn.execute(ownidx) 
        self.conn.execute(statusStmt) 
        self.conn.execute(statusidx)
        self.conn.commit()

    def add_item(self, item_text,today, duration,owner,ownerName): 
        stmt = "INSERT INTO items (description,date, duration,owner,ownerName) VALUES (?, ?, ?, ?, ?)"
        args = (item_text,today, duration,owner,ownerName)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text, owner):
        stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
        args = (item_text, owner )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, owner):
        stmt = "SELECT description FROM items WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]  
        
    def checkin_status(self,item_text,checkinTime,owner): 
        print(self)
        stmt = "REPLACE INTO status (status,checkinTime, owner) VALUES (?, ?, ?)"
        args = (item_text, checkinTime, owner)
        self.conn.execute(stmt, args)
        self.conn.commit() 
    
    def get_status(self, owner):
        stmt = "SELECT status FROM status WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]     
        
    def get_checkinTime(self, owner):
        stmt = "SELECT checkinTime FROM status WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]   
        
    def delete_status(self, item_text, owner):
        stmt = "DELETE FROM status WHERE status = (?) AND owner = (?)"
        args = (item_text, owner )
        self.conn.execute(stmt, args)
        self.conn.commit()   
            
    def get_summary(self,date):
        stmt = "SELECT * FROM items WHERE date = (?)" 
        args = (date, )
        return [x for x in self.conn.execute(stmt,args)]
        