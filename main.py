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
testBooking = bs.Bookings.newBooking(str(uuid.uuid4()),'Test Customer', testViewing)

# Fetches the session ID from the session cookies, if it doesn't exist it creates a new one
def getSession() -> str:
    if 'uuid' not in session:
        session['uuid'] = uuid.uuid4()
    return session['uuid']

# Flow - viewingSelector -> newBooking -> seatSelector -> Summary -> --Submit--

# Pages Routes
# vvvvvvvvvvvv

@app.route('/')
def index():
    sessionID = getSession()

    return render_template('dashboard.html')

@app.route('/viewingSelector')
def viewingsPage():
    sessionID = getSession()
    viewings = bs.Viewings.getUpcomingViewingsAsList()

    return render_template('viewings.html', viewings=viewings)

@app.route('/newBooking')
def newBookingPage():
    sessionID = getSession()
    if request.args.get('viewingID') is None:
        viewing = bs.Viewings.getStoredViewingByID(sessionID)
    else:
        viewing = bs.Viewings.getStoredViewingByID(request.args.get('viewingID'))

    return render_template('newBooking.html', viewing=viewing)

@app.route('/seatSelector')
def chooseSeatsPage():
    sessionID = getSession()
    # unavailableNames = ['A9','A10','A11','A12','J1','J20']
    # unavailableNames += [f'{chr(ord("A") + i)}8' for i in range(10)]
    # unavailableNames += [f'{chr(ord("A") + i)}13' for i in range(10)]
    # reservedNames = ['A4','B7','C9','D12','E15','F18','G21','H15','B4','F5','F6','D15','D14','H10','J2','J3','B19','B18','E2']

    viewing = bs.Viewings.getAllViewingsFromDB()[1]
    seatNames = viewing.getSeatNames()
    reservedNames = []
    unavailableNames = []
    seatsPerRow = viewing.getRowLength()
    viewingName = viewing.getName()

    maxSeats = 5

    return render_template('seatSelector.html', viewingName=viewingName, seatNames=seatNames, reservedSeats=reservedNames, unavailableSeats=unavailableNames, seatsPerRow=seatsPerRow, maxSeats=maxSeats)

@app.route('/seatSelector/getSelectedSeats', methods=['GET'])
def getSelectedSeats():
    pass

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
    # qrImage = request.files['body']
    # # ticket = bs.Ticket.getTicketByID(qrID)
    # if ticket is not None:
    #     return json.dumps({'status': 'Valid', 'seatLocation': ticket.getSeatLocation(), 'ticketType': ticket.getType()})
    # return json.dumps({'status': 'Invalid'})


@app.route('/api/bookings/newBooking', methods=['POST'])
def newBooking():
    sessionID = getSession()
    customer = bs.Customers.newCustomer(firstName=request.json.get('firstName'), Surname=request.json.get('surname'), email=request.json.get('email'))
    booking = bs.Bookings.newBooking(sessionID, customer, request.json.get('viewingID'))
    return json.dumps({'status': '200', 'bookingID': booking.getID()})

@app.route('/api/bookings/addSeat', methods=['POST'])
def addSeat():
    sessionID = getSession()
    booking = bs.Bookings.getBookingByID(sessionID)
    ticket = bs.Ticket(request.json.get('ticketType'), request.json.get('seatLocation'))
    booking.addTicket(ticket)
    return json.dumps({'status': '200', 'ticketID': ticket.getID()})

@app.route('/api/bookings/removeSeat', methods=['POST'])
def removeSeat():
    sessionID = getSession()
    booking = bs.Bookings.getBookingByID(sessionID)
    ticket = bs.Ticket.getTicketByID(request.json.get('ticketID'))
    booking.removeTicket(ticket)
    return json.dumps({'status': '200', 'ticketID': ticket.getID()})

@app.route('/api/bookings/getBookingInfo', methods=['GET'])
def getBookingInfo():
    sessionID = getSession()
    booking = bs.Bookings.getBookingByID(sessionID)
    customer = booking.getCustomer()
    customer_info = {
        'firstName': customer.getFirstName(),
        'surname': customer.getSurname(),
        'email': customer.getEmail()
    }

    booking_info = {
        'bookingID': booking.getID(),
        'customer': customer_info,
        'viewingID': booking.getViewing().getID(),
        'tickets': [ticket.getID() for ticket in booking.getTickets()]
    }

    return json.dumps({'customer': customer_info, 'booking': booking_info})

@app.route('/api/bookings/submit', methods=['GET'])
def submitBooking():
    sessionID = getSession()
    booking = bs.Bookings.getBookingByID(sessionID)
    booking.Submit()
    return json.dumps({'status': '200', 'bookingID': booking.getID()})


@app.route('/testEmail')
def testEmail():
    return render_template('./confEmailBody.html', booking=None)

@app.route('/testEndpoint')
def testEndpoint():
    sessionID = getSession()
    
    customer = bs.Customers.newCustomer(firstName='Test', Surname='Customer', email='freddiejljtaylor+test@gmail.com')
    booking = bs.Bookings.newBooking(sessionID, customer, testViewing)
    ticket = bs.Ticket('Adult', 'A1')
    ticket2 = bs.Ticket('Adult', 'A2')

    # new function
    bookingRetrived = bs.Bookings.getBookingByID(sessionID)
    bookingRetrived.addTicket(ticket)
    bookingRetrived.addTicket(ticket2)
    bookingRetrived.Submit()
    os.system(f'open {ticket.getQR()}')
    os.system(f'open {ticket2.getQR()}')

    return '200'

@app.route('/testEndpoint2')
def testEndpoint2():
    print(session['uuid'])
    return str(session['uuid'])




if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
