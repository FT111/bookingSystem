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
            query, args = self.queue.get()
            db = self.newConnection().cursor()
            db.execute(query, args)
            queryOutput = db.fetchall()
            self.queue.task_done()
            db.close()
            return queryOutput

    def startHandler(self):
        for _ in range(10):
            threading.Thread(target=self.executeQueuedQueries, daemon=True).start()

    def execute(self, query:str, args:tuple) -> None:
        self.queue.put((query, args))

    

    # TODO FIX THIS BULLSHIT 
    # omds


class Database:
    def __init__(self, DatabaseConnection:object) -> None:
        self.cursor = DatabaseConnection


    # Gets rows from the database - Reduces risk of SQL injection
    def getRecords(self, table:str, column='*', where='') -> list:
        query = f'SELECT {column} FROM {table}' 
        query += f' WHERE ?' if where else ''
        records = self.cursor.execute(query, (where,))
        return records if records is not None else []
    
    def addRecords(self, table:str, values:tuple) -> None:
        self.cursor.execute('INSERT INTO ? VALUES ?;', (table, values,))
    
    def getPrices(self) -> list:
        return self.getRecords('Prices')
    
    def getReservedSeats(self, viewingID) -> list:
        return self.getRecords('Tickets', 'Seat', f'ViewingID = {viewingID}')
    
    def getUnavailableSeats(self, viewingID) -> list:
        return self.getRecords('UnavailableSeats', 'Seat', f'ViewingID = {viewingID}')

    def getLastID(self, table:str) -> int:
        self.cursor.execute('SELECT last_insert_rowid() FROM %s;', (table,))
        return self.cursor.fetchone()[0]
