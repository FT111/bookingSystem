let category = 'all';
let selectedViewing = null;

const getViewings = (event) => {
    category = event.target.value;
}

const getFilteredViewings = (viewings, category) => {
    this.filteredViewings = [];
    if (category === 'all') {
        return viewings;
    }

    viewings.forEach(viewing => {
        if (category === 'upcoming') {
            if (viewing['date'] >= Date.now()) {
                this.filteredViewings.push(viewing);
            }
        } else if (category === 'past') {
            if (viewing["date"] < Date.now()) {
                this.filteredViewings.push(viewing);
            }
        }
    })
}

const renderData = (viewings) => {
    let data = fetch('/api/viewings/getViewingDataByIDs', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(viewings)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
}