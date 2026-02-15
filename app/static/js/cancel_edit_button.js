cancelButton = document.querySelector('.js-cancel-add-user-button');
cancelButton.addEventListener('click', () => {
    window.location.href = cancelButton.dataset.referrer;
});
