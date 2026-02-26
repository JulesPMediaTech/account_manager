const deactivateUserBtn = document.getElementById('js-deactivate-user-btn');
const role = deactivateUserBtn.dataset.userRole;
deactivateUserBtn.disabled = !['super','admin'].includes(role);