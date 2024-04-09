let selectedViewingID = null;

const beginViewingDeletion = (viewingID) => {
    selectedViewingID = viewingID;
    document.getElementById('confirmDeletionModal').showModal();
}

const deleteViewing = async () => {
    const response = await fetch(`/api/viewings/manage/${selectedViewingID}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    if (response.status === 200) {
        document.getElementById('confirmDeletionModal').close();
        let viewingCard = document.getElementById(selectedViewingID);
        viewingCard.remove();
    } else {
        newError('Failed to delete viewing');
    }
}

