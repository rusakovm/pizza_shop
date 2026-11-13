let btnPass = document.querySelector('.password-checkbox');
    inputPass = document.querySelector('.input-pass')


btnPass.onclick = function() {
    if(inputPass.getAttribute('type') === 'password'){
        inputPass.setAttribute('type', 'text');
    } else {
        inputPass.setAttribute('type', 'password');
    }
}







