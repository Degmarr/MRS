document.addEventListener('DOMContentLoaded', function () {
    // Function to fetch and display data
    function fetchData() {
        fetch('http://localhost:8000/combined_data/')
            .then(response => response.json())
            .then(data => {
                const dataTable = document.getElementById('data-list');
                dataTable.innerHTML = ''; // Clear previous data

                data.forEach(item => {
                    const row = dataTable.insertRow();

                    const columns = [
                        'name', 'age', 'address', 'national_id',
                        'diagnosis', 'treatment', 'allergies',
                        'immunizations', 'family_history'
                    ];

                    columns.forEach(column => {
                        const cell = row.insertCell();
                        cell.textContent = item[column];
                    });

                    // Add delete button
                    const deleteCell = row.insertCell();
                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete';
                    deleteButton.className = 'delete-button';
                    deleteButton.setAttribute('data-national-id', item.national_id); // Set data-national-id attribute
                    deleteCell.appendChild(deleteButton);
                });
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Call the fetchData function on page load
    fetchData();

    // Event listener for the "Add Data" form submission
    const addForm = document.getElementById('add-form');
    if (addForm) {
        addForm.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(addForm);
            const jsonData = {};

            formData.forEach((value, key) => {
                jsonData[key] = value;
            });

            fetch('http://localhost:8000/combined_data/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(jsonData),
            })
                .then(response => response.json())
                .then(data => {
                    alert('Medical record added successfully!');
                    fetchData(); // Refresh the displayed data on the main page
                })
                .catch(error => console.error('Error adding data:', error));
        });
    }

    // Function to delete data
    function deleteData(nationalId) {
        fetch(`http://localhost:8000/combined_data/${nationalId}`, {
            method: 'DELETE',
        })
            .then(response => response.json())
            .then(data => {
                alert('Medical record deleted successfully!');
                fetchData(); // Refresh the displayed data on the main page
            })
            .catch(error => console.error('Error deleting data:', error));
    }
});
