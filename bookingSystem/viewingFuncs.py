import uuid
from datetime import datetime, time
import time

from functools import wraps


class Viewings:
    ticketTypes = None

    @classmethod
    def setTicketTypes(cls, TicketTypes) -> None:
        cls.ticketTypes = TicketTypes

    def __init__(self, Database) -> None:
        self.allViewings: {int: Viewing} = dict()
        self.Database = Database
        self.stats = dict()

    def getAllViewingsFromDB(self) -> dict:
        viewings = self.Database.getAllViewings()
        self.allViewings = dict()

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

    def newViewing(self, Name, Date: str, Time: str, rowCount, seatsPerRow, BannerURL=None,
                   Description: str = None) -> object:
        try:
            Date = datetime.strptime(Date, '%Y-%m-%d')
            Time = datetime.strptime(Time, '%H:%M')
        except ValueError:
            raise ValueError("Invalid date/time format, please use YYYY-MM-DD and HH:MM.")
        try:
            rowCount = int(rowCount)
            seatsPerRow = int(seatsPerRow)
        except ValueError:
            raise ValueError("Invalid row count or seats per row, please use strings or integers.")

        if (seatsPerRow * rowCount) < 1:
            raise ValueError('Seating must be greater or equal to 1x1.')

        newViewing = Viewing(self.Database, None, Name, Date, Time, rowCount, seatsPerRow, Description, BannerURL)
        newViewing.submitToDB()

        return newViewing

    def getStoredViewings(self) -> dict:
        return self.allViewings

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

    @staticmethod
    def formatViewing(viewing) -> dict:
        viewingFormatted = {'Name': viewing['Name'], 'Date': viewing['Date'],
                            'Time': viewing['Time'], 'Description': viewing['Description'],
                            'Banner': viewing['Banner'], 'viewingID': viewing['viewingID'],
                            'remainingSeatCount': viewing['remainingSeatCount']}
        viewingFormatted['Date'] = viewingFormatted['Date'].strftime('%Y-%m-%d')
        viewingFormatted['Time'] = viewingFormatted['Time'].strftime('%H:%M')
        viewingFormatted['dateFormatted'] = datetime.strptime(viewingFormatted['Date'], '%Y-%m-%d').strftime('%d/%m/%Y')

        return viewingFormatted

    def getAllViewingsAsList(self) -> list:
        self.getAllViewingsFromDB()

        viewingsList = [self.formatViewing(vars(viewing)) for viewing in self.allViewings.values()]

        return viewingsList

    def getUpcomingViewingsAsList(self) -> list:
        upcomingViewingIDs = self.Database.getUpcomingViewingIDs()
        upcomingViewingsList = []
        self.getAllViewingsFromDB()

        # Format the viewings for Jinja to render
        for viewingID in upcomingViewingIDs:
            viewingFormatted = self.formatViewing(vars(self.getStoredViewingByID(viewingID[0])))

            upcomingViewingsList.append(viewingFormatted)

        return upcomingViewingsList

    def deleteViewing(self, viewingID) -> None:
        viewing = self.getStoredViewingByID(viewingID)
        viewing.delete()
        self.allViewings.pop(viewingID)

    def getStats(self, viewingID: int = None, timePeriod: str = None) -> dict[str:any]:

        allViewingInfo = self.Database.getAllViewingInfo(['ViewingID', 'viewingName', 'viewingDate',
                                                          'viewingRows', 'seatsPerRow'])
        allTickets = self.Database.getAllTickets()
        upcomingViewingIDs = [viewingID[0] for viewingID in self.Database.getUpcomingViewingIDs()]
        ticketTypes = self.ticketTypes.getTypes()

        overallRevenue = self.getOverallRevenue(allTickets, ticketTypes)

        filteredViewingInfo = self.filterViewingsByTimePeriod(allViewingInfo, timePeriod, upcomingViewingIDs, viewingID)

        # Filters the tickets and viewingIDs based on the selected viewings
        viewingIDs = [viewing['ViewingID'] for viewing in filteredViewingInfo]

        selectedTickets = [ticket for ticket in allTickets if int(ticket[4]) in viewingIDs]

        seatsPerViewing = {viewing['ViewingID']: viewing['viewingRows'] * viewing['seatsPerRow']
                           for viewing in filteredViewingInfo}

        statsPerViewing = {viewing['ViewingID']: {'viewingName': viewing['viewingName'], 'tickets': 0, 'revenue': 0}
                           for viewing in filteredViewingInfo}

        # Calculating the statistics

        self.stats['totalRevenue'] = self.getRevenueForTickets(selectedTickets, statsPerViewing, ticketTypes)

        # Adding basic statistics to the dictionary
        self.stats['lastUpdated'] = time.time()
        self.stats['totalViewings'] = len(filteredViewingInfo)
        self.stats['totalTickets'] = len(selectedTickets)
        self.stats['statsPerViewing'] = list(statsPerViewing.values())

        self.stats['remainingSeats'] = 0
        self.stats['mostRemaining'] = {'viewingName': None, 'remainingSeats': 0}

        self.getRemainingSeatsForViewings(filteredViewingInfo, seatsPerViewing, statsPerViewing)

        if self.stats['totalViewings'] != 0:
            self.stats['meanRevenuePerViewing'] = round(self.stats['totalRevenue'] / self.stats['totalViewings'], 2)
        else:
            self.stats['meanRevenuePerViewing'] = 0

        self.stats['mostPopularViewing'] = {'viewingName': None, 'tickets': 0}

        self.getMostSoldViewingForViewings(statsPerViewing)

        # Calculates the percentage of tickets sold
        try:
            self.stats['percentageSold'] = round(
                (self.stats['totalTickets'] / (self.stats['remainingSeats'] + self.stats['totalTickets'])) * 100, 2)
            meanRevenueForAllViewings = round(overallRevenue / len(allViewingInfo), 2)

        except ZeroDivisionError:
            self.stats['percentageSold'] = 0
            meanRevenueForAllViewings = 0
        # Calculates the mean revenue for all viewings

        self.getPercentageTicketsSoldToMeanSold(meanRevenueForAllViewings)

        return self.stats

    def getPercentageTicketsSoldToMeanSold(self, meanRevenueForAllViewings):
        # Calculates the percentage of revenue for the selected viewings compared to all viewings
        try:
            self.stats['percentageToMean'] = (self.stats['meanRevenuePerViewing'] / meanRevenueForAllViewings) * 100
            if self.stats['meanRevenuePerViewing'] < meanRevenueForAllViewings:
                self.stats[
                    'percentageToMean'] = f"<strong>{round(100 - self.stats['percentageToMean'], 2)}%</strong> below mean revenue"
            elif self.stats['meanRevenuePerViewing'] == meanRevenueForAllViewings:
                self.stats['percentageToMean'] = "Equal to mean revenue"
            else:
                self.stats[
                    'percentageToMean'] = f"<strong>{round(self.stats['percentageToMean'] - 100, 2)}%</strong> above mean revenue"
        except ZeroDivisionError:
            self.stats['percentageToMean'] = "No tickets or viewings available"

    def getMostSoldViewingForViewings(self, statsPerViewing):
        # Finds the viewing with the most tickets sold
        for viewing in statsPerViewing.values():
            if viewing['tickets'] > self.stats['mostPopularViewing']['tickets']:
                self.stats['mostPopularViewing']['viewingName'] = viewing['viewingName']
                self.stats['mostPopularViewing']['tickets'] = viewing['tickets']

    def getRemainingSeatsForViewings(self, filteredViewingInfo, seatsPerViewing, statsPerViewing):
        # Calculates the remaining seats for each viewing
        for viewing in filteredViewingInfo:
            seatsRemaining = seatsPerViewing[viewing['ViewingID']] - statsPerViewing[viewing['ViewingID']]['tickets']
            self.stats['remainingSeats'] += seatsRemaining
            if seatsRemaining > self.stats['mostRemaining']['remainingSeats']:
                self.stats['mostRemaining']['viewingName'] = viewing['viewingName']
                self.stats['mostRemaining']['remainingSeats'] = seatsRemaining

    @staticmethod
    def getRevenueForTickets(selectedTickets, statsPerViewing, ticketTypes) -> float:
        totalRevenue = 0
        # Calculates the revenue for each viewing, and the total
        for ticket in selectedTickets:
            try:
                price = float(ticket[5])
                ticketViewingID = int(ticket[4])

                statsPerViewing[ticketViewingID]['revenue'] += price
            except IndexError:
                price = 0
            totalRevenue += price

            if int(ticket[4]) in statsPerViewing:
                statsPerViewing[int(ticket[4])]['tickets'] += 1

        return totalRevenue

    @staticmethod
    def filterViewingsByTimePeriod(allViewingInfo: dict, timePeriod: str, upcomingViewingIDs: list, viewingID: int) -> dict:
        # Filters the viewings based on the selected time period
        if timePeriod == 'upcoming':
            filteredViewingInfo = [viewing for viewing in allViewingInfo if viewing['ViewingID'] in
                                   upcomingViewingIDs]
        elif timePeriod == 'past':
            filteredViewingInfo = [viewing for viewing in allViewingInfo if viewing['ViewingID'] not in
                                   upcomingViewingIDs]
        elif viewingID is not None:
            filteredViewingInfo = [viewing for viewing in allViewingInfo if viewing['ViewingID'] == viewingID]
        else:
            filteredViewingInfo = allViewingInfo
        return filteredViewingInfo

    @staticmethod
    def getOverallRevenue(allTickets, ticketTypes) -> float:
        overallRevenue = 0
        for ticket in allTickets:
            try:
                price = float(ticket[5])
            except IndexError:
                price = 0
            overallRevenue += price
        return overallRevenue


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

        self.rowCount = abs(rowCount)
        self.seatsPerRow = abs(seatsPerRow)

        self.seatNames = []
        self.remainingSeatCount = remainingSeatCount
        self.reservedSeats = None
        self.unavailableSeats = None

        # Generate seat names - 'A1', 'A2', 'A3', etc.
        for SeatRow in range(1, self.rowCount + 1):
            for Seat in range(1, self.seatsPerRow + 1):
                rowLetter = chr(ord('A') + SeatRow - 1)
                stringValue = f"{rowLetter}{str(Seat)}"
                self.seatNames.append(stringValue)

        # Generate a unique ID for the viewing
        if not self.inDB:
            self.viewingID = uuid.uuid4().int & (1 << 32) - 1

    def getID(self) -> int:
        return self.viewingID

    def getName(self) -> str:
        return self.Name

    def getDate(self) -> datetime.date:
        return self.Date

    def getFormattedDate(self) -> str:
        return self.Date.strftime('%d/%m/%Y')

    def getTime(self) -> datetime.time:
        return self.Time

    def getBanner(self) -> str:
        return self.Banner

    def getDescription(self) -> str:
        return self.Description

    def getRowCount(self) -> int:
        return self.rowCount

    def getSeatNames(self) -> list:
        return self.seatNames

    def getTimeTillViewing(self) -> float:
        viewingTime = datetime.combine(self.Date, self.Time)
        timeDifference = viewingTime - datetime.now()
        return timeDifference.total_seconds()

    def getRemainingSeats(self) -> int:
        self.remainingSeatCount = self.seatsPerRow * self.rowCount
        self.remainingSeatCount -= len(self.getReservedSeats())
        self.remainingSeatCount -= len(self.getUnavailableSeats())
        return self.remainingSeatCount

    def getReservedSeats(self) -> int:
        self.reservedSeats = self.Database.getReservedSeats(self.viewingID)
        return self.reservedSeats

    def getUnavailableSeats(self) -> list:
        self.unavailableSeats = self.Database.getUnavailableSeats(self.viewingID)
        return self.unavailableSeats

    def setUnavailableSeats(self, seats: list) -> bool:
        alreadyUnavailableSeats = self.getUnavailableSeats()
        addedSeats = []
        removedSeats = []
        for seat in seats:
            if seat not in alreadyUnavailableSeats:
                addedSeats.append(seat)

        for seat in alreadyUnavailableSeats:
            if seat not in seats:
                removedSeats.append(seat)

        if addedSeats:
            self.Database.addUnavailableSeats(self.viewingID, addedSeats)
        if removedSeats:
            self.Database.removeUnavailableSeats(self.viewingID, removedSeats)

        self.removeTickets(seats)

        return True

    def removeTickets(self, seats):
        # Remove tickets for reserved seats that are made unavailable
        ticketsForViewing = self.Database.getTicketsByViewingID(self.viewingID, 'CustomerID', 'Seat')

        # Compiles a list of all seat locations that are reserved for the viewing
        ticketSeats = {ticket['Seat']: ticket['CustomerID'] for ticket in ticketsForViewing}

        # Removes the ticket for the seat if it is made unavailable
        for seat in seats:
            if ticketSeats.get(seat) is not None:
                self.Database.removeTicket(self.viewingID, ticketSeats[seat])

    def getTicketInfo(self) -> list:
        ticketInfo = self.Database.getTicketsByViewingID(self.viewingID)

        formattedTickets = [{'TicketID': ticket[0], 'Seat': ticket[1], 'Type': ticket[2], 'CustomerID': ticket[3]} for
                            ticket in ticketInfo]

        return formattedTickets

    def getRowLength(self) -> int:
        return self.seatsPerRow

    def delete(self) -> None:
        self.Database.deleteViewing(self.viewingID)

        for ticket in self.getTicketInfo():
            self.Database.removeTicket(self.viewingID, ticket['TicketID'])

    def submitToDB(self) -> None:
        self.Database.newViewing(self)

        self.inDB = True

    def submitTicket(self, Ticket: object, Customer: object) -> None:
        self.Database.newTicket(Ticket, Customer, self)
