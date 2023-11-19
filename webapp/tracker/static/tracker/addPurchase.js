document.addEventListener('DOMContentLoaded', function () {

    const existingItemCheckbox = document.querySelector('#existingItem');
    const inputsToDisable = document.querySelectorAll('#item, #brand, #weight');
    const submitButton = document.querySelector('input[type="submit"]');
    const basket = document.querySelector('#basket');

    existingItemCheckbox.addEventListener('change', function () {
        const inputsToDisable = document.querySelectorAll('#item, #brand, #weight');
        inputsToDisable.forEach(input => {
            input.disabled = this.checked;
        });
    });

    submitButton.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent form submission

        const itemName = document.querySelector('#item').value;
        const price = document.querySelector('#price').value;
        const brand = document.querySelector('#brand').value;
        const weight = document.querySelector('#weight').value;
        const travexp = document.querySelector('#travexp').value;

        const newItem = document.createElement('div');
        newItem.classList.add('new-item');
        newItem.innerHTML = `
        <p>Item: ${itemName}
        Price: ${price}
        Brand: ${brand}
        Weight/Volume: ${weight}
        Travel Expenses: ${travexp}</p>
    `;

        basket.appendChild(newItem);

        resetForm();
    });
    const searchItemInput = document.querySelector('#searchItem');
    const dataList = document.querySelector('#itemList');
    const items = Array.from(document.querySelectorAll('#itemList option'));

    searchItemInput.addEventListener('input', function () {
        const searchTerm = this.value.toLowerCase();
        const matchedItems = items.filter(item => item.value.toLowerCase().includes(searchTerm)).slice(0, 5);

        // Clear the existing options in the datalist
        dataList.innerHTML = '';

        // Append matched items to the datalist
        matchedItems.forEach(item => {
            dataList.appendChild(item.cloneNode(true));
        });
    });

    // Handle selecting an option from the datalist
    searchItemInput.addEventListener('change', function () {
        const selectedOption = items.find(item => item.value.toLowerCase() === this.value.toLowerCase());
        if (selectedOption) {
            this.value = selectedOption.value;
            // Handle what to do when an option is selected, for example, you can perform an action here
        }
    });
});

function resetForm() {
    document.querySelectorAll('input[type="text"], input[type="number"]').forEach(input => {
        input.value = '';
    });

    const existingItemCheckbox = document.getElementById('existingItem');
    existingItemCheckbox.checked = false;
    existingItemCheckbox.disabled = true;
}
