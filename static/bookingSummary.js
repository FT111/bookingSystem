
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('newUserForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const FormValues = Object.fromEntries(formData.entries());

        fetch('/api/customers/new', {
            method: 'POST',
            body: JSON.stringify(FormValues)
        }).then(response => response.json())
        .then(data => {
            newError(data.message);
        })
        .catch(error => {
            console.error(error);
        });
    });
});