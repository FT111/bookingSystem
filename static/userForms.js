
let Users = [];
let selectedUser = null;
let filteredUsers = [];

const renderUserTable = (outputTableID, data) => {
    let table = document.getElementById(outputTableID);
    let tableBody = table.getElementsByTagName('tbody')[0];
    tableBody.innerHTML = ''; // Clear the table body

    console.log(data);
    if (data !== undefined && data.length !== 0) {
        data.forEach(user => {
            let newRow = tableBody.insertRow();
            newRow.classList.add('hover', 'cursor-pointer');
            newRow.addEventListener('click', () => {
                selectCustomer(user, outputTableID);
            });

            let nameCell = newRow.insertCell(0);
            let emailCell = newRow.insertCell(1);
            let phoneCell = newRow.insertCell(2);

            nameCell.innerHTML = `${user['firstName'] + ' ' + user['Surname']}`;
            emailCell.innerHTML = user["emailAddress"];
            phoneCell.innerHTML = user['phoneNumber'];
    })}
}

const selectCustomer = (user, userTableID=null) => {
    [...document.getElementsByClassName('drawer-toggle')].forEach(drawer => {
        drawer.checked = false;
    });
    selectedUser = user;

    document.getElementById(('continueBtn')).disabled = false;
    document.getElementById('continueTooltip').classList.remove('tooltip', 'sm:tooltip-left', 'tooltip-bottom');

    if (userTableID !== null) {
        document.getElementById('selectedEmail').innerHTML = user['emailAddress'];
        document.getElementById('selectedPhone').innerHTML = user['phoneNumber'];
        document.getElementById('selectedName').innerHTML = user['firstName'] + ' ' + user['Surname'];
    }
    console.log(user);
    let response = fetch('/api/bookings/addCustomer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"customerID": user['ID']})

    }).then(
        response => {
            return selectedUser;
})};

const getAllCustomers = (outputTableID) => {
    if (Users.length !== 0) {
        return;
    }
    console.log(Users)
    let response = fetch('/api/customers/getAll', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify('ID')
    }).then(response => { if (response.ok) {
        return response.json();
    }})
    .then(data => {
        Users = data.body;
        renderUserTable(outputTableID, data.body);
    })
    .catch(error => {
        newError('Error: ' + error);
    });
}

const getCustomersByName =(userElement, outputTableID) => {
    const searchValue = document.getElementById('customerSearchBar').value;
    let filteredUsers = Users.filter(user => user['firstName'].toLowerCase().includes(searchValue.toLowerCase()) || user['Surname'].toLowerCase().includes(searchValue.toLowerCase()));

    renderUserTable(outputTableID, filteredUsers);

}


document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('newUserForm').addEventListener('submit', function(event) {
        event.preventDefault();

        let formValues = {
            Name: document.getElementById('newName').value,
            Email: document.getElementById('newEmail').value,
            phoneNumber: document.getElementById('newPhone').value,
            addToBooking: true
        };

        let response = fetch('/api/customers/new', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formValues)
        }).then(response => response.json())
        .then(data => {
            if (data.status !== 200) {
                newError(data.body);
                console.log(data);
                return;
            }

            let Name =  formValues.Name.split(' ');

            let newUser = {
                'ID': data.body,
                'firstName': Name[0],
                'Surname': Name[Name.length -1],
                'emailAddress': formValues.Email,
                'phoneNumber': formValues.phoneNumber
            }

            selectCustomer(newUser, 'userTable');
        })
        .catch(error => {
            newError('Error: ' + error);
        });
    });
});