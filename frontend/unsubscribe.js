document.addEventListener('DOMContentLoaded', () => {
    const unsubscribeForm = document.getElementById('unsubscribe-form');

    unsubscribeForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const emailInput = document.getElementById('email');
        const email = emailInput.value;
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';
        unsubscribeForm.appendChild(messageDiv);

        try {
            const response = await fetch('http://localhost:8000/unsubscribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: email }),
            });

            const result = await response.json();

            if (response.ok) {
                messageDiv.textContent = 'You have been successfully unsubscribed.';
                messageDiv.style.color = '#2e7d32';
                unsubscribeForm.reset();
            } else {
                messageDiv.textContent = result.detail || 'An error occurred. Please try again.';
                messageDiv.style.color = '#d32f2f';
            }
        } catch (error) {
            messageDiv.textContent = 'Could not connect to the server. Please try again later.';
            messageDiv.style.color = '#d32f2f';
        }

        setTimeout(() => messageDiv.remove(), 5000);
    });
});
