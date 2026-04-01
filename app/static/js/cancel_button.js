cancelButton = document.querySelector('.js-cancel-button');
cancelButton.addEventListener('click', () => {
    window.location.href = cancelButton.dataset.referrer;
});

