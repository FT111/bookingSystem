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
            renderStats(data);
        })
        .catch((error) => {
            newError('Error :' + error);
        });
}

const renderStats = (stats) => {
    document.getElementById('totalTickets').innerHTML = stats.totalTickets;
    document.getElementById('totalRevenue').innerHTML = formatter.format(stats.totalRevenue);
    document.getElementById('revenuePerViewing').innerHTML = stats.meanRevenuePerViewing;


}