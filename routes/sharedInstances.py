import os
import socket

import bookingSystem as bSystem
from dotenv import load_dotenv

load_dotenv('../instance/.env')

# Get the IP address of the host machine to format ticket's QR code
# Makes the ticket QR code accessible from the network
socketObj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketObj.connect(('192.255.255.255', 1))
IP = f'http://{socketObj.getsockname()[0]}:8000/api/tickets/validate'

# Checks if environment variables are set
try:
    # Load environment variables from .env file
    EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
    EMAIL_AUTH = os.environ['EMAIL_AUTH']
    EMAIL_PROVIDER = os.environ['EMAIL_PROVIDER']
    EMAIL_PORT = int(os.environ['EMAIL_PORT'])

    bs = bSystem.BookingSystem(dbPath='./instance/bookingDatabase.db',
                               emailAddress=EMAIL_ADDRESS,
                               emailAuth=EMAIL_AUTH,
                               emailProvider=EMAIL_PROVIDER,
                               emailPort=EMAIL_PORT,
                               hostName=IP)
except KeyError:
    bs = bSystem.BookingSystem(dbPath='./instance/bookingDatabase.db', hostName=IP)




