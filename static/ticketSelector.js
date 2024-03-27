let selectedClasses = ['shadow-md', 'scale-[1.02]', 'outline', 'outline-1', 'outline-sky-800'];

if (window.screen.width < 800) {
    selectedClasses = [...selectedClasses, 'rounded-md'];
}

const incrementTicket = (ticketType, Price) => {
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
    priceSum += Price;

    checkTotal();
    });

};

const decrementTicket = (ticketType, Price) => {
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
    priceSum -= Price;

    checkTotal();

    });
}

const checkTotal = () => {

    
    for (let i = 0; i < ticketTypes.length; i++) {
        const ticket = document.getElementById(ticketTypes[i].ID);
        if (ticket.value != 0) {
            // 'outline', 'outline-1', 'outline-sky-700'
            document.getElementById(ticketTypes[i].ID + 'Card').classList.add(...selectedClasses);
        } else {
            document.getElementById(ticketTypes[i].ID + 'Card').classList.remove(...selectedClasses);
        }
    }
    
    if (ticketSum == 0) {
        document.getElementById('continueBtn').disabled = true;
        document.getElementById('continueTooltip').classList.add('tooltip', 'tooltip-left');
    } else {
        document.getElementById('continueBtn').disabled = false;
        document.getElementById('continueTooltip').classList.remove('tooltip', 'tooltip-left');
    }

    document.getElementById('priceSumIndicator').innerHTML = formatter.format(priceSum);
}

document.addEventListener('DOMContentLoaded', () => {

    checkTotal();   
});