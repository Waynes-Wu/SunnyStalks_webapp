document.addEventListener('DOMContentLoaded', () => {

    const selects = document.querySelectorAll('select')
    const card = document.querySelectorAll('.compare-branch-card')
    const itemlist = document.querySelectorAll('.ITEMSLIST');

    const select1 = selects[0]
    const select2 = selects[1]

    selects.forEach((el, index )=> {
        el.addEventListener('change', () => {
            axios.get('/api/branch', {
                params: {
                    id: el.value,
                }
            }).then(response => {
                let temp = response.data
                console.log(temp)
                const infoField = card[index].querySelectorAll('.row')
                infoField[0].innerHTML = temp.name.toUpperCase()
                infoField[1].innerHTML = temp.address
                card[index].querySelector('img').src = temp.image

            })
            .catch(error => {
                console.error(error);
            });
            console.log(select1.value)

            // clear bottom part
            itemlist.forEach(el => {
                el.innerHTML=``
            })



            if (select1.value == 0 || select2.value == 0) {
                return
            }
            else if (select1.value == select2.value){
                return
            }
            else {

                let s1 = select1.value
                let s2 = select2.value
                // get data from backend

                axios.get('/api/compare', {
                    params: {
                        grocer1_id: select1.value,
                        grocer2_id: select2.value,
                    }
                })
                    .then(response => {
                        console.log(response.data);
                        data = response.data
                        
                        data.common_with_prices.forEach(el=>{
                            itemlist[1].innerHTML += 
                            ` <div class="mb-3 compare-item">
                                <div style="display: flex; justify-content: space-between;">
                                    <span class="font-inter-compareitem" style="font-weight: 700;">
                                        ${ el.item.brand }
                                    </span>
                                    <span class="font-inter-compareitem" style="font-weight: 700;">
                                    ₱${ el.price_A } - ₱${ el.price_B }
                                    </span>
                                </div>
                                <p class="font-inter-compareitem">
                                    ${ el.item.name }
                                </p>
                            </div>`
                        })
                        data.diffA_with_prices.forEach(el=>{
                            itemlist[0].innerHTML += `<div class="mb-5 compare-item">
                            <div style="display: flex; justify-content: space-between;">
                                <span class="font-inter-compareitem" style="font-weight: 700;">
                                ${ el.item.brand }
                                </span>
                                <span class="font-inter-compareitem" style="font-weight: 700;">
                                    ₱${ el.price }
                                    </span>
                            </div>
                            <p class="font-inter-compareitem">${ el.item.name }</p>
                        </div>`
                        })

                        data.diffB_with_prices.forEach(el=>{
                            itemlist[2].innerHTML += `<div class="mb-5 compare-item">
                            <div style="display: flex; justify-content: space-between;">
                                <span class="font-inter-compareitem" style="font-weight: 700;">
                                ${ el.item.brand }
                                </span>
                                <span class="font-inter-compareitem" style="font-weight: 700;">
                                    ₱${ el.price }
                                    </span>
                            </div>
                            <p class="font-inter-compareitem">${ el.item.name }</p>
                        </div>`
                        })
                        
                    })
                    .catch(error => {
                        console.error(error);
                    });




                

            }
        });
    })
})
