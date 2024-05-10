import qrcode
import uuid
import math


class TicketTypes:
    """
    A class wrapping the ticket types in the booking system.
    Retrieves the ticket types from the database.
    """

    def __init__(self, Database, Viewings) -> None:
        self.allTypes = dict()
        self.Database = Database
        self.Viewings = Viewings

    def getTypes(self) -> list:
        """
        Retrieves all ticket types from the database.

        Returns:
            A dictionary where the key is the ticket type ID and the value is a dictionary representing the ticket type.
        """
        typesTuple = self.Database.getTicketTypes()
        self.allTypes = {}

        for type in typesTuple:
            self.allTypes[type[0]] = {'ID': type[0], 'Name': type[1], 'Price': type[2]}

        return [*self.allTypes.values()]

    def getTypesForViewing(self, viewingID: str) -> list:
        self.getTypes()

        ticketsSold = len(self.Database.getReservedSeats(viewingID))
        timeTillViewing = self.Viewings.getStoredViewingByID(viewingID).getTimeTillViewing()

        for ticketTypeID, ticketType in self.allTypes.items():
            ticketType['Price'] = self.calculatePriceForTicket(ticketType['Price'], ticketsSold, timeTillViewing)

        return [*self.allTypes.values()]

    def getTypePriceForViewing(self, viewingID: str, ticketType: str) -> dict:
        self.getTypesForViewing(viewingID)
        return self.allTypes.get(int(ticketType))['Price']

    @staticmethod
    def calculatePriceForTicket(ticketPrice, ticketsSold, timeTillViewing):
        if ticketPrice != 0:
            if timeTillViewing - 604800 < 0:
                ticketPrice += (604800 - timeTillViewing) * 0.00003
            if ticketsSold > 25:
                ticketPrice += 0.05 * math.log(ticketsSold)

        return round(ticketPrice, 1)

### Container pattern heirachy: Bookings -> Booking -> Ticket


class Ticket:
    Database = None
    qrDomain = None

    @classmethod
    def setHostName(cls, qrDomain: str) -> None:
        cls.qrDomain = qrDomain

    @classmethod
    def setDatabase(cls, Database: object) -> None:
        cls.Database = Database

    def __init__(self, ticketType: str, price: float = 0, seatLocation=None) -> None:
        self.ticketType = ticketType
        self.seatLocation = seatLocation
        self.qrCodeURL = None
        self.price = price

        self.id = uuid.uuid4().int
        self.id = str(self.id)[:16]

    def getID(self) -> str:
        return self.id

    def getType(self) -> str:
        return self.ticketType

    def getSeatLocation(self) -> str:
        return self.seatLocation

    def getPrice(self) -> float:
        return self.price

    def setTicketType(self, ticketType: str) -> None:
        self.ticketType = ticketType

    def setSeatLocation(self, seatLocation: str) -> None:
        self.seatLocation = seatLocation

    def generateQR(self) -> str:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        if self.qrDomain:
            self.qrCodeURL = f'{self.qrDomain}/{self.id}'
        else:
            self.qrCodeURL = self.id

        qr.add_data(self.qrCodeURL)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f'./static/assets/codes/{self.id}.png')

        return self.qrCodeURL

    def getQR(self) -> str:
        return self.qrCodeURL


class Booking:
    """
    Represents a booking made by a customer for a viewing.
    Not submitted directly to the database, but instead the booking's tickets are.

    Attributes:
    - TicketTypes: A reference to the TicketTypes object that contains information about available ticket types.
    - Database: A reference to the Database object used for storing booking information.
    - Customer: The customer who made the booking.
    - Viewing: The viewing object for which the booking is made.
    - Tickets: A list of tickets included in the booking.
    - bookingID: The unique ID of the booking.
    - selectedSeats: A list of seats selected for the booking.

    Methods:
    - setTicketTypes: Class method - Sets the TicketTypes object for all booking instances.

    - getID: Returns the ID of the booking.
    - addTicket: Adds a ticket to the booking.
    - removeTicket: Removes a ticket from the booking.
    - addSeat: Adds a seat to the booking.
    - removeSeat: Removes a seat from the booking.
    - resetSeats: Resets the selected seats for the booking.
    - getSelectedSeats: Returns the selected seats for the booking.
    - removeTicketOfType: Removes all tickets of a specific type from the booking.
    - getTickets: Returns the list of tickets in the booking.
    - getTicketCountPerType: Returns a dictionary with the count of tickets per ticket type.
    - getPriceSum: Returns the total price of the booking.
    - getViewing: Returns the viewing object for the booking.
    - setCustomer: Sets the customer for the booking.
    - getCustomer: Returns the customer for the booking.

    - Submit: Submits the booking.
    - confirmBooking: Sends a confirmation email for the booking.
    """

    TicketTypes = None

    @classmethod
    def setTicketTypes(cls, TicketTypes: object) -> None:
        cls.TicketTypes = TicketTypes

    @classmethod
    def setEmailFuncs(cls, EmailFuncs: object) -> None:
        cls.EmailFuncs = EmailFuncs

    def __init__(self, Database: object, ViewingObj: object) -> None:
        self.Database = Database
        self.Customer = None
        self.Viewing = ViewingObj
        self.Tickets = []
        self.bookingID = str(uuid.uuid4().int)
        self.selectedSeats = []

    def getID(self) -> str:
        return self.bookingID

    def addTicket(self, ticket: object) -> bool:
        if len(self.Tickets) >= self.Viewing.getRemainingSeats():
            return False
        self.Tickets.append(ticket)
        return True

    def removeTicket(self, ticket: object) -> bool:
        if ticket not in self.Tickets:
            return False
        self.Tickets.remove(ticket)
        return False

    def addSeat(self, seat: str) -> bool:
        # Validates that the seat is an available, existing seat
        if seat in self.Viewing.getUnavailableSeats() or seat in self.Viewing.getReservedSeats() or seat not in self.Viewing.getSeatNames():
            return False

        self.selectedSeats.append(seat)
        return True

    def removeSeat(self, seat: str) -> bool:
        if seat not in self.selectedSeats:
            return False
        self.selectedSeats.remove(seat)

    def resetSeats(self) -> None:
        self.selectedSeats = []

    def getSelectedSeats(self):
        return self.selectedSeats

    def removeTicketOfType(self, ticketType: str) -> None:
        for ticket in self.Tickets:
            if ticket.getType() == ticketType:
                self.Tickets.remove(ticket)
                break

    def getTickets(self) -> list:
        return self.Tickets

    def getTicketCountPerType(self) -> dict:
        ticketCounts = dict()
        ticketTypes = self.TicketTypes.getTypesForViewing(self.Viewing.getID())

        # Fill the dictionary with ticket types
        for ticketType in ticketTypes:
            ticketCounts[ticketType['ID']] = 0

        # Count the number of tickets of each type
        for ticket in self.Tickets:
            ticketCounts[ticket.getType()] += 1

        return ticketCounts

    def getPriceSum(self) -> float:
        priceSum = 0

        for ticket in self.Tickets:
            priceSum += ticket.getPrice()

        return priceSum

    def getViewing(self) -> object:
        return self.Viewing

    def setCustomer(self, Customer: object) -> None:
        self.Customer = Customer

    def getCustomer(self) -> object:
        return self.Customer

    def Submit(self, seats=None) -> bool:
        # Validate that the booking has a customer
        if self.Customer is None:
            return False

        # Validate that the requested seats are available
        unavailableSeats = self.Viewing.getUnavailableSeats()
        unavailableSeats += self.Viewing.getReservedSeats()
        if seats is not None:
            seats = list(seats)

        # Validate that the booking has tickets
        if len(self.Tickets) == 0:
            return False

        # Handles assigning seats to tickets if they are not already assigned
        if seats:
            if len(seats) != len(self.Tickets):
                return False

            for ticket in self.Tickets:
                ticket.setSeatLocation(seats.pop(0))

        if not seats:
            for ticket in self.Tickets:
                if ticket.getSeatLocation() in unavailableSeats or ticket.getSeatLocation() not in self.Viewing.getSeatNames():
                    self.Tickets = []
                    return False

        else:
            for seat in seats:
                if seat in unavailableSeats or seat not in self.Viewing.getSeatNames():
                    self.Tickets = []
                    return False

        # If the seats are available, submit the booking
        for ticket in self.Tickets:
            self.Viewing.submitTicket(ticket, self.Customer)
            ticket.generateQR()

        self.EmailFuncs.sendBookingConfirmation(self.Customer.getEmail(), self, self.Customer,
                                                self.Viewing, self.Tickets)

        return True


class Bookings:
    """
    Represents the system's currently stored bookings.
    Wraps the collection of bookings and provides methods for managing them.

    Attributes:
        Database (object): The database object used for storing booking information.
        allBookings (dict): A dictionary containing all the bookings, with booking IDs as keys and Booking objects as values.
    Methods:
        newBooking: Creates a new booking and adds it to the collection of bookings.
        removeBooking: Removes a booking from the collection of bookings.
        getBookingByID: Retrieves a booking from the collection of bookings based on its ID.
    """

    def __init__(self, Database: object) -> None:
        self.Database = Database
        self.allBookings: {str: Booking} = dict()

    def newBooking(self, ID: str, ViewingObj: object) -> Booking:
        """
        Creates a new booking and adds it to the collection of bookings.

        Args:
            ID (str): The ID of the booking.
            ViewingObj (object): The viewing object associated with the booking.

        Returns:
            int: The booking object that was created.
        """

        newBooking = Booking(self.Database, ViewingObj)
        self.allBookings[ID] = newBooking

        return newBooking

    def removeBooking(self, index: int) -> bool:
        """
        Removes a booking from the collection of bookings.

        Args:
            index (int): The index of the booking to be removed.
        """
        try:
            del self.allBookings[index]
            return True
        except KeyError:
            return False

    def getBookingByID(self, index: int) -> object:
        """
        Retrieves a booking from the collection of bookings based on its ID.

        Args:
            index (int): The ID of the booking to be retrieved.

        Returns:
            object: The booking object with the specified ID, or None if it doesn't exist.
        """

        # Attempts to retrieve the current booking
        try:
            return self.allBookings[index]
        except KeyError:
            return None


