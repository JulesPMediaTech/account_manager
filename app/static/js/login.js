const passwordInput = document.querySelector('input[name="password"]') ;
const showPasswordCheckBox = document.getElementById('js-show-password-checkbox');

showPasswordCheckBox.addEventListener('change', () => {
    passwordInput.type = showPasswordCheckBox.checked ? 'text' : 'password';
});