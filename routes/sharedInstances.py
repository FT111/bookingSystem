import os
import bookingSystem as bSystem
from dotenv import load_dotenv

load_dotenv('../instance/.env')

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
                               emailPort=EMAIL_PORT)
except KeyError:
    raise Exception('Environment variables not set. Please check the .env file.')
    bs = bSystem.BookingSystem(dbPath='./instance/bookingDatabase.db')




