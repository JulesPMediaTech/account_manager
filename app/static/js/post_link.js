document.addEventListener('DOMContentLoaded', () => {
    // Find all elements that should act as a POST link
    const postLinks = document.querySelectorAll('.js-post-link');

    postLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault(); // Stop the default link/button behavior

            const linkElement = event.currentTarget;
            const { action, userId, redir, confirmMessage } = linkElement.dataset;

            // If a confirmation message is set, show a confirm dialog
            if (confirmMessage && !confirm(confirmMessage)) {
                return; // User clicked 'Cancel', so we stop
            }

            // Create a temporary form
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = action;

            // --- Helper function to add hidden inputs ---
            const addInput = (name, value) => {
                if (value) { // Only add the input if the value exists
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = name;
                    input.value = value;
                    form.appendChild(input);
                }
            };

            // Add required data to the form
            addInput('user_id', userId);
            addInput('redir', redir);
            
            // Add CSRF token
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            addInput('csrf_token', csrfToken);

            // Submit the form
            document.body.appendChild(form);
            form.submit();
        });
    });
});