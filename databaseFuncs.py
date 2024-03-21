import sqlite3
from queue import Queue
import threading

class DatabaseConnection:
    
    def __init__(self, path:str) -> None:
        self.queue = Queue()
        self.path = path

        self.startHandler()

    def newConnection(self):
        connection = sqlite3.connect(self.path)
        return connection

    def executeQueuedQueries(self):
        while True:
            arguments = self.queue.get()
            query = arguments[0]
            args = arguments[1]
            db = self.newConnection()
            cursor = db.cursor()
            
            if args == ():
                cursor.execute(query)
            else:
                cursor.execute(query, args)
            db.commit()
            queryOutput = cursor.fetchall()
            self.queue.task_done()
            db.close()

            return queryOutput


    def startHandler(self):
        for thread in range(10):
            threading.Thread(target=self.executeQueuedQueries, daemon=True).start()

    def execute(self, query:str, args:tuple=()) -> list:
        print(f'Executing {query} {"with" + args if args != () else ""}')
        self.queue.put((query, args))
        return self.executeQueuedQueries()



class Database:

    def __init__(self, DatabaseConnection:object) -> None:
        self.cursor = DatabaseConnection

    # def getRecords(self, table:str, column='*', where='') -> list:
    #     query = f'SELECT {column} FROM {table}' 
    #     where = where.split(' ') if where else ''
    #     query += f' WHERE {where[0]} {where[1]} ?' if where else ''
    #     records = self.cursor.execute(query, (where[2] if where[2] else '',))
    #     return records if records is not None else []
    
    # def addRecords(self, table:str, values:tuple) -> None:
    #     query = f'INSERT INTO {table} VALUES (?);'
    #     self.cursor.execute(query, values)
        
    def getAllViewings(self) -> list:
        return self.cursor.execute('SELECT * FROM Viewings;')
    
    def getUpcomingViewingIDs(self) -> list:
        return self.cursor.execute("SELECT viewingID FROM Viewings WHERE datetime(viewingDate) >= datetime('now') ORDER BY viewingDate ASC;")
    
    def getTicketTypes(self) -> list:
        return self.cursor.execute('SELECT * FROM ticketTypes')
    
    def getReservedSeats(self, viewingID) -> list:
        return self.cursor.execute('SELECT Seat FROM Tickets WHERE ViewingID = ?;', (viewingID,))
    
    def getUnavailableSeats(self, viewingID) -> list:
        return self.cursor.execute('SELECT seat FROM unavailableSeats WHERE ViewingID = ?;', (viewingID,))
    
    def getTicketByID(self, ticketID) -> list:
        return self.cursor.execute('SELECT * FROM Tickets WHERE ID = ?;', (ticketID,))

    def newTicket(self, ticket:object, customer:object, viewing:object) -> None:
        self.cursor.execute('INSERT INTO Tickets VALUES (?, ?, ?, ?, ?);', (ticket.getID(), ticket.getSeatLocation(), ticket.getType(), customer.getID(), viewing.getID(),))

    def submitViewing():
        pass
    # def getLastID(self, table:str) -> int:
    #     self.cursor.execute('SELECT last_insert_rowid() FROM ;', (table,))
    #     return self.cursor.fetchone()[0]
