
const incrementTicket = (ticketID) => {
    const ticket = document.getElementById(ticketID);
    fetch('/api/bookings/addTicket')

    ticket.value = parseInt(ticket.value) + 1;
    updateTotal();
    }