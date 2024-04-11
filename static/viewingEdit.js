

const toggleUnavailableSeat = (seatID) => {
    const index = unavailableSeats.indexOf(seatID);
    if (index !== -1) {
        unavailableSeats.splice(index, 1);
        console.log('deleted');
    } else {
        unavailableSeats.push(seatID);
    }
    console.log(unavailableSeats);
}
const updateViewing = async () => {
    const response = await fetch(`/api/viewings/editAvailableSeats/${viewingID}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            unavailableSeats: unavailableSeats
        })
    });

    if (response.status === 200) {
        newSuccessAlert('Viewing updated successfully');
        window.location.reload();
    } else {
        newError('Failed to update viewing');
    }
}

