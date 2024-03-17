
class Viewings:
    def __init__(self, Database) -> None:
        self.allViewings = dict()
        self.Database = Database

    def getAllViewingsFromDB(self) -> dict:
        viewings = self.Database.getRecords('Viewings', '*')
        for viewing in viewings:
            self.allViewings[viewing[0]] = Viewing(self.Database, 
                                                   viewingID=viewing[0], Name=viewing[1], 
                                                   Description=viewing[2], viewingBanner=viewing[3], 
                                                   Date=viewing[4], 
                                                   rowCount=viewing[5],
                                                   seatsPerRow=viewing[6])
        return self.allViewings
    
    def newViewing(self, Name, Date, rowCount, seatsPerRow) -> object:
        newViewing = Viewing(self.Database, None, Name, Date, rowCount, seatsPerRow)
        #newViewing.submitToDB()
        return newViewing
    
    def getStoredViewing(self, viewingID) -> object:
        return self.allViewings.get(viewingID, None)
    

class Viewing:
    def __init__(self, Database, viewingID, Name, Date, rowCount, seatsPerRow, Description='', viewingBanner='') -> None:
        self.Database = Database
        self.viewingID = viewingID
        self.Name = Name
        self.Date = Date
        self.rowCount = rowCount
        self.seatsPerRow = seatsPerRow

        self.Desciption = Description
        self.Banner = viewingBanner
        self.seatNames = []

        for SeatRow in range(1, rowCount + 1):
            for Seat in range(1, seatsPerRow + 1):
                rowLetter = chr(ord('A') + SeatRow - 1)
                stringValue = f"{rowLetter}{str(Seat)}"
                self.seatNames.append(stringValue)
        
    def getSeatNames(self):
        return self.seatNames
    
    def getRowLength(self):
        return self.seatsPerRow
    
    def submitToDB(self):
        self.Database.addRecords('Viewings', (self.Name, self.Description, self.Banner, self.Date, self.rowCount, self.seatsPerRow))
    
    def submitTicket(self, Ticket:object, Customer:object):
        self.Database.addRecords('Tickets', (self.viewingID, Ticket.getID(), Ticket.getSeatLocation(), Ticket.getTicketType(), Customer.id))