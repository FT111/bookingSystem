
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
        document.getElementById('continueTooltip').classList.add('tooltip', 'tooltip-left');
    } else {
        document.getElementById('continueBtn').disabled = false;
        document.getElementById('continueTooltip').classList.remove('tooltip', 'tooltip-left');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    checkTotal();   
});