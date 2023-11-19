document.addEventListener('DOMContentLoaded', function () {
    const existingItemCheckbox = document.querySelector('#existingItem');
    const submitButton = document.querySelector('input[type="submit"]');
    const basket = document.querySelector('#basket');

    // * checkbox update enable forms
    existingItemCheckbox.addEventListener('change', function () {
        const inputsToDisable = document.querySelectorAll('#item, #brand, #weight');
        inputsToDisable.forEach(input => {
            input.disabled = this.checked;
        });
    });

    // * for submit button to add to basket
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
    // * for searching
    const searchItemInput = document.querySelector('#searchItem');
    const itemDropdown = document.querySelector('#itemDropdown');
    const items = Array.from(document.querySelectorAll('#itemDropdown li'));

    searchItemInput.addEventListener('input', function () {
        const searchTerm = this.value.toUpperCase();
        items.forEach(item => {
            const txtValue = item.textContent || item.innerText;
            if (txtValue.toUpperCase().indexOf(searchTerm) > -1) {
                item.style.display = "";
            } else {
                item.style.display = "none";
            }
        });

        itemDropdown.classList.remove('hide');
    });

    searchItemInput.addEventListener('focus', function () {
        itemDropdown.classList.remove('hide');
    });

    searchItemInput.addEventListener('blur', function (e) {
        setTimeout(function() {

            
            itemDropdown.classList.add('hide');

        }, 50);
    });

    itemDropdown.addEventListener('click', function (e) {
        if (e.target.tagName === 'LI') {
            searchItemInput.value = e.target.textContent;
            itemDropdown.classList.remove('show');

            const itemNameInput = document.querySelector('#item');
            const priceInput = document.querySelector('#price');
            const brandInput = document.querySelector('#brand');
            const weightInput = document.querySelector('#weight');

            const selectedItemId = e.target.dataset.id;
            const selectedBrand = e.target.dataset.brand;
            const selectedName = e.target.dataset.name;
            const selectedWeight = e.target.dataset.weight;

            itemNameInput.value = selectedName;
            priceInput.value = '';
            brandInput.value = selectedBrand;
            weightInput.value = selectedWeight;

            existingItemCheckbox.checked = true;
            itemDropdown.classList.add('hide');
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
