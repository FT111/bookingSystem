from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import qrcode
import uuid
from flask import render_template

class TicketTypes:
    def __init__(self, Database) -> None:
        self.allTypes = list()
        self.Database = Database

    def getTypes(self) -> tuple:
        self.typesTuple = self.Database.getTicketTypes()
        self.allTypes = []
        for type in self.typesTuple:
            self.allTypes.append({ 'ID':type[0],
                                'Name': type[1], 
                                'Price': type[2] })
        return self.allTypes

###
### Container pattern heirachy: Bookings -> Booking -> Ticket
###

class Ticket:
    Database = None

    @classmethod
    def setDatabase(cls, Database:object) -> None:
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
    TicketTypes = None
    
    @classmethod
    def setTicketTypes(cls, TicketTypes:object) -> None:
        cls.TicketTypes = TicketTypes

    def __init__(self, Database:object, ViewingObj:object) -> None:
        self.Database = Database
        self.Customer = None
        self.Viewing = ViewingObj
        self.Tickets = []
        self.bookingID = str(uuid.uuid4().int)
        self.selectedSeats = []

    def getID(self) -> str:
        return self.bookingID

    def addTicket(self, ticket:object) -> None:
        self.Tickets.append(ticket)
    
    def removeTicket(self, ticket:object) -> None:
        self.Tickets.remove(ticket)

    def addSeat(self, seat:str) -> bool:
        # Validates that the seat is an available, existing seat
        if seat in self.Viewing.getUnavailableSeats() or seat in self.Viewing.getReservedSeats() or seat not in self.Viewing.getSeatNames():
            return False
        
        self.selectedSeats.append(seat)
        return True
    
    def removeSeat(self, seat:str) -> bool:
        if seat not in self.selectedSeats:
            return False
        self.selectedSeats.remove(seat)
    
    def resetSeats(self) -> None:
        self.selectedSeats = []

    def getSelectedSeats(self):
        return self.selectedSeats
    

    def removeTicketOfType(self, ticketType:str) -> None:
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
    
    def setCustomer(self, Customer:object) -> None:
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
        seats = list(seats)

        # Validate that the booking has tickets
        if len(self.Tickets) == 0:
            return False

        # Handles assigning seats to tickets if they are not already assigned
        if seats is not None:
            if len(seats) != len(self.Tickets):
                return False
            
            for ticket in self.Tickets:
                ticket.setSeatLocation(seats.pop(0))
        
        for ticket in self.Tickets:
            if ticket.getSeatLocation() in unavailableSeats or ticket.getSeatLocation() not in self.Viewing.getSeatNames():
                self.Tickets = []
                return False

        # If the seats are available, submit the booking
        for ticket in self.Tickets:
            self.Viewing.submitTicket(ticket, self.Customer)
            ticket.generateQR()
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

    def __init__(self, Database:object) -> None:
        self.Database = Database
        self.allBookings = dict()

    def newBooking(self, ID:str, ViewingObj:object) -> int:
        newBooking = Booking(self.Database, ViewingObj)
        self.allBookings[ID] = newBooking

        return newBooking

    def removeBooking(self, index:int) -> None:
        self.allBookings.pop(index, None)

    def getBookingByID(self, index:int) -> object:
        if index in self.allBookings:
            return self.allBookings[index]
        else:
            return None