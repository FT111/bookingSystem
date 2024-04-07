
const submitBooking = () => {
    let response = fetch('/api/bookings/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json()).then(data => {
        console.log(data);
        if (data.status === "200") {
            document.getElementById('confirmationScreen').classList.remove('hidden', 'opacity-0', 'bg-base-100/0');
            document.getElementById('confirmationScreen').classList.add('bg-base-100', 'opacity-100');

            setTimeout(() => {
                window.location.href = '/dashboard'
            }, 500);
        } else {
            newError('Error submitting booking');
        }
    })
}