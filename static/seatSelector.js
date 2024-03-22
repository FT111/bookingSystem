let selectedSeats = [];
let seatsDisabled = false;
let badgeClasses = 'badge badge-lg badge-neutral gap-2 justify-center border border-neutral-200 hover:bg-red-300 hover:border-red-300 hover:text-neutral-900 focus:outline-none focus:ring focus:ring-neutral-200 focus:ring-offset-2 focus:ring-offset-neutral-100 transition ease-in-out duration-150';

const removeSeat = (seat) => {
    if (seatsDisabled) {
        enableAllSeats();
        seatsDisabled = false;
    }
    selectedSeats = selectedSeats.filter((s) => s !== seat);
    sessionStorage.setItem('selectedSeats', JSON.stringify(selectedSeats));
    document.getElementById(seat).checked = false;
    refreshSeatIndicator();
};

const disableAllSeats = () => {
    const Seats = document.getElementsByClassName('Seat');
    for (let i = 0; i < Seats.length; i++) {
        if (Seats[i].checked == false) {
            Seats[i].disabled = true;
            Seats[i].nextElementSibling.classList.add('opacity-75');
            document.getElementById('continueBtn').disabled = false;
            document.getElementById('continueTooltip').classList.remove('tooltip', 'tooltip-left');
        }
        ;
    }
    ;
};

const enableAllSeats = () => {
    const Seats = document.getElementsByClassName('Seat');
    for (let i = 0; i < Seats.length; i++) {
        Seats[i].disabled = false;
        Seats[i].nextElementSibling.classList.remove('opacity-75');
        document.getElementById('continueBtn').disabled = true;
        document.getElementById('continueTooltip').classList.add('tooltip', 'tooltip-left');
    }
    ;
};

const toggleSeat = (seat) => {
    console.log(seat);
    if (selectedSeats.includes(seat)) {
        removeSeat(seat);
    }
    else {
        selectedSeats.push(seat);
    }
    sessionStorage.setItem('selectedSeats', JSON.stringify(selectedSeats));
    refreshSeatIndicator();
};

const refreshSeatIndicator = () => {
    console.log(selectedSeats);
    const seatsRemainingIndicator = document.getElementById("seatsRemaining");
    seatsRemainingIndicator.innerHTML = (maxSeats - selectedSeats.length);
    const seatIndicator = document.getElementById("seatIndicator");
    let formattedSeats = [];
    for (let i = 0; i < selectedSeats.length; i++) {
        let seat = document.getElementById(selectedSeats[i]);
        if (seat.checked == false) {
            seat.checked = true;
        }
        formattedSeats[i] = `<button class="${badgeClasses}" onclick="removeSeat('${selectedSeats[i]}')">  <svg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' class='inline-block w-4 h-4 stroke-current'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M6 18L18 6M6 6l12 12'></path></svg> ${selectedSeats[i]}</button>`;
    }
    ;
    seatIndicator.innerHTML = 'Selected Seats: ' + formattedSeats.join(' ');
    if (seatsDisabled) {
        enableAllSeats();
    }
    ;
    if (selectedSeats.length === maxSeats) {
        disableAllSeats();
        seatsDisabled = true;
    }
    ;
};

window.onload = () => {
    if (sessionStorage.getItem('maxSeats')) {
        if (sessionStorage.getItem('viewing')!= null) {
            const lastViewing = JSON.parse(sessionStorage.getItem('viewing'));
            const lastMaxSeats = JSON.parse(sessionStorage.getItem('maxSeats'));
            if (lastMaxSeats != maxSeats || lastViewing != viewingName) {
                sessionStorage.setItem('maxSeats', JSON.stringify(maxSeats));
                sessionStorage.setItem('viewing', JSON.stringify(viewingName));
            }
            else {
                if (sessionStorage.getItem('selectedSeats')) {
                    selectedSeats = JSON.parse(sessionStorage.getItem('selectedSeats'));
                    refreshSeatIndicator();
                }
                else {
                    sessionStorage.setItem('selectedSeats', JSON.stringify(selectedSeats));
                }
                ;
        }
        ;
    }
}
    else {
        sessionStorage.setItem('maxSeats', JSON.stringify(maxSeats));
        sessionStorage.setItem('viewing', JSON.stringify(viewingName));
        
    }
    ;
};
