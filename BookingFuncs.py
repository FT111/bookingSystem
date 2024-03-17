from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import qrcode
import random
from flask import render_template

class Prices:
    def __init__(self, Database) -> None:
        self.Prices = ()
        self.Database = Database

    def getPrices(self) -> tuple:
        self.Prices = self.Database.getPrices()
        return self.Prices

###
### Container pattern heirachy: Bookings -> Booking -> Ticket
###

class Ticket:
    Database = None

    @classmethod
    def setDatabase(cls, Database:object) -> None:
        cls.Database = Database

    def __init__(self, ticketType: str, seatLocation: str) -> None:
        self.id = 0
        self.ticketType = ticketType
        self.seatLocation = seatLocation
        self.qrCodeURL = None

        # Generates a unique ID and ensures it is not already in use
        while self.id is 0 or self.id in Ticket.Database.getRecords('Tickets', 'ticketID', f'ticketID = {self.id}'):
            self.id = random.randint(9**7, 9**10)
    

    
    def getID(self) -> int:
        return self.id

    def getTicketType(self) -> str:
        return self.ticketType
    
    def getSeatLocation(self) -> str:
        return self.seatLocation
    
    def setSeatLocation(self, seatLocation: str) -> bool:
        if seatLocation in self.Database.getUnavailableSeats(self.Viewing.viewingID) or seatLocation in self.Database.getReservedSeats(self.Viewing.viewingID):
            return False
        
        self.seatLocation = seatLocation
        return True
    
    def setTicketType(self, ticketType: str) -> None:
        self.ticketType = ticketType

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
        self.qrCodeURL = f'./static/assets/qrCodes/{self.id}.png'
        img.save(self.qrCodeURL)
        return self.qrCodeURL


class Booking:
    def __init__(self, Database:object, Customer:object, ViewingObj:object) -> None:
        self.Database = Database
        self.Customer = Customer
        self.Viewing = ViewingObj
        self.Tickets = []

    def addTicket(self, ticket:object) -> None:
        self.Tickets.append(ticket)
    
    def removeTicket(self, ticket:object) -> None:
        self.Tickets.remove(ticket)

    def getTickets(self) -> list:
        return self.Tickets
    
    def getCustomer(self) -> object:
        return self.Customer
    
    def Submit(self) -> bool:
        # Validate that the requested seats are available
        unavailableSeats = self.Database.getReservedSeats(self.Viewing.viewingID)
        unavailableSeats += self.Database.getUnavailableSeats(self.Viewing.viewingID)

        for ticket in self.Tickets:
            if ticket.getSeatLocation() in unavailableSeats:
                return False
        if len(self.Tickets) == 0:
            return False
        else:
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

    def newBooking(self, ID:str, Customer:object, ViewingObj:object) -> int:
        newBooking = Booking(self.Database, Customer, ViewingObj)
        self.allBookings[ID] = newBooking

        return ID

    def removeBooking(self, index:int) -> None:
        self.allBookings.pop(index, None)

    def getBooking(self, index:int) -> object:
        return self.allBookings[index]