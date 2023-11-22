const axios = require('axios');


document.addEventListener('DOMContentLoaded', function () {
    const existingItemCheckbox = document.querySelector('#existingItem');
    const submitButton = document.querySelector('input[type="submit"]');
    const basket = document.querySelector('#basket');

    // * checkbox update enable forms
    existingItemCheckbox.addEventListener('change', disableForms);

    // * for submit button to add to basket
    submitButton.addEventListener('click', function (e) {
        e.preventDefault(); // Prevent form submission

        const requiredInputs = document.querySelectorAll('input[required]');

        for (const input of requiredInputs) {
            if (input.value.trim() === '') {
                console.log(`${input.id} is empty.`);
                return;
            }
        }

        const id = document.querySelector('#id').value;
        const itemName = document.querySelector('#item').value;
        const price = document.querySelector('#price').value;
        const brand = document.querySelector('#brand').value;
        const weight = document.querySelector('#weight').value;
        const travexp = document.querySelector('#travexp').value;


        const newItem = document.createElement('div');
        newItem.classList.add('new-item');

        // add data
        if (existingItemCheckbox.checked) {
            newItem.dataset['id'] = id
        }
        newItem.dataset['item'] = itemName
        newItem.dataset['price'] = price
        newItem.dataset['brand'] = brand
        newItem.dataset['weight'] = weight
        if (travexp == "") {
            newItem.dataset['travexp'] = -1
        }



        newItem.innerHTML = `
        <p>Item: ${itemName}
        Price: ${price}
        Brand: ${brand}
        Weight/Volume: ${weight}
        Travel Expenses: ${travexp}</p>`;
        basket.appendChild(newItem);
        resetForm();
    });


    // * for searching
    const searchItemInput = document.querySelector('#searchItem');
    const itemDropdown = document.querySelector('#itemDropdown');
    const items = Array.from(document.querySelectorAll('#itemDropdown li'));

    searchItemInput.addEventListener('input', function () {
        if (searchItemInput.value == "") {
            resetForm()
            existingItemCheckbox.disabled = true
        }

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

    // * dropdown show
    searchItemInput.addEventListener('focus', function () {
        itemDropdown.classList.remove('hide');
    });
    // * dropdown show hide
    searchItemInput.addEventListener('blur', function (e) {
        setTimeout(function () {
            itemDropdown.classList.add('hide');
        }, 100);
    });

    // * dropdown click
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

            clickCheckBox(false)
            itemDropdown.classList.add('hide');
        }
    });

    document.querySelector('i.fa-floppy-disk').addEventListener('click', () => {
        // send to backend
        document.querySelectorAll('new-item').forEach(el => {
            const itemsData = [];
            // list of dict?
            dict = {
                'id': el.dataset.id,
                'itemname': el.dataset.itemName,
                'price': el.dataset.price,
                'brand': el.dataset.brand,
                'weight': el.dataset.weight,
                'travexp': el.dataset.travexp
            }
            itemsData.push(dict)
        })
        
        axios.post(window.location.pathname, {
            'itemList': itemsData
        })
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });

    })





});

function disableForms() {
    const inputsToDisable = document.querySelectorAll('#item, #brand, #weight');
    inputsToDisable.forEach(input => {
        input.disabled = this.checked;
    });
}

function resetForm() {
    document.querySelectorAll('input[type="text"], input[type="number"]').forEach(input => {
        input.value = '';
        input.disabled = false
    });

    const existingItemCheckbox = document.getElementById('existingItem');
    existingItemCheckbox.checked = false;
    existingItemCheckbox.disabled = true;
}
function clickCheckBox(disableAfter) {
    const existingItemCheckbox = document.querySelector('#existingItem');
    existingItemCheckbox.disabled = false
    existingItemCheckbox.click()
    if (disableAfter) {
        existingItemCheckbox.disabled = true
    }
}
