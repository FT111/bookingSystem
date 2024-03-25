let ticketSum = 0;

const incrementTicket = (ticketType) => {
    const ticket = document.getElementById(ticketType);
    fetch('/api/bookings/addTicket', {
        method: 'POST',
        body: JSON.stringify({ticketType: ticketType}),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(() => {

    ticket.value = parseInt(ticket.value) + 1;
    ticketSum++;
    checkTotal();
    });

};

const decrementTicket = (ticketType) => {
    if (document.getElementById(ticketType).value === '0') {
        return;
    }
    const ticket = document.getElementById(ticketType);
    fetch('/api/bookings/removeTicket', {
        method: 'POST',
        body: JSON.stringify({ticketType: ticketType}),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(() => {
    ticket.value = parseInt(ticket.value) - 1;
    ticketSum--;
    checkTotal();

    });
}

const checkTotal = () => {
    
    if (ticketSum == 0) {
        document.getElementById('continueBtn').disabled = true;
    } else {
        document.getElementById('continueBtn').disabled = false;
    }
}


