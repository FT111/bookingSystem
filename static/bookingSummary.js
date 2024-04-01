
const submitBooking = () => {
    let response = fetch('/api/bookings/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json()).then(data => {
        console.log(data);
        if (data.status === "200") {
            window.location.href = '/booking/new';
        } else {
            newError('Error submitting booking');
        }
    })
}