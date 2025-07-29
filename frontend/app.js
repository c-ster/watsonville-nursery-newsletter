document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signup-form');

        signupForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const emailInput = document.getElementById('email');
        const email = emailInput.value;
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';
        signupForm.appendChild(messageDiv);

        try {
            const response = await fetch('http://localhost:8000/subscribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email: email }),
            });

            const result = await response.json();

            if (response.ok) {
                messageDiv.textContent = 'Thank you for subscribing!';
                messageDiv.style.color = '#2e7d32';
                signupForm.reset();
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
