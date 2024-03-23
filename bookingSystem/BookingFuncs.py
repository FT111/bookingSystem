from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import qrcode
import random
import uuid
import os
from flask import render_template

class TicketTypes:
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
                qr = ticket.generateQR()


        
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

    def getBookingByID(self, index:int) -> object:
        if index in self.allBookings:
            return self.allBookings[index]
        else:
            return None