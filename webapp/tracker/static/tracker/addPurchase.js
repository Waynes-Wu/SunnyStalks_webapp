

document.addEventListener('DOMContentLoaded', function () {
    const existingItemCheckbox = document.querySelector('#existingItem');
    const submitButton = document.querySelector('input[type="submit"]');
    const basket = document.querySelector('#basket');

    // * checkbox update enable forms
    existingItemCheckbox.addEventListener('change', disableForms);

    // * for submit button to add to basket
    submitButton.addEventListener('click', function (e) {
        e.preventDefault(); 

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
        


        const newItem = document.createElement('div');
        newItem.classList.add('new-item');

        // add data
        if (existingItemCheckbox.checked) {
            newItem.dataset['id'] = id
        }
        else{
            newItem.dataset['id'] = 0
        }
        newItem.dataset['item'] = itemName
        newItem.dataset['price'] = price
        newItem.dataset['brand'] = brand
        newItem.dataset['weight'] = weight

        newItem.innerHTML = `
        <p>Item: ${itemName}
        Price: ${price}
        Brand: ${brand}
        Weight/Volume: ${weight}`;
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
            itemDropdown.classList.remove('hide');
        });
    });

    // * dropdown show
    searchItemInput.addEventListener('focus', function () {
        itemDropdown.classList.remove('hide');
    });
    // * dropdown show hide
    searchItemInput.addEventListener('blur', function (e) {
        setTimeout( function () {
            itemDropdown.classList.add('hide');
        }, 100);
    });

    // * dropdown click
    itemDropdown.addEventListener('click', function (e) {
        if (e.target.tagName === 'LI') {
            searchItemInput.value = e.target.textContent;
            itemDropdown.classList.remove('show');

            const idInput = document.querySelector('#id');
            const itemNameInput = document.querySelector('#item');
            const priceInput = document.querySelector('#price');
            const brandInput = document.querySelector('#brand');
            const weightInput = document.querySelector('#weight');

            const selectedItemId = e.target.dataset.id;
            const selectedBrand = e.target.dataset.brand;
            const selectedName = e.target.dataset.name;
            const selectedWeight = e.target.dataset.weight;

            idInput.value = selectedItemId;
            itemNameInput.value = selectedName;
            priceInput.value = '';
            brandInput.value = selectedBrand;
            weightInput.value = selectedWeight;

            if (!existingItemCheckbox.checked)
                clickCheckBox(false)
            itemDropdown.classList.add('hide');
        }
    });

    document.querySelector('i.fa-floppy-disk').addEventListener('click', () => {
        // send to backend
        const itemsData = [];
        document.querySelectorAll('.new-item').forEach(el => {
            // list of dict?
            dict = {
                'id': el.dataset.id,
                'itemname': el.dataset.itemName,
                'price': el.dataset.price,
                'brand': el.dataset.brand,
                'weight': el.dataset.weight,
            }
            itemsData.push(dict)
        })

        travelExp = document.querySelector('#travexp').value
        if (travexp == "") {
            travelExp = -1
        }
        axios.defaults.headers.common['X-CSRFToken'] = csrf_token;
        axios.post(window.location.pathname, {
            'itemList': itemsData,
            'travelExp': travelExp
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
    const existingItemCheckbox = document.querySelector('#existingItem');
    inputsToDisable.forEach(input => {
        input.disabled = existingItemCheckbox.checked;
    });
}

function resetForm() {
    document.querySelectorAll('input:not(#travexp):not([type="submit"])').forEach(input => {
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
