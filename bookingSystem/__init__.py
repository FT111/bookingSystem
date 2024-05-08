"""
This package handles the logic for a booking system.
All objects are UI agnostic.
The database is safe to use in a multi-threaded environment.
"""

from .databaseFuncs import DatabaseConnection, Database
from .customerFuncs import Customer, Customers
from .viewingFuncs import Viewing, Viewings
from .bookingFuncs import Ticket, Booking, Bookings, TicketTypes
from .emailFuncs import EmailFuncs


class BookingSystem:
    """
           Initialises the BookingSystem with a database connection and sets up the main entities.

           Assigns all instanced entities to the database connection.

           :param dbPath: The path to the SQLite database file.

           :param emailAddress: The email address the system will use to send emails.
           :param emailAuth: The password for the email address.
           :param emailProvider: The email provider's SMTP server.
           :param emailPort: The email provider's SMTP port.

           :param hostName: Optional - The hostname of the server. Used for generating ticket QR codes.

    """

    def __init__(self, dbPath: str, emailAddress: str = None, emailAuth: str = None,
                 emailProvider: str = None, emailPort: int = None, hostName: str = None) -> None:
        self.Ticket = Ticket
        self.Booking = Booking
        self.Viewing = Viewing
        self.Customer = Customer

        self.DATABASE_CONNECTION = DatabaseConnection(dbPath)  # Thread safe SQLite connection handler
        self.Database = Database(self.DATABASE_CONNECTION)  # Primary database functions

        self.Bookings = Bookings(self.Database)  # Booking management container
        self.Viewings = Viewings(self.Database)  # Viewing management container
        self.Customers = Customers(self.Database)  # Customer management container
        self.EmailFuncs = EmailFuncs(emailAddress, emailAuth, emailProvider, emailPort)  # Email functions
        self.TicketTypes = TicketTypes(self.Database, self.Viewings)  # Ticket types

        # Dependency injection using class methods
        Booking.setTicketTypes(self.TicketTypes)
        Booking.setEmailFuncs(self.EmailFuncs)
        Viewings.setTicketTypes(self.TicketTypes)
        Ticket.setDatabase(self.Database)
        if hostName:
            Ticket.setHostName(hostName)

        Customer.setDatabase(self.Database)
