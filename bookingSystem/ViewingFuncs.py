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
                                                   rowCount=viewing[5], seatsPerRow=viewing[6],
                                                   inDB=True)
            
        # Update the remaining seat count for each viewing
        seatsRemaining = self.getAllRemainingSeatCounts()
        for viewingID in self.allViewings:
            self.allViewings[viewingID].remainingSeatCount = seatsRemaining[viewingID]

        return self.allViewings
    
    def newViewing(self, Name, DateTime:datetime, rowCount, seatsPerRow) -> object:
        Date = DateTime.date()
        Time = DateTime.time()
        newViewing = Viewing(self.Database, None, Name, Date, Time, rowCount, seatsPerRow)
        #newViewing.submitToDB()
        return newViewing
    
    def getStoredViewingByID(self, viewingID) -> object:
        return self.allViewings.get(viewingID, None)
    
    def getAllRemainingSeatCounts(self) -> dict:
        seatCounts = dict()
        # Fetches all viewing IDs and places them as keys in the dictionary
        for viewingID in self.allViewings:
            viewing = self.allViewings[viewingID]
            seatCounts[viewingID] = viewing.seatsPerRow * viewing.rowCount

        # Counts the number of remaining seats for each viewing
        if len(self.allViewings) != 0:
            # Uses a single query to get all unavailable seats - Faster than querying for each viewing
            for viewing in self.Database.getAllUnavailableSeats():
                if viewing[0] in seatCounts: 
                    seatCounts[viewing[0]] -= 1
        
        return seatCounts

    
    def getUpcomingViewingsAsList(self) -> list:
        upcomingViewingIDs = self.Database.getUpcomingViewingIDs()
        upcomingViewingsList = []
        self.getAllViewingsFromDB()

        # Format the viewings for Jinja to render
        for viewingID in upcomingViewingIDs:
            viewing = vars(self.getStoredViewingByID(viewingID[0]))
            viewingFormatted = {'Name': viewing['Name'], 'Date': viewing['Date'],
                                'Time': viewing['Time'],'Description': viewing['Description'],
                                'Banner': viewing['Banner'],'viewingID': viewing['viewingID'],
                                'remainingSeatCount': viewing['remainingSeatCount']}
            viewingFormatted['Date'] = viewingFormatted['Date'].strftime('%Y-%m-%d')
            viewingFormatted['Time'] = viewingFormatted['Time'].strftime('%H:%M')

            upcomingViewingsList.append(viewingFormatted)
        
        return upcomingViewingsList
    

class Viewing:
    def __init__(self, Database, viewingID, Name, 
                 Date, Time, rowCount, seatsPerRow, 
                 Description='', viewingBanner=None, 
                 remainingSeatCount=None, inDB=False) -> None:
        self.Database = Database
        self.viewingID = viewingID
        self.Name = Name
        self.Banner = viewingBanner
        self.Description = Description
        self.Date = Date
        self.Time = Time
        self.inDB = inDB

        self.rowCount = rowCount
        self.seatsPerRow = seatsPerRow
        self.seatNames = []
        self.remainingSeatCount = remainingSeatCount
        self.reservedSeats = None
        self.unavailableSeats = None

        # if self.inDB and self.remainingSeatCount == None:
            # self.getRemainingSeats()

        # Generate seat names - 'A1', 'A2', 'A3', etc.
        for SeatRow in range(1, rowCount + 1):
            for Seat in range(1, seatsPerRow + 1):
                rowLetter = chr(ord('A') + SeatRow - 1)
                stringValue = f"{rowLetter}{str(Seat)}"
                self.seatNames.append(stringValue)
        
        # Generate a unique ID for the viewing
        if self.inDB == False:
            self.viewingID = uuid.uuid4().int & (1<<32)-1

    def getID(self) -> int:
        return self.viewingID
    
    def getName(self) -> str:
        return self.Name
    
    def getDate(self) -> datetime.date:
        return self.Date
        
    def getSeatNames(self) -> list:
        return self.seatNames
    
    def getRemainingSeats(self) -> int:
        self.remainingSeatCount = self.seatsPerRow * self.rowCount
        self.remainingSeatCount -= len(self.getReservedSeats())
        self.remainingSeatCount -= len(self.getUnavailableSeats())
        return self.remainingSeatCount
    
    def getReservedSeats(self) -> int:
        self.reservedSeats = self.Database.getReservedSeats(self.viewingID)
        return self.reservedSeats
    
    def getUnavailableSeats(self) -> int:
        self.unavailableSeats = self.Database.getUnavailableSeats(self.viewingID)
        return self.unavailableSeats
    
    def getRowLength(self) -> int:
        return self.seatsPerRow
    
    def submitToDB(self) -> None:
        self.Database.addRecords('Viewings', (self.viewingID, self.Name, self.Description, self.Banner, self.Date, self.rowCount, self.seatsPerRow))
        self.inDB = True
    
    def submitTicket(self, Ticket:object, Customer:object) -> None:
        self.Database.newTicket(Ticket, Customer, self)