
const submitBooking = () => {
    let btnLoadingClasses = ['animate-pulse', 'cursor-not-allowed', 'pointer-events-none', 'bg-gray-300', 'text-gray-800', 'hover:bg-gray-300','hover:text-gray-300', 'border-gray-300', 'shadow-none']
    let continueBtn = document.getElementById('continueBtn');

    continueBtn.classList.add(...btnLoadingClasses);

    continueBtn.innerHTML = `Submit
    <span class="loading loading-spinner loading-md"></span>
    `;

    let response = fetch('/api/bookings/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json()).then(data => {
        console.log(data);
        if (data.status === "200") {
            continueBtn.classList.remove(...btnLoadingClasses);
            continueBtn.classList.add('bg-green-500', 'shadow-md', 'scale-105', 'border-green-500','hover:bg-green-500','hover:text-black','hover:border-green-500', 'outline-none', 'pointer-events-none','cursor-normal', 'text-black');
            continueBtn.innerHTML = `Success
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>

            `;


            setTimeout(() => {
                document.getElementById('confirmationScreen').classList.remove('hidden', 'opacity-0', 'bg-base-100/0');
                document.getElementById('confirmationScreen').classList.add('bg-base-100/60', 'opacity-100');

                setTimeout(() => {
                    window.location.href = '/dashboard'
                }, 500);
            }, 1000);
        } else {
            newError('Error submitting booking');
            document.getElementById('continueBtn').classList.remove(...btnLoadingClasses);
        }
    })
}