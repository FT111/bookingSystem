from flask import Flask, render_template, request, redirect, url_for, Response, session
from flask_cors import CORS
import json
import random
import uuid
from bookingSystem import BookingSystem


bs = BookingSystem(dbPath='./database/bookingDatabase.db')
app = Flask(__name__)
app.secret_key = 'iuwderfipubwrvipervbijaenv'
CORS(app)

testViewing = bs.Viewings.newViewing('Test Viewing', '2023-10-10', 10, 20)
testBooking = bs.Bookings.newBooking('Test Customer', testViewing)

def getSession():
    if 'uuid' not in session:
        session['uuid'] = uuid.uuid4()
    return session['uuid']

@app.route('/')
def index():
    sessionID = getSession()

    return render_template('dashboard.html')

@app.route('/seatSelector')
def chooseSeats():
    sessionID = getSession()
    # unavailableNames = ['A9','A10','A11','A12','J1','J20']
    # unavailableNames += [f'{chr(ord("A") + i)}8' for i in range(10)]
    # unavailableNames += [f'{chr(ord("A") + i)}13' for i in range(10)]
    # reservedNames = ['A4','B7','C9','D12','E15','F18','G21','H15','B4','F5','F6','D15','D14','H10','J2','J3','B19','B18','E2']


    seatNames = testViewing.getSeatNames()
    reservedNames = []
    unavailableNames = []
    seatsPerRow = testViewing.getRowLength()
    viewingName = testViewing.Name

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

@app.route('/cdn/codes/<path:path>')
def returnCode(path):
    return app.send_static_file(f'./assets/qrCodes/{path}.png')


@app.route('/testEmail')
def testEmail():
    return render_template('./confEmailBody.html', booking=None)

@app.route('/testEndpoint')
def testEndpoint():
    sessionID = getSession()
    
    customer = bs.Customers.newCustomer(firstName='Test', Surname='Customer', email='freddiejljtaylor+test@gmail.com',)
    booking = bs.Bookings.newBooking(sessionID, customer, testViewing)
    ticket = bs.Ticket('A1', 'Adult')
    ticket2 = bs.Ticket('A2', 'Adult')
    bookingRetrived = bs.Bookings.getBooking(booking)
    bookingRetrived.addTicket(ticket)
    bookingRetrived.addTicket(ticket2)
    bookingRetrived.Submit()

    return '200'




@app.route('/testEndpoint2')
def testEndpoint2():
    print(session['uuid'])
    return str(session['uuid'])






if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
