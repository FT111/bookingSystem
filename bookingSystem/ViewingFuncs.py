import uuid
from datetime import datetime
import json

class Viewings:
    def __init__(self, Database) -> None:
        self.allViewings = dict()
        self.Database = Database

    def getAllViewingsFromDB(self) -> dict:
        viewings = self.Database.getAllViewings()
        for viewing in viewings:
            # Format YY/MM/DD
            dateTimeObject = datetime.strptime(viewing[4], '%Y-%m-%d %H:%M:%S')
            viewingDate = dateTimeObject.date()
            viewingTime = dateTimeObject.time()
            self.allViewings[viewing[0]] = Viewing(self.Database, 
                                                   viewingID=viewing[0], Name=viewing[1], 
                                                   Description=viewing[2], viewingBanner=viewing[3], 
                                                   Date=viewingDate, Time=viewingTime,
                                                   rowCount=viewing[5], seatsPerRow=viewing[6])
        return self.allViewings
    
    def newViewing(self, Name, DateTime:datetime, rowCount, seatsPerRow) -> object:
        Date = DateTime.date()
        Time = DateTime.time()
        newViewing = Viewing(self.Database, None, Name, Date, Time, rowCount, seatsPerRow)
        #newViewing.submitToDB()
        return newViewing
    
    def getStoredViewingByID(self, viewingID) -> object:
        return self.allViewings.get(viewingID, None)
    
    def getUpcomingViewingsAsList(self) -> list:
        upcomingViewingIDs = self.Database.getUpcomingViewingIDs()
        upcomingViewingsList = []
        self.getAllViewingsFromDB()
        for viewingID in upcomingViewingIDs:
            viewing = vars(self.getStoredViewingByID(viewingID[0]))
            viewingFormatted = {'Name': viewing['Name'], 'Date': viewing['Date'],
                                'Time': viewing['Time'],'Description': viewing['Description'],
                                'Banner': viewing['Banner'],'viewingID': viewing['viewingID']}
            viewingFormatted['Date'] = viewingFormatted['Date'].strftime('%Y-%m-%d')
            viewingFormatted['Time'] = viewingFormatted['Time'].strftime('%H:%M')

            upcomingViewingsList.append(viewingFormatted)
        
        return upcomingViewingsList
    

class Viewing:
    def __init__(self, Database, viewingID, Name, 
                 Date, Time, rowCount, seatsPerRow, 
                 Description='', viewingBanner=None) -> None:
        self.Database = Database
        self.viewingID = viewingID
        self.Name = Name
        self.Date = Date
        self.Time = Time
        self.rowCount = rowCount
        self.seatsPerRow = seatsPerRow

        self.Description = Description
        self.Banner = viewingBanner
        self.seatNames = []

        # Generate seat names - 'A1', 'A2', 'A3', etc.
        for SeatRow in range(1, rowCount + 1):
            for Seat in range(1, seatsPerRow + 1):
                rowLetter = chr(ord('A') + SeatRow - 1)
                stringValue = f"{rowLetter}{str(Seat)}"
                self.seatNames.append(stringValue)
        
        # Generate a unique ID for the viewing
        if self.viewingID == None:
            self.viewingID = uuid.uuid4().int & (1<<32)-1

    def getID(self):
        return self.viewingID
    
    def getName(self):
        return self.Name
    
    def getDate(self):
        return self.Date
        
    def getSeatNames(self):
        return self.seatNames
    
    def getRowLength(self):
        return self.seatsPerRow
    
    def submitToDB(self):
        self.Database.addRecords('Viewings', (self.viewingID, self.Name, self.Description, self.Banner, self.Date, self.rowCount, self.seatsPerRow))
    
    def submitTicket(self, Ticket:object, Customer:object):
        self.Database.newTicket(Ticket, Customer, self)