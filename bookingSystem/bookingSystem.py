from bookingSystem.ViewingFuncs import Viewing, Viewings
from bookingSystem.BookingFuncs import Ticket, Booking, Bookings, TicketTypes
from bookingSystem.databaseFuncs import Database, DatabaseConnection
from bookingSystem.customerFuncs import Customer, Customers


class BookingSystem:

    def __init__(self, dbPath:str) -> None:
        self.Ticket = Ticket
        self.Booking = Booking
        self.Viewing = Viewing
        self.Customer = Customer

        # The composite pattern is needed to manage simultaneous Flask sessions
        self.DATABASE_CONNECTION = DatabaseConnection(dbPath) # Thread safe SQLite connection handler
        self.Database = Database(self.DATABASE_CONNECTION) # Primary database functions
        self.Bookings = Bookings(self.Database) # Booking management container
        self.Viewings = Viewings(self.Database) # Viewing management container
        self.Customers = Customers(self.Database) # Customer management container
        self.TicketTypes = TicketTypes(self.Database) # Ticket types

        Booking.setTicketTypes(self.TicketTypes)
        Ticket.setDatabase(self.Database)
        Customer.setDatabase(self.Database)
    

