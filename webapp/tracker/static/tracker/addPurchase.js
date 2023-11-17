document.addEventListener('DOMContentLoaded', function () {
    const items = ['Apple', 'Banana', 'Orange']; // Sample items

    const searchBar = document.getElementById('searchInput');
    searchBar.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            searchItem();
        }
    });

    const searchButton = document.getElementById('searchButton');
    searchButton.addEventListener('click', searchItem);

    function searchItem() {
        const searchValue = searchBar.value.toLowerCase();
        const resultsList = document.getElementById('resultsList');
        resultsList.innerHTML = '';

        const filteredItems = items.filter(item => item.toLowerCase().includes(searchValue));

        filteredItems.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            resultsList.appendChild(li);
        });

        // Add "Add New" option if the searched item doesn't exist in the list
        if (!filteredItems.includes(searchValue) && searchValue !== '') {
            const li = document.createElement('li');
            li.textContent = `Add New: ${searchValue}`;
            li.classList.add('add-new');
            resultsList.appendChild(li);
        }
    }
});
