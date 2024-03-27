from flask import Flask, render_template, request, redirect, url_for, Response, session
from flask_cors import CORS
import json
import uuid
import os

from bookingSystem.bookingSystem import BookingSystem

bs = BookingSystem(dbPath='./database/bookingDatabase.db')
bs.Viewings.getAllViewingsFromDB()
app = Flask(__name__)
app.secret_key = 'eqrfvgkn=lqejkrnvw#c ( rtb&@/elgjkn$£;,sdcm/.jtfwq05d.@£y.`p3oi4jgp34jg3if2qjpfcvnqkalcs'
CORS(app)


testViewing = bs.Viewings.getStoredViewingByID(1)
testBooking = bs.Bookings.newBooking(str(uuid.uuid4()), testViewing)

# Fetches the session ID from the session cookies, if it doesn't exist it creates a new one
def getSession() -> str:
    if 'uuid' not in session:
        session['uuid'] = uuid.uuid4()
    return str(session['uuid'])

# Flow - viewingSelector -> newBooking -> seatSelector -> Summary -> --Submit--

# Pages Routes
# vvvvvvvvvvvv

@app.route('/dashboard')
def index():

    return render_template('dashboard.html')

# Shows the upcoming viewings to the user and allows selection
@app.route('/booking/new')
def viewingsPage():
    viewings = bs.Viewings.getUpcomingViewingsAsList()

    return render_template('viewings.html', viewings=viewings)

# Allows the user to select the number of tickets they want to purchase
@app.route('/booking/tickets')
def newBookingPage():
    sessionID = getSession()
    try:
        currentBooking = bs.Bookings.getBookingByID(sessionID)
        currentViewing = currentBooking.getViewing()
    except AttributeError:
        return redirect(url_for('viewingsPage'))

    ticketTypes = bs.TicketTypes.getTypes()
    ticketCounts = currentBooking.getTicketCountPerType()
    ticketSum = sum(ticketCounts.values())
    priceSum = currentBooking.getPriceSum()

    return render_template('newBooking.html', booking=currentBooking, ticketSum=ticketSum, priceSum=priceSum, ticketCounts=ticketCounts, viewing=currentViewing, ticketTypes=ticketTypes)

# Allows the user to select the seats they want to book
@app.route('/booking/seats')
def chooseSeatsPage():
    sessionID = getSession()

    # Fetches the current user's booking and validates that it exists
    booking = bs.Bookings.getBookingByID(sessionID)
    if booking is None:
        return redirect(url_for('viewingsPage'))
    

    maxSeats = len(booking.getTickets())
    if maxSeats <= 0: # Ensures that the user has selected at least one ticket
        return redirect(url_for('newBookingPage'))
    
    # Retrieve the viewing object from the current user's booking
    viewing = booking.getViewing()

    seatNames = viewing.getSeatNames()
    reservedNames = viewing.getReservedSeats()
    unavailableNames = viewing.getUnavailableSeats()
    seatsPerRow = viewing.getRowLength()
    viewingName = viewing.getName()


    return render_template('seatSelector.html', viewingName=viewingName, seatNames=seatNames, reservedSeats=reservedNames, unavailableSeats=unavailableNames, seatsPerRow=seatsPerRow, maxSeats=maxSeats)


@app.route('/booking/summary')
def bookingSummary():
    sessionID = getSession()
    try:
        currentBooking = bs.Bookings.getBookingByID(sessionID)
        currentViewing = currentBooking.getViewing()
    except AttributeError:
        return redirect(url_for('viewingsPage'))
    
    tickets = currentBooking.getTickets()
    seats = currentBooking.getSelectedSeats()
    if len(tickets) <= 0:
        return redirect(url_for('newBookingPage'))
    
    print(tickets)
    print(seats)
    if len(seats) != len(tickets):
        return redirect(url_for('chooseSeatsPage'))
    

    ticketTypes = bs.TicketTypes.getTypes()
    ticketCounts = currentBooking.getTicketCountPerType()
    ticketSum = sum(ticketCounts.values())
    priceSum = currentBooking.getPriceSum()
    tickets = currentBooking.getTickets()

    return render_template('bookingSummary.html', booking=currentBooking, tickets=tickets, ticketSum=ticketSum, priceSum=priceSum, ticketCounts=ticketCounts, viewing=currentViewing, ticketTypes=ticketTypes)


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
    booking.resetSeats()
    return json.dumps({'status': '200', 'ticketID': ticket.getID()})

@app.route('/api/bookings/removeTicket', methods=['POST'])
def removeTicket():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    print(request.json.get('ticketType'))
    booking.removeTicketOfType(request.json.get('ticketType'))
    booking.resetSeats()
    return json.dumps({'status': '200'})

@app.route('/api/bookings/addSeat', methods=['POST'])
def setSeats():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    seatLocation = request.json.get('seat')
    booking.addSeat(seatLocation)
    return json.dumps({'status': '200'})

@app.route('/api/bookings/removeSeat', methods=['POST'])
def removeSeat():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    seatLocation = request.json.get('seat')
    booking.removeSeat(seatLocation)
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
    ticket = bs.Ticket(2)
    ticket2 = bs.Ticket(1)
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
