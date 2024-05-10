from flask import Flask, render_template, request, redirect, url_for, Response, session, Blueprint
import json
import os

import time
import random

from routes.pageRoutes import login as loginPage
from routes.sharedInstances import bs
from routes.authFuncs import getSession, authenticateSession, APIrequiresAuth, requiresAuth

# Defines the blueprint for use in the main file
apiRoutes = Blueprint('apiRoutes', __name__)


@apiRoutes.route('/login', methods=['POST'])
def login():
    username = request.form.get('name')
    password = request.form.get('password')

    if not authenticateSession(username, password):
        return loginPage(isRetry=True)

    if not session.get('loginRedirect'):
        return redirect('/dashboard')
    return redirect(session.get('loginRedirect'))


@apiRoutes.route('/tickets/validate/<int:ticketID>')
def checkTicket(ticketID):
    bs.Viewings.getAllViewingsFromDB()

    ticket = bs.Database.getTicketByID(ticketID)
    if not ticket:
        return render_template('ticketCheck.html', status='Invalid Ticket')

    viewing = bs.Viewings.formatViewing(vars(bs.Viewings.getStoredViewingByID(ticket[0][4])))

    return render_template('ticketCheck.html', status='Valid Ticket', ticket=ticket[0], viewing=viewing)


@apiRoutes.route('/viewings/manage/<int:viewingID>', methods=['DELETE'])
@APIrequiresAuth
def deleteViewing(viewingID):
    bs.Viewings.getAllViewingsFromDB()
    bs.Viewings.deleteViewing(viewingID)

    return Response('{"status": "200"}', status=200, mimetype='application/json')


@apiRoutes.route('/viewings/getViewingDataByIDs', methods=['POST'])
@APIrequiresAuth
def getViewingData():
    selectedViewings = (bs.Viewings.getStoredViewingByID(viewingID) for viewingID in request.json.get('viewingIDs'))


@apiRoutes.route('/viewings/getStats', methods=['POST'])
@APIrequiresAuth
def getAllStats():
    stats = bs.Viewings.getStats()
    return Response(f'{{"body": {json.dumps(stats)}}}', status=200, mimetype='application/json')


@apiRoutes.route('/viewings/getStats/upcoming', methods=['POST'])
@APIrequiresAuth
def getUpcomingStats():
    stats = bs.Viewings.getStats(timePeriod='upcoming')
    return Response(f'{{"body": {json.dumps(stats)}}}', status=200, mimetype='application/json')


@apiRoutes.route('/viewings/getStats/past', methods=['POST'])
@APIrequiresAuth
def getPastStats():
    stats = bs.Viewings.getStats(timePeriod='past')
    return Response(f'{{"body": {json.dumps(stats)}}}', status=200, mimetype='application/json')


@apiRoutes.route('/viewings/getStats/viewing/<int:viewingID>', methods=['POST'])
@APIrequiresAuth
def getSpecificStats(viewingID):
    stats = bs.Viewings.getStats(viewingID=viewingID)
    return Response(f'{{"body": {json.dumps(stats)}}}', status=200, mimetype='application/json')


@apiRoutes.route('/viewings/editAvailableSeats/<int:viewingID>', methods=['POST'])
@APIrequiresAuth
def editAvailableSeats(viewingID):
    viewing = bs.Viewings.getStoredViewingByID(viewingID)

    # Ensures the process is completed
    if viewing.setUnavailableSeats(request.json.get('unavailableSeats')):
        return Response('{"status": "200"}', status=200, mimetype='application/json')
    else:
        return Response('{"status": "400"}', status=400, mimetype='application/json')


@apiRoutes.route('/viewings/submit', methods=['POST'])
@APIrequiresAuth
def newViewing():
    # Validation
    requiredFields = ['viewingName', 'Date', 'Time', 'rowCount', 'seatsPerRow']
    missingFields = [field for field in requiredFields if field not in request.form.keys()]

    if missingFields:
        return Response(f'{{"body": "Missing required fields: {", ".join(missingFields)}"}}', status=400,
                        mimetype='application/json')

    try:
        viewing = bs.Viewings.newViewing(request.form.get('viewingName'),
                                         request.form.get('Date'),
                                         request.form.get('Time'),
                                         request.form.get('rowCount'),
                                         request.form.get('seatsPerRow'),
                                         request.form.get('Banner') if 'Banner' in request.form.keys() else None,
                                         request.form.get('Description') if 'Description' in request.form.keys() else None,
                                         )
    except ValueError as error:
        return redirect('/viewings/manage')

    return redirect(f'/viewings/edit/{viewing.getID()}')


@apiRoutes.route('/viewings/getAll', methods=['POST'])
@APIrequiresAuth
def getAllViewings():
    viewings = bs.Viewings.getAllViewingsAsList()
    return Response(f'{{"body": {json.dumps(viewings)}}}', status=200, mimetype='application/json')


@apiRoutes.route('/customers/getAll', methods=['POST'])
@APIrequiresAuth
def getAllCustomers():
    customers = bs.Customers.getAllCustomerInfoFromDB('firstName', 'Surname', 'emailAddress', 'phoneNumber', 'ID')

    customers = json.dumps(customers)

    return Response(f'{{"body": {customers}}}', status=200, mimetype='application/json')


@apiRoutes.route('/bookings/getTicketsByViewing/<int:viewingID>', methods=['POST'])
@APIrequiresAuth
def getCustomersByViewing(viewingID):
    customers = bs.Customers.getAllCustomerInfoFromDB('firstName', 'Surname', 'emailAddress', 'phoneNumber', 'ID')
    customerDictByID = {customer['ID']: customer for customer in customers}
    tickets = bs.Viewings.getStoredViewingByID(viewingID).getTicketInfo()
    ticketsDictByID = {ticket['TicketID']: ticket for ticket in tickets}

    for ticket in ticketsDictByID.values():
        if ticket['CustomerID'] in customerDictByID.keys():
            ticketsDictByID[ticket['TicketID']] = {**ticket, **customerDictByID[ticket['CustomerID']]}

    ticketList = list(ticketsDictByID.values())

    return Response(f'{{"body": {json.dumps(ticketList)}}}', status=200, mimetype='application/json')


@apiRoutes.route('/customers/new', methods=['POST'])
@APIrequiresAuth
def newCustomer():
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
@APIrequiresAuth
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
@APIrequiresAuth
def addSeat():
    sessionID = getSession()
    booking = bs.Bookings.getBookingByID(sessionID)

    ticketPrice = bs.TicketTypes.getTypePriceForViewing(booking.getViewing().getID(), request.json.get('ticketType'))
    ticket = bs.Ticket(request.json.get('ticketType'), price=ticketPrice)

    confirmation = booking.addTicket(ticket)
    booking.resetSeats()
    if not confirmation:
        return Response('{"body": "Not enough tickets remaining"}', status=403, mimetype='application/json')
    return json.dumps({"status": "200", "body": ticket.getID()})


@apiRoutes.route('/bookings/removeTicket', methods=['POST'])
@APIrequiresAuth
def removeTicket():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    booking.removeTicketOfType(request.json.get('ticketType'))
    booking.resetSeats()
    return json.dumps({'status': '200'})


@apiRoutes.route('/bookings/addSeat', methods=['POST'])
@APIrequiresAuth
def setSeats():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    seatLocation = request.json.get('seat')
    booking.addSeat(seatLocation)
    return json.dumps({'status': '200'})


@apiRoutes.route('/bookings/removeSeat', methods=['POST'])
@APIrequiresAuth
def removeSeat():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    seatLocation = request.json.get('seat')
    booking.removeSeat(seatLocation)
    return json.dumps({'status': '200'})


@apiRoutes.route('/bookings/getBookingInfo', methods=['POST'])
@APIrequiresAuth
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
@APIrequiresAuth
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
@APIrequiresAuth
def submitBooking():
    sessionID = getSession()

    booking = bs.Bookings.getBookingByID(sessionID)
    seatLocations = booking.getSelectedSeats()

    if not booking.Submit(seatLocations):
        return Response('{"status": "403"}', status=403, mimetype='application/json')

    bs.Bookings.removeBooking(sessionID)

    return Response('{"status": "200"}', status=200, mimetype='application/json')


# Test Endpoints
# vvvvvvvvvvvvvv


@apiRoutes.route('/testBooking')
def testBookings():
    sessionID = getSession()

    bs.Viewings.getAllViewingsFromDB()
    viewing = bs.Viewings.getAllViewingsFromDB()[1]
    booking = bs.Bookings.newBooking(sessionID, viewing)
    ticket = bs.Ticket(2)
    ticket2 = bs.Ticket(1)

    booking.addTicket(ticket)
    booking.addTicket(ticket2)

    booking.addSeat('C1')
    booking.addSeat('C2')

    return redirect('/booking/summary')

@apiRoutes.route('/bookings/testSubmit', methods=['POST'])
@APIrequiresAuth
def testSubmitBooking():
    sessionID = getSession()

    time.sleep(random.randint(1, 3))

    bs.Bookings.removeBooking(sessionID)

    return Response('{"status": "200"}', status=200, mimetype='application/json')



@apiRoutes.route('/testEmail')
def testEmail():
    sessionID = getSession()

    viewing = bs.Viewings.getAllViewingsAsList()[0]
    bookingObj = bs.Bookings.getBookingByID(sessionID)
    priceSum = bookingObj.getPriceSum()
    customer = bs.Customers.getCustomerByID(5)
    customer.Name = customer.getName()
    booking = vars(bookingObj)
    seats = bookingObj.getSelectedSeats()

    return render_template('./emailFormats/bookingConfirmed.html', viewing=viewing, seats=seats,
                           customer=customer, booking=booking, priceSum=priceSum)


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




