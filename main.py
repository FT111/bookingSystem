from flask import Flask, render_template, request, redirect, url_for, Response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)




@app.route('/seatSelector')
def chooseSeats():
    maxSeats = request.args.get('maxSeats')
    seatsPerRow = request.args.get('seatsPerRow')
    rowCount = 10
    #with open("testSeats.json") as json_file:
    #    seats = json.load(json_file)

    unavailableNames = ['A9','A10','A11']
    reservedNames = ['A4','B7','C9','D12','E15','F18','G21','H15','B4']
    reservedIDs = []
    unavailableIDs = []


    for i in range(len(reservedNames)):
        seatID = (ord(reservedNames[i][0])-65)*int(seatsPerRow) + int(reservedNames[i][1:])
        reservedIDs.append(seatID)

    for i in range(len(unavailableNames)):
        seatID = (ord(unavailableNames[i][0])-65)*int(seatsPerRow) + int(unavailableNames[i][1:])
        unavailableIDs.append(seatID)
    
    print(reservedIDs)

    return render_template('seatSelector.html', rowCount=rowCount, reservedSeats=reservedIDs, unavailableSeats=unavailableIDs, seatsPerRow=seatsPerRow, maxSeats=maxSeats)


@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
