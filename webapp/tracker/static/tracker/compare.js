document.addEventListener('DOMContentLoaded', function() {
    const grocery1Select = document.getElementById('grocery1');
    const grocery2Select = document.getElementById('grocery2');
    const compareBtn = document.getElementById('compareBtn');
    const comparisonResult = document.getElementById('comparisonResult');

    compareBtn.addEventListener('click', function() {
        const selectedGrocery1 = grocery1Select.value;
        const selectedGrocery2 = grocery2Select.value;

        if (selectedGrocery1 && selectedGrocery2) {
            grocery1Select.disabled = true; // Disable grocery 1 select
            grocery2Select.disabled = true; // Disable grocery 2 select
            fetchComparisonData(selectedGrocery1, selectedGrocery2);
        } else {
            comparisonResult.textContent = 'Please select two groceries to compare.';
        }
    });

    function fetchComparisonData(grocery1, grocery2) {
        // Make a fetch request to the backend to get comparison data
        fetch(`/compare/${grocery1}/${grocery2}`)
            .then(response => response.json())
            .then(data => {
                // Display the received comparison data
                displayComparison(data);
            })
            .catch(error => {
                console.error('Error fetching comparison data:', error);
            });
    }

    function displayComparison(data) {
        // Update the comparisonResult div with the fetched data
        comparisonResult.textContent = JSON.stringify(data);
        // Modify this part to format and display the comparison data as desired
    }
});
