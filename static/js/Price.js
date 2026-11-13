const sw1 = document.querySelector('#quantity1');

const basePrice1 = 350;

sw1.addEventListener('input', function () {
    calculate1();
})

function calculate1 () {
    let totalPrice1 = basePrice1 * parseInt(sw1.value);
    console.log(totalPrice1);

    const formatter1 = new Intl.NumberFormat('ru')


    totalPriceEl1.innerText = formatter1.format(totalPrice1);
}
calculate1 ()



const sw2 = document.querySelector('#quantity2');

const basePrice2 = 540;

sw2.addEventListener('input', function () {
    calculate2();
})

function calculate2 () {
    let totalPrice2 = basePrice2 * parseInt(sw2.value);
    console.log(totalPrice2);

    const formatter2 = new Intl.NumberFormat('ru')


    totalPriceEl2.innerText = formatter2.format(totalPrice2);
}
calculate2 ()


const sw3 = document.querySelector('#quantity3');

const basePrice3 = 700;

sw3.addEventListener('input', function () {
    calculate3();
})

function calculate3 () {
    let totalPrice3 = basePrice3 * parseInt(sw3.value);
    console.log(totalPrice3);

    const formatter3 = new Intl.NumberFormat('ru')


    totalPriceEl3.innerText = formatter3.format(totalPrice3);
}

calculate3 ()

