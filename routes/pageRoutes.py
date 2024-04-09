from flask import Flask, render_template, request, redirect, url_for, Response, session, Blueprint
from datetime import datetime
from routes.sharedInstances import bs
from routes.webAppFunctions import getSession

# Defines the blueprint for use in the main file
pageRoutes = Blueprint('pageRoutes', __name__)


@pageRoutes.route('/dashboard')
def index():
    allStats = bs.Viewings.getStats()
    customers = bs.Customers.getAllCustomerInfoFromDB('firstName','Surname', 'emailAddress', 'phoneNumber')

    return render_template('dashboard.html', stats=allStats, customers=customers)


@pageRoutes.route('/viewings/manage')
def manageViewings():
    viewings = bs.Viewings.getAllViewingsAsList()
    return render_template('viewings/manage.html', viewings=viewings)


# Shows the upcoming viewings to the user and allows selection
@pageRoutes.route('/booking/new')
def viewingsPage():
    viewings = bs.Viewings.getUpcomingViewingsAsList()

    return render_template('bookings/bookingViewingSelection.html', viewings=viewings)


# Allows the user to select the number of tickets they want to purchase
@pageRoutes.route('/booking/tickets')
def newBookingPage():
    sessionID = getSession()
    try:
        currentBooking = bs.Bookings.getBookingByID(sessionID)
        currentViewing = currentBooking.getViewing()
    except AttributeError:
        return redirect(url_for('pageRoutes.viewingsPage'))

    ticketTypes = bs.TicketTypes.getTypes()
    ticketCounts = currentBooking.getTicketCountPerType()
    ticketSum = sum(ticketCounts.values())
    priceSum = currentBooking.getPriceSum()

    return render_template('bookings/bookingNew.html', booking=currentBooking, ticketSum=ticketSum, priceSum=priceSum,
                           ticketCounts=ticketCounts, viewing=currentViewing, ticketTypes=ticketTypes)


# Allows the user to select the seats they want to book
@pageRoutes.route('/booking/seats')
def chooseSeatsPage():
    sessionID = getSession()

    # Fetches the current user's booking and validates that it exists
    booking = bs.Bookings.getBookingByID(sessionID)
    if booking is None:
        return redirect(url_for('pageRoutes.viewingsPage'))

    maxSeats = len(booking.getTickets())
    if maxSeats <= 0:  # Ensures that the user has selected at least one ticket
        return redirect(url_for('pageRoutes.newBookingPage'))

    # Retrieve the viewing object from the current user's booking
    viewing = booking.getViewing()

    seatNames = viewing.getSeatNames()
    reservedNames = viewing.getReservedSeats()
    unavailableNames = viewing.getUnavailableSeats()
    seatsPerRow = viewing.getRowLength()
    viewingName = viewing.getName()
    bookingID = booking.getID()

    return render_template('bookings/seatSelector.html', bookingID=bookingID, viewingName=viewingName, seatNames=seatNames,
                           reservedSeats=reservedNames, unavailableSeats=unavailableNames, seatsPerRow=seatsPerRow,
                           maxSeats=maxSeats)


@pageRoutes.route('/booking/summary')
def bookingSummary():
    sessionID = getSession()
    try:
        currentBooking = bs.Bookings.getBookingByID(sessionID)
        currentViewing = currentBooking.getViewing()
    except AttributeError:
        return redirect(url_for('pageRoutes.viewingsPage'))

    tickets = currentBooking.getTickets()
    seats = currentBooking.getSelectedSeats()
    if len(tickets) <= 0:
        return redirect(url_for('pageRoutes.newBookingPage'))

    if len(seats) != len(tickets):
        return redirect(url_for('pageRoutes.chooseSeatsPage'))

    ticketTypes = bs.TicketTypes.getTypes()
    ticketCounts = currentBooking.getTicketCountPerType()
    print(ticketCounts)
    ticketSum = sum(ticketCounts.values())
    priceSum = currentBooking.getPriceSum()
    tickets = currentBooking.getTickets()

    return render_template('bookings/bookingSummary.html', booking=currentBooking, tickets=tickets, ticketSum=ticketSum,
                           priceSum=priceSum, ticketCounts=ticketCounts, viewing=currentViewing,
                           ticketTypes=ticketTypes)



@pageRoutes.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res