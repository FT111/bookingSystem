import sqlite3
from queue import Queue
import threading


class DatabaseConnection:

    def __init__(self, path: str) -> None:
        self.queue = Queue()
        self.path = path

        self.startHandler()

    def newConnection(self):
        connection = sqlite3.connect(self.path)
        return connection

    def executeQueuedQueries(self):
        while True:
            # file deepcode ignore single~iteration~loop: <please specify a reason of ignoring this>
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

    def execute(self, query: str, args: tuple = ()) -> list:
        try:
            print(f'Executing {query} {"with" + args if args != () else ""}')
        except TypeError:
            print(f'Executing {query}')
        self.queue.put((query, args))
        return self.executeQueuedQueries()


class Database:
    def __init__(self, DBConnectionInstance: object) -> None:
        self.cursor = DBConnectionInstance

        self.acceptedCustomerColumns = ['ID', 'firstName', 'Surname', 'emailAddress', 'phoneNumber']
        self.acceptedViewingColumns = ['ViewingID', 'viewingName', 'viewingDesc', 'viewingBanner', 'viewingDate',
                                       'viewingRows', 'seatsPerRow']

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

    def getAllViewingIDs(self) -> list:
        return self.cursor.execute('SELECT viewingID FROM Viewings;')

    def getUpcomingViewingIDs(self) -> list:
        return self.cursor.execute("""SELECT viewingID FROM Viewings WHERE datetime(viewingDate) >= datetime('now')
                                      ORDER BY viewingDate ASC;""")

    def getTicketTypes(self) -> list:
        return self.cursor.execute('SELECT * FROM ticketTypes')

    def getReservedSeats(self, viewingID) -> list:
        reservedSeatTuples = self.cursor.execute('SELECT seat FROM Tickets WHERE ViewingID = ?;', (viewingID,))
        reservedSeatList = [seat[0] for seat in reservedSeatTuples]

        return reservedSeatList

    def getUnavailableSeats(self, viewingID) -> list:
        unavailableSeatTuples = self.cursor.execute('SELECT seat FROM unavailableSeats WHERE ViewingID = ?;',
                                                    (viewingID,))
        unavailableSeatList = [seat[0] for seat in unavailableSeatTuples]

        return unavailableSeatList

    def getAllReservedSeats(self) -> list:
        reservedSeats = self.cursor.execute('SELECT ViewingID FROM Tickets;')
        return reservedSeats

    def getAllUnavailableSeats(self) -> list:
        unavailableSeats = self.cursor.execute('SELECT ViewingID FROM Tickets;')
        unavailableSeats += self.cursor.execute('SELECT ViewingID FROM unavailableSeats;')
        return unavailableSeats

    def addUnavailableSeats(self, viewingID, seats: list) -> None:
        baseQuery = 'INSERT INTO unavailableSeats '
        wildCards = []
        for index, seat in enumerate(seats):
            wildCards += [seat, viewingID]
            baseQuery += f'SELECT ?, ? {"UNION ALL" if index != len(seats)-1 else ';'} '

        print(baseQuery, wildCards)

        self.cursor.execute(baseQuery, (*wildCards,))

    def removeUnavailableSeats(self, viewingID, seats: list) -> None:
        seatsPlaceholders = ",".join("?" * len(seats))
        baseQuery = f'DELETE FROM unavailableSeats WHERE ViewingID = ? AND Seat IN ({seatsPlaceholders})'
        wildCards = [viewingID] + seats

        self.cursor.execute(baseQuery, wildCards)

    def getTicketsByViewingID(self, viewingID, *columns) -> iter:
        if columns:
            sqlColumns = ', '.join(columns)
            tickets = self.cursor.execute(f'SELECT {sqlColumns} FROM Tickets WHERE ViewingID = ?;', (viewingID,))
            return self.zipColumnsToDict(columns, tickets)

        return self.cursor.execute('SELECT * FROM Tickets WHERE ViewingID = ?;', (viewingID,))

    def getTicketByID(self, ticketID) -> list:
        return self.cursor.execute('SELECT * FROM Tickets WHERE ID = ?;', (ticketID,))

    def newTicket(self, ticket: object, customer: object, viewing: object) -> None:
        self.cursor.execute('INSERT INTO Tickets VALUES (?, ?, ?, ?, ?);', (
            ticket.getID(), ticket.getSeatLocation(), ticket.getType(), customer.getID(), viewing.getID(),))

    def removeTicket(self, viewingID, ticketID: int) -> None:
        self.cursor.execute('DELETE FROM Tickets WHERE ViewingID = ? AND CustomerID = ?;', (viewingID, ticketID,))

    def getAllTickets(self) -> list:
        return self.cursor.execute('SELECT * FROM Tickets;')

    def newCustomer(self, customer: object) -> None:
        self.cursor.execute('INSERT INTO Customers VALUES (?, ?, ?, ?, ?);', (
            customer.getID(), customer.getFirstName(), customer.getSurname(), customer.getEmail(),
            customer.getPhoneNumber(),))

    def getCustomerInfoByID(self, ID: int) -> list:
        return self.cursor.execute('SELECT * FROM Customers WHERE ID = ?;', (ID,))

    def getAllCustomers(self) -> list:
        return self.cursor.execute('SELECT * FROM Customers;')

    def getAllCustomerInfo(self, columns: list) -> list:
        for column in columns:
            if column not in self.acceptedCustomerColumns:
                return []
        sqlColumns = ', '.join(columns)
        response = self.cursor.execute(f'SELECT {sqlColumns} FROM Customers ORDER BY Surname ASC;')
        return self.zipColumnsToDict(columns, response)

    def getAllViewingInfo(self, columns: list) -> list:
        for column in columns:
            if column not in self.acceptedViewingColumns:
                return []
        sqlColumns = ', '.join(columns)
        response = self.cursor.execute(f'SELECT {sqlColumns} FROM Viewings;')
        return self.zipColumnsToDict(columns, response)

    def deleteViewing(self, viewingID: int) -> None:
        self.cursor.execute('DELETE FROM Viewings WHERE ViewingID = ?;', (viewingID,))

    def newViewing(self, viewing: object) -> None:
        viewingDateTime = f'{viewing.getDate().strftime("%Y-%m-%d")} {viewing.getTime().strftime("%H:%M")}:00'

        self.cursor.execute('INSERT INTO Viewings VALUES (?, ?, ?, ?, ?, ?, ?);', (viewing.getID(),
                                                                                   viewing.getName(),
                                                                                   viewing.getDescription(),
                                                                                   viewing.getBanner(),
                                                                                   viewingDateTime,
                                                                                   viewing.getRowCount(),
                                                                                   viewing.getRowLength(),))

    @staticmethod
    def zipColumnsToDict(columns, response) -> list:
        for index, record in enumerate(response):
            response[index] = dict(zip(columns, record))
        return response

    def submitViewing(self):
        pass
