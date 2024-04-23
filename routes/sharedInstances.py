import os
import socket

import bookingSystem as bSystem
from dotenv import load_dotenv

load_dotenv('../instance/.env')


def getHostName():
    # Get the IP address of the host machine to format ticket's QR code
    # Makes the ticket QR code accessible from the network. Makes the system portable.
    # Would be removed in production - IP address would be hardcoded.
    socketObj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socketObj.connect(('192.255.255.255', 1))
    hostName = '127.0.0.1'
    # Gets the machine's various IP addresses and finds the most likely one for LAN.
    for IP in socketObj.getsockname():
        if '192' == str(IP)[:3] or '172' == str(IP)[:3]:
            hostName = IP

    return hostName


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
                               hostName=f'http://{getHostName()}:8000/api/tickets/validate')
except KeyError:
    # Configures the system to run without email functionality.
    bs = bSystem.BookingSystem(dbPath='./instance/bookingDatabase.db',
                               hostName=f'http://{getHostName()}:8000/api/tickets/validate')




