
const incrementTicket = (ticketID) => {
    const ticket = document.getElementById(ticketID);
    fetch('/api/bookings/addTicket', {
        method: 'POST',
        body: JSON.stringify({ticketID: ticketID}),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(() => {

    ticket.value = parseInt(ticket.value) + 1;
    });
    // updateTotal();
};
