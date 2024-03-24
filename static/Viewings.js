let lastSearchedViewings = [];
let sortedViewings = [];    

const newBooking = (viewingID) => {
    fetch('/api/bookings/startNewBooking', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'viewingID': viewingID})
    }).then((response) => {
        if (response.status == 200) {
            window.location.href = '/booking/tickets';
        } else {
            newError('Error: Selection request failed');
        }
    }).catch((error) => {
        newError('Error: Selection request failed - ' + error);
    });
};


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
            <span class='flex gap-3'>
            <div class="badge p-3 flex gap-2 badge-neutral font-semibold"><svg class="w-4 self-center" version="1.1" id="_x32_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <style type="text/css"> .st0{fill:#ffffffec;} </style> <g> <path class="st0" d="M149.193,103.525c15.995,0,28.964-12.97,28.964-28.973V28.964C178.157,12.97,165.188,0,149.193,0 c-16.002,0-28.973,12.97-28.973,28.964v45.588C120.22,90.556,133.191,103.525,149.193,103.525z"></path> <path class="st0" d="M362.816,103.525c15.994,0,28.964-12.97,28.964-28.973V28.964C391.78,12.97,378.81,0,362.816,0 c-16.003,0-28.973,12.97-28.973,28.964v45.588C333.843,90.556,346.813,103.525,362.816,103.525z"></path> <path class="st0" d="M435.164,41.287h-17.925v33.265c0,30.017-24.414,54.432-54.422,54.432c-30.018,0-54.432-24.415-54.432-54.432 V41.287H203.616v33.265c0,30.017-24.415,54.432-54.423,54.432c-30.016,0-54.432-24.415-54.432-54.432V41.287H76.836 c-38.528,0-69.763,31.235-69.763,69.763v331.187C7.073,480.765,38.309,512,76.836,512h358.328 c38.528,0,69.763-31.235,69.763-69.763V111.05C504.927,72.522,473.692,41.287,435.164,41.287z M470.982,442.237 c0,19.748-16.069,35.818-35.818,35.818H76.836c-19.748,0-35.818-16.07-35.818-35.818V155.138h429.964V442.237z"></path> <rect x="175.862" y="384.002" class="st0" width="62.859" height="62.859"></rect> <rect x="175.862" y="286.584" class="st0" width="62.859" height="62.859"></rect> <rect x="78.453" y="384.002" class="st0" width="62.851" height="62.859"></rect> <rect x="78.453" y="286.584" class="st0" width="62.851" height="62.859"></rect> <rect x="370.697" y="189.175" class="st0" width="62.851" height="62.851"></rect> <rect x="273.28" y="189.175" class="st0" width="62.859" height="62.851"></rect> <rect x="273.28" y="286.584" class="st0" width="62.859" height="62.859"></rect> <rect x="370.697" y="384.002" class="st0" width="62.851" height="62.859"></rect> <rect x="370.697" y="286.584" class="st0" width="62.851" height="62.859"></rect> <rect x="273.28" y="384.002" class="st0" width="62.859" height="62.859"></rect> <rect x="175.862" y="189.175" class="st0" width="62.859" height="62.851"></rect> <rect x="78.453" y="189.175" class="st0" width="62.851" height="62.851"></rect> </g> </g></svg> ${viewing.Date}</div>
            <div class="badge p-3 flex gap-2 badge-neutral font-semibold"><svg class="w-4 self-center" height="200px" width="200px" version="1.1" id="_x32_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <style type="text/css"> .st0{fill:#ffffffec;} </style> <g> <path class="st0" d="M94.568,165.976l-0.448,0.863l15.71,7.895l15.826,9.274l0.548-0.968c0.948-1.694,1.924-3.355,2.928-4.992 l-30.619-18.806C97.153,161.444,95.841,163.694,94.568,165.976z"></path> <path class="st0" d="M110.667,255.847c0-1.339,0.026-2.686,0.059-4.024l-43.109-0.855c-0.052,1.629-0.076,3.258-0.076,4.879 l0.024,3.097l43.129-0.54L110.667,255.847z"></path> <path class="st0" d="M93.391,343.936c1.276,2.363,2.611,4.702,4,7.024l30.828-18.468c-1.109-1.855-2.175-3.734-3.2-5.637 L93.391,343.936z"></path> <path class="st0" d="M386.883,184.976l31.586-17.154c-1.284-2.355-2.611-4.685-3.988-6.992l-30.829,18.476 C384.776,181.178,385.851,183.064,386.883,184.976z"></path> <path class="st0" d="M256.147,110.669c1.292,0,2.583,0.016,3.869,0.057l0.926-43.113c-1.593-0.048-3.194-0.072-4.794-0.072 l-3.264,0.032l0.645,43.121L256.147,110.669z"></path> <path class="st0" d="M185.056,125.072l-17.101-31.605c-2.365,1.274-4.702,2.605-7.012,3.984l18.462,30.839 C181.266,127.178,183.153,126.105,185.056,125.072z"></path> <path class="st0" d="M352.641,98.444c-2.161-1.323-4.365-2.613-6.71-3.92l-8.964,15.573l-8.423,15.879 c1.804,1,3.572,2.04,5.314,3.105L352.641,98.444z"></path> <path class="st0" d="M326.754,387.032l17.044,31.645c2.371-1.274,4.716-2.605,7.026-3.984l-18.419-30.863 C330.544,384.944,328.663,386.008,326.754,387.032z"></path> <path class="st0" d="M382.762,334.121l30.562,18.903c1.418-2.29,2.78-4.613,3.91-6.653l0.568-1.008l-31.77-16.814 C384.98,330.436,383.885,332.298,382.762,334.121z"></path> <path class="st0" d="M159.133,413.419c2.232,1.379,4.506,2.71,6.915,4.057l17.413-31.444c-1.867-1.04-3.706-2.121-5.516-3.226 L159.133,413.419z"></path> <path class="st0" d="M444.417,252.718l-43.111,0.742l0.026,2.702c0,1.25-0.026,2.5-0.059,3.758l43.109,0.895 c0.052-1.556,0.076-3.105,0.076-4.653L444.417,252.718z"></path> <path class="st0" d="M255.853,401.339c-1.361,0-2.724-0.024-4.093-0.065l-0.982,43.105c1.691,0.064,3.389,0.088,5.074,0.088 l2.97-0.024l-0.562-43.129L255.853,401.339z"></path> <path class="st0" d="M256,0C114.839,0,0,114.847,0,256c0,141.161,114.839,256,256,256s256-114.839,256-256 C512,114.847,397.161,0,256,0z M256,465.597c-115.572,0-209.597-94.024-209.597-209.597S140.428,46.403,256,46.403 S465.605,140.428,465.605,256S371.572,465.597,256,465.597z"></path> <path class="st0" d="M385.351,154.282l-20.03-21.081L258.976,234.226l-66.774-66.774l-27.359,27.363l66.07,66.073l-22.609,21.476 l20.032,21.089l23.147-21.992l24.056,24.056l27.361-27.363l-23.355-23.355L385.351,154.282z M256,269.081 c-7.222,0-13.077-5.855-13.077-13.081c0-7.218,5.855-13.072,13.077-13.072c7.222,0,13.074,5.855,13.074,13.072 C269.074,263.226,263.222,269.081,256,269.081z"></path> </g> </g></svg> ${viewing.Time}</div>
            </span>
            
            <p>${ viewing.Description }</p>
            <button onclick="newBooking(${ viewing.viewingID })" class="btn no-animation btn-primary text-base-100 text-lg" name="Select">Select</button>
            </div>
        </div>
        `;
    });
};

document.addEventListener('keydown', (event) => {
    if (event.metaKey && event.key === 'k' || event.ctrlKey && event.key === 'k') {
        let searchBox = document.getElementById('searchBar');
        searchBox.focus();
    }
  });

