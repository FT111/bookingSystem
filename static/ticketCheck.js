
function openCamera() {
    document.getElementById('fileInput').click();
}

function fileSelected() {
    var file = document.getElementById('fileInput').files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('imagePreview').src = e.target.result;
        };
        reader.readAsDataURL(file);
        checkTicket(file);
    }
}

function checkTicket(imageFile) {
    if (file) {
        const response = fetch('/api/tickets/checkQR', {
            method: 'POST',
            body: imageFile
        }).then(response => response.json()).then(data => {
            if (data.status === 'valid') {
                alert('Ticket is valid - ' + data.seatLocation);
            } else {
                alert('Ticket is not valid');
            }
        }).catch(error => {
            alert('An error occurred');
        });
    }
}

document.getElementById('fileInput').addEventListener('change', fileSelected);