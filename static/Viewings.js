let lastSearchedViewings = [];


const showEnter = () => {
    if (window.innerWidth > 768) {
        document.getElementById('enter').style.display = 'block';
        [...document.getElementsByClassName('unfocusedKbd')].forEach((element) => {element.style.display = 'none';});
    }
};

const hideEnter = () => {
    if (window.innerWidth > 768) {
        document.getElementById('enter').style.display = 'none';
        [...document.getElementsByClassName('unfocusedKbd')].forEach((element) => {element.style.display = 'block';});
    }
};


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

document.addEventListener('keydown', (event) => {
    if (event.metaKey && event.key === 'k') {
        let searchBox = document.getElementById('searchBar');
        searchBox.focus();
    }
  });

