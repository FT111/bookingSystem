from flask import Flask, render_template, request, redirect, url_for, Response, session, Blueprint
import json
import os

from routes.sharedInstances import bs
from routes.webAppFunctions import getSession

# Defines the blueprint for use in the main file
apiRoutes = Blueprint('apiRoutes', __name__)


@apiRoutes.route('/tickets/checkQR', methods=['POST'])
def checkTicket():
    pass


@apiRoutes.route('/viewings/getViewingDataByIDs', methods=['POST'])
def getViewingData():
    selectedViewings = (bs.Viewings.getStoredViewingByID(viewingID) for viewingID in request.json.get('viewingIDs'))


@apiRoutes.route('/customers/getAll', methods=['POST'])
def getAllCustomers():
    customers = bs.Customers.getAllCustomerInfoFromDB('firstName', 'Surname', 'emailAddress', 'phoneNumber', 'ID')

    print(customers)
    customers = json.dumps(customers)

    return Response(f'{{"body": {customers}}}', status=200, mimetype='application/json')


@apiRoutes.route('/customers/new', methods=['POST'])
def newCustomer():
    print(request.json)
    requiredFields = ['Name', 'Email', 'phoneNumber']
    missingFields = [field for field in requiredFields if field not in request.json.keys()]

    if missingFields:
        return Response(f'{{"body": "Missing required fields: {", ".join(missingFields)}"}}', status=400,
                        mimetype='application/json')

    splitName = request.json.get('Name').split(' ')
    firstName = splitName[0]
    surname = splitName[len(splitName) - 1]

    newCust = bs.Customers.newCustomer(firstName=firstName,
                                       surname=surname,
                                       email=request.json.get('Email'),
                                       phoneNumber=request.json.get('phoneNumber'))
    if newCust is None:
        return Response('{"body": "Error creating customer"}', status=400, mimetype='application/json')
    newCust.submitToDB()

    if request.json.get('addToBooking'):
        sessionID = getSession()
        booking = bs.Bookings.getBookingByID(sessionID)
        booking.setCustomer(newCust)

    return Response(f'{{"body": "{str(newCust.getID())}"}}', status=200, mimetype='application/json')


@apiRoutes.route('/bookings/startNewBooking', methods=['POST'])
def startNewBooking():
    sessionID = getSession()

    requestJSON = request.get_json()
    viewing = bs.Viewings.getStoredViewingByID(requestJSON.get('viewingID'))
    bs.Bookings.newBooking(sessionID, viewing)
    return json.dumps({'status': '200'})


# @app.route('/bookings/addCustomer', methods=['POST'])
# def newBooking():
#     sessionID = getSession()

#     customer = bs.Customers.newCustomer(firstName=request.json.get('firstName'), Surname=request.json.get('surname'), email=request.json.get('email'))
#     booking = bs.Bookings.getBookingByID(sessionID)
#     booking.setCustomer(customer)

#     return json.dumps({'status': '200'})

@apiRoutes.route('/bookings/addTicket', methods=['POST'])
def addSeat():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    ticket = bs.Ticket(request.json.get('ticketType'))
    confirmation = booking.addTicket(ticket)
    booking.resetSeats()
    if not confirmation:
        return Response('{"body": "Not enough tickets remaining"}', status=400, mimetype='application/json')
    return json.dumps({"status": "200", "body": ticket.getID()})


@apiRoutes.route('/bookings/removeTicket', methods=['POST'])
def removeTicket():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    print(request.json.get('ticketType'))
    booking.removeTicketOfType(request.json.get('ticketType'))
    booking.resetSeats()
    return json.dumps({'status': '200'})


@apiRoutes.route('/bookings/addSeat', methods=['POST'])
def setSeats():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    seatLocation = request.json.get('seat')
    booking.addSeat(seatLocation)
    return json.dumps({'status': '200'})


@apiRoutes.route('/bookings/removeSeat', methods=['POST'])
def removeSeat():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    seatLocation = request.json.get('seat')
    booking.removeSeat(seatLocation)
    return json.dumps({'status': '200'})


@apiRoutes.route('/bookings/getBookingInfo', methods=['POST'])
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


@apiRoutes.route('/bookings/addCustomer', methods=['POST'])
def addCustomer():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    customer = bs.Customers.getStoredCustomer(request.json.get('customerID'))

    if not customer:
        customer = bs.Customer(id=request.json.get('customerID'))
        bs.Customers.addCustomer(customer)

    booking.setCustomer(customer)
    return json.dumps({'status': '200'})


@apiRoutes.route('/bookings/submit', methods=['POST'])
def submitBooking():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    seatLocations = booking.getSelectedSeats()
    booking.Submit(seatLocations)

    return Response('{"status": "200"}', status=200, mimetype='application/json')


# Test Endpoints
# vvvvvvvvvvvvvv

@apiRoutes.route('/testEmail')
def testEmail():
    return render_template('./confEmailBody.html', booking=None)


@apiRoutes.route('/testEndpoint')
def testEndpoint():
    sessionID = getSession()

    bs.Viewings.getAllViewingsFromDB()
    customer = bs.Customers.newCustomer(firstName='Test',
                                        surname='Customer',
                                        email='freddiejljtaylor+test2@gmail.com',
                                        phoneNumber='07776159389')
    booking = bs.Bookings.newBooking(sessionID, bs.Viewings.getStoredViewingByID(1))
    ticket = bs.Ticket(2)
    ticket2 = bs.Ticket(1)
    booking.setCustomer(customer)

    # new function
    bookingRetrieved = bs.Bookings.getBookingByID(sessionID)
    bookingRetrieved.addTicket(ticket)
    bookingRetrieved.addTicket(ticket2)
    bookingRetrieved.Submit(('A1', 'A2'))
    os.system(f'open {ticket.getQR()}')
    os.system(f'open {ticket2.getQR()}')

    return '200'


@apiRoutes.route('/testEndpoint2')
def testEndpoint2():
    print(session['uuid'])
    return str(session['uuid'])