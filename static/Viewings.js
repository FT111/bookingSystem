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
    let selector = document.getElementById('orderSelector')

    if (selector.value === 'earliest') {
        sortedViewings = sortEarliest(viewings);

        renderViewings(viewings);
    }
    else {
        sortedViewings = sortLatest(viewings);
        renderViewings(viewings);
    }
    viewings.forEach((viewing) => {
            console.log(viewing.Name + ': ' + viewing.Date + ' ' + viewing.Time);
        });
};

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

    if (edit === true) {
        viewingsContainer.innerHTML = `
            <div class="drawer drawer-end">
              <input id="newViewingDrawer" type="checkbox" class="drawer-toggle" />
              <div class="drawer-content">
                  <label for="newViewingDrawer" class="viewingCard card w-full drawer-button bg-base-200 hover:bg-base-300 hover:scale-[1.02] hover:shadow-lg cursor-pointer transition-all h-80 flex-1 items-center p-20">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-full h-full">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                    </svg>
                  </label>
              </div>
              <div class="drawer-side z-50 h-full">
                <label for="newViewingDrawer" aria-label="close sidebar" class="drawer-overlay"></label>
                  <div class="w-11/12 sm:w-1/2 lg:w-1/2 min-h-full h-max bg-base-100 p-3 sm:p-8">
                <form action="/api/viewings/submit" method="POST" class="flex flex-col min-h-full w-full">
                    <div class="flex flex-col gap-5 w-full card sm:p-10">
                        <label for="name" class="flex flex-row gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M9.568 3H5.25A2.25 2.25 0 0 0 3 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 0 0 5.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 0 0 9.568 3Z" />
                              <path stroke-linecap="round" stroke-linejoin="round" d="M6 6h.008v.008H6V6Z" />
                            </svg>

                            Name</label>
                        <input type="text" name="viewingName" id="name" class="input input-bordered rounded-box" required>

                        <label for="date" class="flex flex-row gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5m-9-6h.008v.008H12v-.008ZM12 15h.008v.008H12V15Zm0 2.25h.008v.008H12v-.008ZM9.75 15h.008v.008H9.75V15Zm0 2.25h.008v.008H9.75v-.008ZM7.5 15h.008v.008H7.5V15Zm0 2.25h.008v.008H7.5v-.008Zm6.75-4.5h.008v.008h-.008v-.008Zm0 2.25h.008v.008h-.008V15Zm0 2.25h.008v.008h-.008v-.008Zm2.25-4.5h.008v.008H16.5v-.008Zm0 2.25h.008v.008H16.5V15Z" />
                            </svg>

                            Date</label>
                        <input type="date" name="Date" id="date" class="input input-bordered rounded-box" required>

                        <label for="time" class="flex flex-row gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                            </svg>


                            Time</label>
                        <input type="time" name="Time" id="time" class="input input-bordered rounded-box" required >

                        <label for="banner" class="flex flex-row gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" />
                        </svg>
                        Banner URL
                        </label>
                        <input type="text" name="Banner" id="banner" class="input input-bordered rounded-box">

                        <div class="flex flex-col md:flex-row flex-1 gap-4">
                            <div class="flex flex-col gap-3 grow">
                                <label for="rows" class="flex flex-row gap-2">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 4.5h14.25M3 9h9.75M3 13.5h9.75m4.5-4.5v12m0 0-3.75-3.75M17.25 21 21 17.25" />
                                </svg>
                                Number of rows
                                </label>

                                <input type="number" name="rowCount" id="rows" class="input input-bordered rounded-box" required>
                            </div>
                            <div class="flex flex-col gap-3 grow">
                                <label for="seatsPerRow" class="flex flex-row gap-2">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25H12" />
                                </svg>
                                    Seats in each row
                                </label>
                                <input type="number" name="seatsPerRow" id="seatsPerRow" class="input input-bordered rounded-box" required>
                            </div>
                        </div>

                        <label for="Description">Description</label>
                        <textarea name="Description" id="description" class="textarea textarea-bordered rounded-box"></textarea>

                    </div>
                    <div class="flex flex-col gap-4 sm:gap-0 my-3 px-0 p-3 sm:flex-row w-full items-center justify-between transition-full ease-in-out duration-100">
                        <div></div> <!-- Spacer -->

                            <button formaction="/api/viewings/submit" class="btn btn-primary items-center btn-block sm:btn-md sm:w-auto flex-end rounded-md text-white transition-all ease-in-out duration-200" id="submitBtn">Submit
                                <!-- prettier-ignore -->
                                <svg class="stroke-base-200 transition-all ease-in-out duration-400" width="16px" height="16px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M5 12H19M19 12L13 6M19 12L13 18" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
                            </button>
                        </div>
                </form>
                  </div>
              </div>
            </div>

`;
           } else {
        viewingsContainer.innerHTML = ``;
    }


    viewings.forEach((viewing) => {
        if (edit === true) {
            viewingsContainer.innerHTML += `
            <div class="viewingCard card w-full bg-base-300 h-80" id="${viewing.viewingID}">
            ${viewing.Banner ? `<figure><img src="${viewing.Banner}" alt="${viewing.Name} banner" /></figure>` : '<figure></figure>'}
            <div class="card-body gap-3">
            
                <h2 class="card-title text-xl font-bold flex-wrap">${viewing.Name}</h2>
                <span class='flex flex-wrap gap-3 w-full'>
                <div class="badge p-3 flex gap-2 badge-neutral font-semibold"><svg class="w-4 self-center" version="1.1" id="_x32_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <style type="text/css"> .st0{fill:#ffffffec;} </style> <g> <path class="st0" d="M149.193,103.525c15.995,0,28.964-12.97,28.964-28.973V28.964C178.157,12.97,165.188,0,149.193,0 c-16.002,0-28.973,12.97-28.973,28.964v45.588C120.22,90.556,133.191,103.525,149.193,103.525z"></path> <path class="st0" d="M362.816,103.525c15.994,0,28.964-12.97,28.964-28.973V28.964C391.78,12.97,378.81,0,362.816,0 c-16.003,0-28.973,12.97-28.973,28.964v45.588C333.843,90.556,346.813,103.525,362.816,103.525z"></path> <path class="st0" d="M435.164,41.287h-17.925v33.265c0,30.017-24.414,54.432-54.422,54.432c-30.018,0-54.432-24.415-54.432-54.432 V41.287H203.616v33.265c0,30.017-24.415,54.432-54.423,54.432c-30.016,0-54.432-24.415-54.432-54.432V41.287H76.836 c-38.528,0-69.763,31.235-69.763,69.763v331.187C7.073,480.765,38.309,512,76.836,512h358.328 c38.528,0,69.763-31.235,69.763-69.763V111.05C504.927,72.522,473.692,41.287,435.164,41.287z M470.982,442.237 c0,19.748-16.069,35.818-35.818,35.818H76.836c-19.748,0-35.818-16.07-35.818-35.818V155.138h429.964V442.237z"></path> <rect x="175.862" y="384.002" class="st0" width="62.859" height="62.859"></rect> <rect x="175.862" y="286.584" class="st0" width="62.859" height="62.859"></rect> <rect x="78.453" y="384.002" class="st0" width="62.851" height="62.859"></rect> <rect x="78.453" y="286.584" class="st0" width="62.851" height="62.859"></rect> <rect x="370.697" y="189.175" class="st0" width="62.851" height="62.851"></rect> <rect x="273.28" y="189.175" class="st0" width="62.859" height="62.851"></rect> <rect x="273.28" y="286.584" class="st0" width="62.859" height="62.859"></rect> <rect x="370.697" y="384.002" class="st0" width="62.851" height="62.859"></rect> <rect x="370.697" y="286.584" class="st0" width="62.851" height="62.859"></rect> <rect x="273.28" y="384.002" class="st0" width="62.859" height="62.859"></rect> <rect x="175.862" y="189.175" class="st0" width="62.859" height="62.851"></rect> <rect x="78.453" y="189.175" class="st0" width="62.851" height="62.851"></rect> </g> </g></svg> ${viewing.dateFormatted}</div>
                <div class="badge p-3 flex gap-2 badge-neutral font-semibold"><svg class="w-4 self-center" height="200px" width="200px" version="1.1" id="_x32_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <style type="text/css"> .st0{fill:#ffffffec;} </style> <g> <path class="st0" d="M94.568,165.976l-0.448,0.863l15.71,7.895l15.826,9.274l0.548-0.968c0.948-1.694,1.924-3.355,2.928-4.992 l-30.619-18.806C97.153,161.444,95.841,163.694,94.568,165.976z"></path> <path class="st0" d="M110.667,255.847c0-1.339,0.026-2.686,0.059-4.024l-43.109-0.855c-0.052,1.629-0.076,3.258-0.076,4.879 l0.024,3.097l43.129-0.54L110.667,255.847z"></path> <path class="st0" d="M93.391,343.936c1.276,2.363,2.611,4.702,4,7.024l30.828-18.468c-1.109-1.855-2.175-3.734-3.2-5.637 L93.391,343.936z"></path> <path class="st0" d="M386.883,184.976l31.586-17.154c-1.284-2.355-2.611-4.685-3.988-6.992l-30.829,18.476 C384.776,181.178,385.851,183.064,386.883,184.976z"></path> <path class="st0" d="M256.147,110.669c1.292,0,2.583,0.016,3.869,0.057l0.926-43.113c-1.593-0.048-3.194-0.072-4.794-0.072 l-3.264,0.032l0.645,43.121L256.147,110.669z"></path> <path class="st0" d="M185.056,125.072l-17.101-31.605c-2.365,1.274-4.702,2.605-7.012,3.984l18.462,30.839 C181.266,127.178,183.153,126.105,185.056,125.072z"></path> <path class="st0" d="M352.641,98.444c-2.161-1.323-4.365-2.613-6.71-3.92l-8.964,15.573l-8.423,15.879 c1.804,1,3.572,2.04,5.314,3.105L352.641,98.444z"></path> <path class="st0" d="M326.754,387.032l17.044,31.645c2.371-1.274,4.716-2.605,7.026-3.984l-18.419-30.863 C330.544,384.944,328.663,386.008,326.754,387.032z"></path> <path class="st0" d="M382.762,334.121l30.562,18.903c1.418-2.29,2.78-4.613,3.91-6.653l0.568-1.008l-31.77-16.814 C384.98,330.436,383.885,332.298,382.762,334.121z"></path> <path class="st0" d="M159.133,413.419c2.232,1.379,4.506,2.71,6.915,4.057l17.413-31.444c-1.867-1.04-3.706-2.121-5.516-3.226 L159.133,413.419z"></path> <path class="st0" d="M444.417,252.718l-43.111,0.742l0.026,2.702c0,1.25-0.026,2.5-0.059,3.758l43.109,0.895 c0.052-1.556,0.076-3.105,0.076-4.653L444.417,252.718z"></path> <path class="st0" d="M255.853,401.339c-1.361,0-2.724-0.024-4.093-0.065l-0.982,43.105c1.691,0.064,3.389,0.088,5.074,0.088 l2.97-0.024l-0.562-43.129L255.853,401.339z"></path> <path class="st0" d="M256,0C114.839,0,0,114.847,0,256c0,141.161,114.839,256,256,256s256-114.839,256-256 C512,114.847,397.161,0,256,0z M256,465.597c-115.572,0-209.597-94.024-209.597-209.597S140.428,46.403,256,46.403 S465.605,140.428,465.605,256S371.572,465.597,256,465.597z"></path> <path class="st0" d="M385.351,154.282l-20.03-21.081L258.976,234.226l-66.774-66.774l-27.359,27.363l66.07,66.073l-22.609,21.476 l20.032,21.089l23.147-21.992l24.056,24.056l27.361-27.363l-23.355-23.355L385.351,154.282z M256,269.081 c-7.222,0-13.077-5.855-13.077-13.081c0-7.218,5.855-13.072,13.077-13.072c7.222,0,13.074,5.855,13.074,13.072 C269.074,263.226,263.222,269.081,256,269.081z"></path> </g> </g></svg> ${viewing.Time}</div>
                <div class="tooltip" data-tip="Remaining tickets">
                    <div class="badge p-3 flex gap-2 badge-neutral font-semibold"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 6v.75m0 3v.75m0 3v.75m0 3V18m-9-5.25h5.25M7.5 15h3M3.375 5.25c-.621 0-1.125.504-1.125 1.125v3.026a2.999 2.999 0 0 1 0 5.198v3.026c0 .621.504 1.125 1.125 1.125h17.25c.621 0 1.125-.504 1.125-1.125v-3.026a2.999 2.999 0 0 1 0-5.198V6.375c0-.621-.504-1.125-1.125-1.125H3.375Z" /></svg>${viewing.remainingSeatCount}</div>
                </div>
                </span>
                
                <p class="truncate">${viewing.Description}</p>
                <div class="flex flex-row gap-3 w-full flex-1 items-end">
                    <button onclick="beginViewingDeletion(${viewing.viewingID})" class="btn no-animation btn-error text-white text-lg" name="Select">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                      <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                    </svg>
    
                    </button>
                    
                    
                    <button onclick="window.location.href='/viewings/edit/${viewing.viewingID}'" class="btn grow no-animation btn-primary text-white text-lg" name="Select">Edit</button>
    
                </div>
                </div>
            </div>
            `;

        } else {
            let viewingButton = viewing.remainingSeatCount > 0
                ? `<button onclick="newBooking(${viewing.viewingID})"class="btn btn-primary text-white text-lg btn-no-animation" name="Select">Select</button>`
                : `<button class="btn btn-neutral btn-disabled text-white text-lg" name="Select">Sold out</button>`;

            viewingsContainer.innerHTML += `
            <div class="viewingCard card w-full bg-base-300 h-80" id="${viewing.viewingID}">
            ${viewing.Banner ? `<figure><img draggable="false" ondragstart="return false;"  src="${viewing.Banner}" alt="${viewing.Name} banner" /></figure>` : '<figure></figure>'}
            <div class="card-body gap-3">
            
                <h2 class="card-title">${viewing.Name}</h2>
                
                <span class='flex flex-wrap gap-3 w-full'>
                 <div class="badge p-3 flex gap-2 badge-neutral font-semibold"><svg class="w-4 self-center" version="1.1" id="_x32_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <style type="text/css"> .st0{fill:#ffffffec;} </style> <g> <path class="st0" d="M149.193,103.525c15.995,0,28.964-12.97,28.964-28.973V28.964C178.157,12.97,165.188,0,149.193,0 c-16.002,0-28.973,12.97-28.973,28.964v45.588C120.22,90.556,133.191,103.525,149.193,103.525z"></path> <path class="st0" d="M362.816,103.525c15.994,0,28.964-12.97,28.964-28.973V28.964C391.78,12.97,378.81,0,362.816,0 c-16.003,0-28.973,12.97-28.973,28.964v45.588C333.843,90.556,346.813,103.525,362.816,103.525z"></path> <path class="st0" d="M435.164,41.287h-17.925v33.265c0,30.017-24.414,54.432-54.422,54.432c-30.018,0-54.432-24.415-54.432-54.432 V41.287H203.616v33.265c0,30.017-24.415,54.432-54.423,54.432c-30.016,0-54.432-24.415-54.432-54.432V41.287H76.836 c-38.528,0-69.763,31.235-69.763,69.763v331.187C7.073,480.765,38.309,512,76.836,512h358.328 c38.528,0,69.763-31.235,69.763-69.763V111.05C504.927,72.522,473.692,41.287,435.164,41.287z M470.982,442.237 c0,19.748-16.069,35.818-35.818,35.818H76.836c-19.748,0-35.818-16.07-35.818-35.818V155.138h429.964V442.237z"></path> <rect x="175.862" y="384.002" class="st0" width="62.859" height="62.859"></rect> <rect x="175.862" y="286.584" class="st0" width="62.859" height="62.859"></rect> <rect x="78.453" y="384.002" class="st0" width="62.851" height="62.859"></rect> <rect x="78.453" y="286.584" class="st0" width="62.851" height="62.859"></rect> <rect x="370.697" y="189.175" class="st0" width="62.851" height="62.851"></rect> <rect x="273.28" y="189.175" class="st0" width="62.859" height="62.851"></rect> <rect x="273.28" y="286.584" class="st0" width="62.859" height="62.859"></rect> <rect x="370.697" y="384.002" class="st0" width="62.851" height="62.859"></rect> <rect x="370.697" y="286.584" class="st0" width="62.851" height="62.859"></rect> <rect x="273.28" y="384.002" class="st0" width="62.859" height="62.859"></rect> <rect x="175.862" y="189.175" class="st0" width="62.859" height="62.851"></rect> <rect x="78.453" y="189.175" class="st0" width="62.851" height="62.851"></rect> </g> </g></svg> ${viewing.dateFormatted}</div>
                <div class="badge p-3 flex gap-2 badge-neutral font-semibold"><svg class="w-4 self-center" height="200px" width="200px" version="1.1" id="_x32_" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 512 512" xml:space="preserve" fill="#000000"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <style type="text/css"> .st0{fill:#ffffffec;} </style> <g> <path class="st0" d="M94.568,165.976l-0.448,0.863l15.71,7.895l15.826,9.274l0.548-0.968c0.948-1.694,1.924-3.355,2.928-4.992 l-30.619-18.806C97.153,161.444,95.841,163.694,94.568,165.976z"></path> <path class="st0" d="M110.667,255.847c0-1.339,0.026-2.686,0.059-4.024l-43.109-0.855c-0.052,1.629-0.076,3.258-0.076,4.879 l0.024,3.097l43.129-0.54L110.667,255.847z"></path> <path class="st0" d="M93.391,343.936c1.276,2.363,2.611,4.702,4,7.024l30.828-18.468c-1.109-1.855-2.175-3.734-3.2-5.637 L93.391,343.936z"></path> <path class="st0" d="M386.883,184.976l31.586-17.154c-1.284-2.355-2.611-4.685-3.988-6.992l-30.829,18.476 C384.776,181.178,385.851,183.064,386.883,184.976z"></path> <path class="st0" d="M256.147,110.669c1.292,0,2.583,0.016,3.869,0.057l0.926-43.113c-1.593-0.048-3.194-0.072-4.794-0.072 l-3.264,0.032l0.645,43.121L256.147,110.669z"></path> <path class="st0" d="M185.056,125.072l-17.101-31.605c-2.365,1.274-4.702,2.605-7.012,3.984l18.462,30.839 C181.266,127.178,183.153,126.105,185.056,125.072z"></path> <path class="st0" d="M352.641,98.444c-2.161-1.323-4.365-2.613-6.71-3.92l-8.964,15.573l-8.423,15.879 c1.804,1,3.572,2.04,5.314,3.105L352.641,98.444z"></path> <path class="st0" d="M326.754,387.032l17.044,31.645c2.371-1.274,4.716-2.605,7.026-3.984l-18.419-30.863 C330.544,384.944,328.663,386.008,326.754,387.032z"></path> <path class="st0" d="M382.762,334.121l30.562,18.903c1.418-2.29,2.78-4.613,3.91-6.653l0.568-1.008l-31.77-16.814 C384.98,330.436,383.885,332.298,382.762,334.121z"></path> <path class="st0" d="M159.133,413.419c2.232,1.379,4.506,2.71,6.915,4.057l17.413-31.444c-1.867-1.04-3.706-2.121-5.516-3.226 L159.133,413.419z"></path> <path class="st0" d="M444.417,252.718l-43.111,0.742l0.026,2.702c0,1.25-0.026,2.5-0.059,3.758l43.109,0.895 c0.052-1.556,0.076-3.105,0.076-4.653L444.417,252.718z"></path> <path class="st0" d="M255.853,401.339c-1.361,0-2.724-0.024-4.093-0.065l-0.982,43.105c1.691,0.064,3.389,0.088,5.074,0.088 l2.97-0.024l-0.562-43.129L255.853,401.339z"></path> <path class="st0" d="M256,0C114.839,0,0,114.847,0,256c0,141.161,114.839,256,256,256s256-114.839,256-256 C512,114.847,397.161,0,256,0z M256,465.597c-115.572,0-209.597-94.024-209.597-209.597S140.428,46.403,256,46.403 S465.605,140.428,465.605,256S371.572,465.597,256,465.597z"></path> <path class="st0" d="M385.351,154.282l-20.03-21.081L258.976,234.226l-66.774-66.774l-27.359,27.363l66.07,66.073l-22.609,21.476 l20.032,21.089l23.147-21.992l24.056,24.056l27.361-27.363l-23.355-23.355L385.351,154.282z M256,269.081 c-7.222,0-13.077-5.855-13.077-13.081c0-7.218,5.855-13.072,13.077-13.072c7.222,0,13.074,5.855,13.074,13.072 C269.074,263.226,263.222,269.081,256,269.081z"></path> </g> </g></svg> ${viewing.Time}</div>
                <div class="tooltip" data-tip="Remaining tickets">
                <div class="badge p-3 flex gap-2 badge-neutral font-semibold"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 6v.75m0 3v.75m0 3v.75m0 3V18m-9-5.25h5.25M7.5 15h3M3.375 5.25c-.621 0-1.125.504-1.125 1.125v3.026a2.999 2.999 0 0 1 0 5.198v3.026c0 .621.504 1.125 1.125 1.125h17.25c.621 0 1.125-.504 1.125-1.125v-3.026a2.999 2.999 0 0 1 0-5.198V6.375c0-.621-.504-1.125-1.125-1.125H3.375Z" /></svg>${viewing.remainingSeatCount}</div>
                </div>
                </span>
                
                <p class="truncate">${viewing.Description}</p>

                ${viewingButton}
                `
        }
    });
};


document.addEventListener('keydown', (event) => {
    if (event.metaKey && event.key === 'k' || event.ctrlKey && event.key === 'k') {
        let searchBox = document.getElementById('searchBar');
        searchBox.focus();
    }
  });

window.addEventListener('load', () => {

    getSort();
});