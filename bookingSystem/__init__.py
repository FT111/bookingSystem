"""
This package handles the logic for a booking system.
The database is safe to use in a multi-threaded environment.
"""

from .databaseFuncs import DatabaseConnection, Database
from .customerFuncs import Customer, Customers
from .viewingFuncs import Viewing, Viewings
from .bookingFuncs import Ticket, Booking, Bookings, TicketTypes


class BookingSystem:
    """
           Initialises the BookingSystem with a database connection and sets up the main entities.

           Assigns all instanced entities to the database connection.

           :param dbPath: The path to the SQLite database file.
    """

    def __init__(self, dbPath: str) -> None:
        self.Ticket = Ticket
        self.Booking = Booking
        self.Viewing = Viewing
        self.Customer = Customer

        # The composite pattern is needed to manage simultaneous Flask sessions
        self.DATABASE_CONNECTION = DatabaseConnection(dbPath)  # Thread safe SQLite connection handler
        self.Database = Database(self.DATABASE_CONNECTION)  # Primary database functions

        self.Bookings = Bookings(self.Database)  # Booking management container
        self.Viewings = Viewings(self.Database)  # Viewing management container
        self.Customers = Customers(self.Database)  # Customer management container
        self.TicketTypes = TicketTypes(self.Database)  # Ticket types

        Booking.setTicketTypes(self.TicketTypes)
        Ticket.setDatabase(self.Database)
        Customer.setDatabase(self.Database)
