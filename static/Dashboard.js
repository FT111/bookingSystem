let category = 'all';
let selectedViewing = null;

const getViewings = (searchElement) => {
    category = searchElement.value;

    let url = '/api/viewings/getStats';

    if (category === 'upcoming' || category === 'past') {
        url = `/api/viewings/getStats/${category}`;
    } else if (category === 'specific') {
        document.getElementById('viewingSelector').style.display = 'block';
        if (selectedViewing === null) {
            return;
        }
        url = `/api/viewings/getSpecificStats/${selectedViewing}`;
    }


    let response = fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then((response) => response.json())
        .then((data) => {
            console.log(data);
            window.ticketChart.data.labels = data.body.ticketsPerViewing.map(row => row.viewingName);
            window.ticketChart.data.datasets[0].data = data.body.ticketsPerViewing.map(row => row.tickets);
            window.ticketChart.update();

            renderStats(data.body);
        })
        .catch((error) => {
            newError('Error :' + error);
        });
}

const renderStats = (stats) => {
    console.log(stats);
    let remainingSeatsSubtitle = `Most remaining: ${stats['mostRemaining']['viewingName']} - ${stats['mostRemaining']['remainingSeats']}`;

    document.getElementById('totalTickets').innerHTML = stats['totalTickets'];
    document.getElementById('totalRevenue').innerHTML = formatter.format(stats['totalRevenue']);
    document.getElementById('revenuePerViewing').innerHTML = stats['meanRevenuePerViewing'];
    document.getElementById('remainingSeats').innerHTML = stats['remainingSeats'];
    document.getElementById('remainingSeatsSub').innerHTML = remainingSeatsSubtitle;



}