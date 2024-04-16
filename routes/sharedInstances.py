import os
import bookingSystem as bSystem


bs = bSystem.BookingSystem(dbPath='./instance/bookingDatabase.db',
                           emailAddress=os.environ['EMAIL_ADDRESS'],
                           emailAuth=os.environ['EMAIL_AUTH'],
                           emailProvider=os.environ['EMAIL_PROVIDER'],
                           emailPort=int(os.environ['EMAIL_PORT']))


