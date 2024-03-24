from flask import Flask, render_template, request, redirect, url_for, Response, session
from flask_cors import CORS
import json
import random
import uuid
import os
import qrcode
from datetime import datetime

from bookingSystem.bookingSystem import BookingSystem

bs = BookingSystem(dbPath='./database/bookingDatabase.db')
app = Flask(__name__)
app.secret_key = 'eqrfvgkn=lqejkrnvw#c ( rtb&@/elgjkn$£;,sdcm/.jtfwq05d.@£y.`p3oi4jgp34jg3if2qjpfcvnqkalcs'
CORS(app)

testViewing = bs.Viewings.newViewing(Name='Test Viewing', DateTime=datetime(year=25,month=4,day=23,hour=17,minute=00,second=00), rowCount=10, seatsPerRow=20)
testBooking = bs.Bookings.newBooking(str(uuid.uuid4()), testViewing)

# Fetches the session ID from the session cookies, if it doesn't exist it creates a new one
def getSession() -> str:
    if 'uuid' not in session:
        session['uuid'] = uuid.uuid4()
    return str(session['uuid'])

# Flow - viewingSelector -> newBooking -> seatSelector -> Summary -> --Submit--

# Pages Routes
# vvvvvvvvvvvv

@app.route('/')
def index():
    sessionID = getSession()

    return render_template('dashboard.html')

@app.route('/booking/new')
def viewingsPage():
    sessionID = getSession()
    viewings = bs.Viewings.getUpcomingViewingsAsList()

    return render_template('viewings.html', viewings=viewings)

@app.route('/booking/tickets')
def newBookingPage():
    sessionID = getSession()
    try:
        currentBooking = bs.Bookings.getBookingByID(sessionID)
        currentViewing = currentBooking.getViewing()
    except AttributeError:
        return redirect(url_for('viewingsPage'))

    ticketTypes = bs.TicketTypes.getTypes()

    return render_template('newBooking.html', booking=currentBooking, viewing=currentViewing, ticketTypes=ticketTypes)

@app.route('/booking/seats')
def chooseSeatsPage():
    sessionID = getSession()
    # unavailableNames = ['A9','A10','A11','A12','J1','J20']
    # unavailableNames += [f'{chr(ord("A") + i)}8' for i in range(10)]
    # unavailableNames += [f'{chr(ord("A") + i)}13' for i in range(10)]
    # reservedNames = ['A4','B7','C9','D12','E15','F18','G21','H15','B4','F5','F6','D15','D14','H10','J2','J3','B19','B18','E2']


    # TODO: FIX SETTING BOOKING

    booking = bs.Bookings.getBookingByID(sessionID)

    if booking is None:
        return redirect(url_for('viewingsPage'))
    
    viewing = booking.getViewing()
    print(bs.Viewings.allViewings)
    # viewing = bs.Viewings.getAllViewingsFromDB()[0]
    seatNames = viewing.getSeatNames()
    reservedNames = []
    unavailableNames = []
    seatsPerRow = viewing.getRowLength()
    viewingName = viewing.getName()

    maxSeats = 5

    return render_template('seatSelector.html', viewingName=viewingName, seatNames=seatNames, reservedSeats=reservedNames, unavailableSeats=unavailableNames, seatsPerRow=seatsPerRow, maxSeats=maxSeats)

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res

# @app.route('/cdn/codes/<path:path>')
# def returnCode(path):
#     return app.send_file(f'../assets/qrCodes/{path}.png')

@app.route('/ticketCheck')
def scanTicket():
    return render_template('ticketCheck.html')


# API Endpoints
# vvvvvvvvvvvvv

@app.route('/api/tickets/checkQR', methods=['POST'])
def checkTicket():
    pass

@app.route('/api/bookings/startNewBooking', methods=['POST'])
def startNewBooking():
    sessionID = getSession()

    requestJSON = request.get_json()
    viewing = bs.Viewings.getStoredViewingByID(requestJSON.get('viewingID'))
    bs.Bookings.newBooking(sessionID, viewing)
    return json.dumps({'status': '200'})

@app.route('/api/bookings/addCustomer', methods=['POST'])
def newBooking():
    sessionID = getSession()

    customer = bs.Customers.newCustomer(firstName=request.json.get('firstName'), Surname=request.json.get('surname'), email=request.json.get('email'))
    booking = bs.Bookings.getBookingByID(sessionID)
    booking.setCustomer(customer)

    return json.dumps({'status': '200', 'customerID': customer.getID()})

@app.route('/api/bookings/addTicket', methods=['POST'])
def addSeat():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    ticket = bs.Ticket(request.json.get('ticketType'))
    booking.addTicket(ticket)
    return json.dumps({'status': '200', 'ticketID': ticket.getID()})

@app.route('/api/bookings/removeTicket', methods=['POST'])
def removeSeat():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    ticket = bs.Ticket.getTicketByID(request.json.get('ticketID'))
    booking.removeTicket(ticket)
    return json.dumps({'status': '200'})

@app.route('/api/bookings/getBookingInfo', methods=['POST'])
def getBookingInfo():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    customer = booking.getCustomer()
    viewing = booking.getViewing()
    customerInfo = {
        'firstName': customer.getFirstName(),
        'surname': customer.getSurname(),
        'email': customer.getEmail()
    }

    bookingInfo = {
        'bookingID': booking.getID(),
        'customer': customerInfo,
        'viewingID': booking.getViewing().getID(),
        'tickets': [ticket.getID() for ticket in booking.getTickets()]
    }

    viewingInfo = {
        'viewingID': viewing.getID(),
        'viewingName': viewing.getName(),
        'viewingDateTime': viewing.getDateTime().strftime('%Y-%m-%d %H:%M:%S'),
        'rowCount': viewing.getRowCount(),
        'seatsPerRow': viewing.getSeatsPerRow()
    }
    return json.dumps({'customer': customerInfo, 'booking': bookingInfo, 'viewing': viewingInfo})

@app.route('/api/bookings/submit', methods=['POST'])
def submitBooking():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    seatLocations = request.json.get('seats')
    booking.Submit(seatLocations)
    return json.dumps({'status': '200', 'bookingID': booking.getID()})


@app.route('/testEmail')
def testEmail():
    return render_template('./confEmailBody.html', booking=None)

@app.route('/testEndpoint')
def testEndpoint():
    sessionID = getSession()
    
    customer = bs.Customers.newCustomer(firstName='Test', Surname='Customer', email='freddiejljtaylor+test@gmail.com')
    booking = bs.Bookings.newBooking(sessionID, testViewing)
    ticket = bs.Ticket('Adult')
    ticket2 = bs.Ticket('Adult')
    booking.setCustomer(customer)
    

    # new function
    bookingRetrived = bs.Bookings.getBookingByID(sessionID)
    bookingRetrived.addTicket(ticket)
    bookingRetrived.addTicket(ticket2)
    bookingRetrived.Submit(('A1', 'A2'))
    os.system(f'open {ticket.getQR()}')
    os.system(f'open {ticket2.getQR()}')

    return '200'

@app.route('/testEndpoint2')
def testEndpoint2():
    print(session['uuid'])
    return str(session['uuid'])




if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
