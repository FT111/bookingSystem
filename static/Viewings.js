let lastSearchedViewings = [];
` Example viewing data = let viewings = JSON.parse('[{"Banner": null, "Date": "2024-04-06", "Description": "Film. For testing.", "Name": "Test Film", "Time": "19:30:00", "viewingID": 1}, {"Banner": null, "Date": "2024-04-08", "Description": "Film. 2. For testing.", "Name": "Test Film: The Sequel", "Time": "20:15:00", "viewingID": 2}, {"Banner": null, "Date": "2024-04-23", "Description": "The worse Film. For testing.", "Name": "Test Film: Revolutions", "Time": "17:45:00", "viewingID": 3}, {"Banner": "https://www.looper.com/img/gallery/why-the-matrix-is-the-best-sci-fi-movie-ever/l-intro-1606326740.jpg", "Date": "2024-05-20", "Description": "Eh. For Testing", "Name": "Test Film: Reloaded", "Time": "18:30:00", "viewingID": 5}, {"Banner": null, "Date": "2025-02-04", "Description": "Film", "Name": "The Imitation Game", "Time": "18:00:00", "viewingID": 0}]');`

const sortLatest = (viewings) => {
    return viewings.sort((a, b) => new Date(b.Date + ' ' + b.Time) - new Date(a.Date + ' ' + a.Time));
};

const sortEarliest = (viewings) => {
    return viewings.sort((a, b) => new Date(a.Date + ' ' + a.Time) - new Date(b.Date + ' ' + b.Time));
};

const getSort = () => {
    selector = document.getElementById('orderSelector')
    if (selector.value === 'earliest') {
        sortedViewings = sortEarliest(viewings);
        renderViewings(viewings);
    }
    else {
        sortedViewings = sortLatest(viewings);
        renderViewings(viewings);
    }
};

// TODO: FIX SEARCH CONFLICTING WITH SORT

const searchName = () => {
    const search = document.getElementById('searchBar').value;
    const filteredViewings = viewings.filter(viewing => viewing.Name.toLowerCase().includes(search.toLowerCase()));
    if (filteredViewings === lastSearchedViewings) {
        return;
    }
    lastSearchedViewings = filteredViewings;
    renderViewings(filteredViewings);
}

const renderViewings = (viewings) => {
    const viewingsContainer = document.getElementById('viewingsContainer');
    viewingsContainer.innerHTML = '';

    viewings.forEach((viewing) => {
        viewingsContainer.innerHTML += `
        <div class="viewingCard card w-full bg-base-300 h-80" id="${viewing.viewingID}">
        ${ viewing.Banner ? `<figure><img src="${ viewing.Banner }" alt="${viewing.Name} banner" /></figure>` : '<figure></figure>' }
        <div class="card-body gap-3 flex-wrap">
        
            <h2 class="card-title text-xl font-bold flex-wrap">${ viewing.Name }</h2>
            <span>
            <div class="badge p-3 badge-neutral mx-1">${viewing.Date}</div>
            <div class="badge p-3 badge-neutral mx-1">${viewing.Time}</div>
            </span>
            
            <p>${ viewing.Description }</p>
            <a href="/newBooking?id=${viewing.viewingID}" class="btn btn-primary text-base-100 text-lg" name="Select">Select</a>
        </div>
        </div>
        `;
    });
};
