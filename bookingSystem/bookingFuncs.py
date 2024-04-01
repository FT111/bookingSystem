from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import qrcode
import uuid
from flask import render_template


class TicketTypes:
    """
    A class wrapping the ticket types in the booking system.
    Retreives the ticket types from the database.
    """

    def __init__(self, Database) -> None:
        self.allTypes = list()
        self.Database = Database

    def getTypes(self) -> list:
        """
        Retrieves all ticket types from the database.

        Returns:
            A list of dictionaries representing each ticket type, with keys 'ID', 'Name', and 'Price'.
        """
        typesTuple = self.Database.getTicketTypes()
        self.allTypes = []
        for type in typesTuple:
            self.allTypes.append({'ID': type[0],
                                  'Name': type[1],
                                  'Price': type[2]})
        return self.allTypes


###
### Container pattern heirachy: Bookings -> Booking -> Ticket
###

class Ticket:
    Database = None

    @classmethod
    def setDatabase(cls, Database: object) -> None:
        cls.Database = Database

    def __init__(self, ticketType: str, seatLocation=None) -> None:
        self.ticketType = ticketType
        self.seatLocation = seatLocation
        self.qrCodeURL = None

        self.id = str(uuid.uuid4().int)

    def getID(self) -> str:
        return self.id

    def getType(self) -> str:
        return self.ticketType

    def getSeatLocation(self) -> str:
        return self.seatLocation

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
        qr.add_data(self.id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        self.qrCodeURL = f'./static/assets/codes/{self.id}.png'
        img.save(self.qrCodeURL)
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
    - setTicketTypes: Classmethod - Sets the TicketTypes object for all booking instances.

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
        ticketTypes = self.TicketTypes.getTypes()

        # Fill the dictionary with ticket types
        for type in ticketTypes:
            ticketCounts[type['ID']] = 0

        # Count the number of tickets of each type
        for ticket in self.Tickets:
            ticketCounts[ticket.getType()] += 1

        return ticketCounts

    def getPriceSum(self) -> float:
        ticketTypes = self.TicketTypes.getTypes()
        priceSum = 0

        for ticket in self.Tickets:
            for type in ticketTypes:
                if ticket.getType() == type['ID']:
                    priceSum += type['Price']
                    break

        return priceSum

    def getViewing(self) -> object:
        return self.Viewing

    def setCustomer(self, Customer: object) -> None:
        self.Customer = Customer

    def getCustomer(self) -> object:
        return self.Customer

    def Submit(self, seats=None) -> bool:
        print('Stage 0')
        # Validate that the booking has a customer
        if self.Customer is None:
            return False

        print('Stage 1')

        # Validate that the requested seats are available
        unavailableSeats = self.Viewing.getUnavailableSeats()
        unavailableSeats += self.Viewing.getReservedSeats()
        if seats is not None:
            seats = list(seats)

        print('Stage 2')

        # Validate that the booking has tickets
        if len(self.Tickets) == 0:
            return False

        print('Stage 3')

        # Handles assigning seats to tickets if they are not already assigned
        if seats:
            if len(seats) != len(self.Tickets):
                return False

            for ticket in self.Tickets:
                ticket.setSeatLocation(seats.pop(0))

        print('Stage 4')

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

        print('Stage 5')

        # If the seats are available, submit the booking
        for ticket in self.Tickets:
            self.Viewing.submitTicket(ticket, self.Customer)
            ticket.generateQR()

        print('Stage 6')

        # self.confirmBooking()
        return True

    def confirmBooking(self) -> None:

        # Send Email
        msg = MIMEMultipart()
        msg['From'] = ''
        msg['To'] = self.Customer.getEmail()
        msg['Subject'] = 'Booking Confirmation'

        # Renders the email body from Jinja template
        emailBody = render_template('confEmailBody.html', booking=self)
        msg.attach(MIMEText(emailBody, 'html'))


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
        self.allBookings = dict()

    def newBooking(self, ID: str, ViewingObj: object) -> int:
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

    def removeBooking(self, index: int) -> None:
        """
        Removes a booking from the collection of bookings.

        Args:
            index (int): The index of the booking to be removed.
        """

        self.allBookings.pop(index, None)

    def getBookingByID(self, index: int) -> object:
        """
        Retrieves a booking from the collection of bookings based on its ID.

        Args:
            index (int): The ID of the booking to be retrieved.

        Returns:
            object: The booking object with the specified ID, or None if it doesn't exist.
        """

        if index in self.allBookings:
            return self.allBookings[index]
        else:
            return None
