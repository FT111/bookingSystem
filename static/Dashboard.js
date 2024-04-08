let category = 'all';
let selectedViewing = null;

let statsPage;
let usersPage;
let viewStatsLabel;
let viewUsersLabel;

let customerTable;
let customerTableHeader;

const getViewings = (searchElement=undefined, ID= undefined) => {
    let url = '/api/viewings/getStats';

    if (searchElement !== undefined) {
        category = searchElement.value;


        if (category !== 'specific') {
            closeViewings();
            resetCustomers();
        }

        if (category === 'upcoming' || category === 'past') {
            url = `/api/viewings/getStats/${category}`;
            console.log(url);

        } else if (category === 'specific') {

            let response = fetch('/api/viewings/getAll', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            }).then((response) => response.json())
                .then((data) => {
                    showViewings(data.body);
                })
                .catch((error) => {
                    newError('Error :' + error);
                });
        }} else {
            showCustomersForViewing(ID);
            url = `/api/viewings/getStats/viewing/${ID}`;
            [... document.getElementsByClassName('viewingButton')].forEach(element => {
                element.classList.remove('bg-secondary');
            });
            document.getElementById(ID).classList.add('bg-secondary');

        }

    console.log(url);

    let response = fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then((response) => response.json())
        .then((data) => {
            renderStats(data.body);
        })
        .catch((error) => {
            newError('Error :' + error);
        });
}

const closeViewings = () => {
    let viewingSelector = document.getElementById('viewingSelector');
    viewingSelector.classList.add('hidden', '-translate-y-1/2', 'opacity-0', 'blur-lg');

    let optionBar = document.getElementById('optionBar');
    optionBar.classList.remove('h-1/2')
    optionBar.classList.add('sticky', 'z-50')
}

const showViewings = (viewings) => {

    let viewingSelector = document.getElementById('viewingSelector');
    viewingSelector.innerHTML = '';
    viewingSelector.classList.remove('hidden');

    let optionBar = document.getElementById('optionBar');
    optionBar.classList.add('h-1/2', 'overflow-y-auto')
    optionBar.classList.remove('sticky', 'z-50')

    viewings.forEach(viewing => {
        viewingSelector.innerHTML += `
        <div class='tooltip tooltip-top' data-tip="${viewing.Date} ${viewing.Time}">
        <div id="${viewing.viewingID}" class="viewingButton badge badge-primary badge-lg p-5 text-white cursor-pointer hover:bg-secondary hover:border-secondary" onclick="getViewings(undefined, ${viewing.viewingID})">${viewing.Name}</div>
        </div>
        `
    });

    setTimeout(() => {
        viewingSelector.classList.remove('-translate-y-1/2', 'opacity-0', 'blur-lg');
    }, 1);
    
}

const renderStats = (stats) => {
    console.log(stats);
    let remainingSeatsSubtitle = `with <strong>${ stats['mostRemaining']['remainingSeats']}</strong> tickets unsold`;
    let mostPopularViewingSubtitle = `with <strong>${stats['mostPopularViewing']['tickets']}</strong> tickets sold`;
    let percentageSoldSubtitle = `<strong>${stats['percentageSold']}%</strong> of seats sold`;
    console.log(stats['percentageToMean'])

    // Ticket stats
    document.getElementById('totalTickets').innerHTML = stats['totalTickets'];
    document.getElementById('totalRevenue').innerHTML = formatter.format(stats['totalRevenue']);
    document.getElementById('revenuePerViewing').innerHTML = formatter.format(stats['meanRevenuePerViewing']);
    document.getElementById('revenuePerViewingSub').innerHTML = stats['percentageToMean']
    document.getElementById('remainingSeats').innerHTML = stats['remainingSeats'];
    document.getElementById('remainingSeatsSub').innerHTML = percentageSoldSubtitle;

    // Viewing stats
    document.getElementById('leastPopularViewing').innerHTML = stats['mostRemaining']['viewingName'];
    document.getElementById('leastPopularViewingSub').innerHTML = remainingSeatsSubtitle;
    document.getElementById('mostPopularViewing').innerHTML = stats['mostPopularViewing']['viewingName'];
    document.getElementById('mostPopularViewingSub').innerHTML = mostPopularViewingSubtitle;

    // Tickets per viewing chart
    window.revenueChart.data.labels = stats.statsPerViewing.map(row => row.viewingName);
    window.revenueChart.data.datasets[0].data = stats.statsPerViewing.map(row => row.revenue);

    window.ticketChart.data.labels = stats.statsPerViewing.map(row => row.viewingName);
    window.ticketChart.data.datasets[0].data = stats.statsPerViewing.map(row => row.tickets);
    window.ticketChart.update();
    window.revenueChart.update();

}

document.addEventListener('DOMContentLoaded', function () {
    statsPage = document.getElementById('statsPage');
    usersPage = document.getElementById('usersPage');
    viewStatsLabel = document.getElementById('viewStatsLabel');
    viewUsersLabel = document.getElementById('viewUsersLabel');  

    customerTable = document.getElementById('customerTable');
    customerTableHeader = document.getElementById('customerTableHeader');

    viewStatistics();
});

const viewStatistics = () => {
        
    usersPage.classList.add('hidden');
    statsPage.classList.remove('hidden');

    viewStatsLabel.classList.add('bg-primary');
    viewUsersLabel.classList.remove('bg-primary');

}

const viewUsers = () => {

    statsPage.classList.add('hidden');
    usersPage.classList.remove('hidden');

    viewUsersLabel.classList.add('bg-primary');
    viewStatsLabel.classList.remove('bg-primary');
}

const toggleView = () => {
    let radios = document.getElementsByName('viewOptions');
    let selectedView = 'statistics';

    radios.forEach(radio => {
        if (radio.checked) {
            selectedView = radio.value;
        }
    });

    if (selectedView === 'viewStats') {
        viewStatistics();
    }
    else {
        viewUsers();
    }
};

const showCustomersForViewing = (viewingID) => {

    response = fetch(`/api/bookings/getTicketsByViewing/${viewingID}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then((response) => response.json())
        .then((data) => {
            console.log(data.body);
            renderCustomers(data.body);
        })
        .catch((error) => {
            renderCustomers([])
        });
}

const renderCustomers = (customers) => {

    customerTableHeader.innerHTML = '';

    Object.keys(customers[0]).forEach(key => {
        if (key === 'Surname') {
            key = 'Name';
        } else if (key === 'firstName') {
            return;
        }
        customerTableHeader.innerHTML += `<th>${key}</th>`;
    });

    customerTable.innerHTML = '';

    customers.forEach(customer => {
        if (customer['firstName'] && customer['Surname']) {
            customer['Surname'] = customer['firstName'] + ' ' + customer['Surname'];
            delete customer['firstName'];
        }
        customerTable.innerHTML += `

        <tr>
            ${Object.keys(customer).map(key => { 
                return '<td>'+customer[key]+'</td>'
            }).join('')}
        </tr>
        
        `
    });
}

const resetCustomers = () => {
    renderCustomers(customers);
}
