document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registration-form');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const passwordRepeatInput = document.getElementById('password-repeat');
    const agreeInput = document.getElementById('agree');
    const signupButton = document.querySelector('.btn');

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the form from submitting by default

        // Perform your form validation checks here
        if (!isNameValid(nameInput.value.trim())) {
            showErrorMessage('name', 'Name should only contain letters.');
            return;
        } else {
            hideErrorMessage('name');
        }

        if (!isEmailValid(emailInput.value.trim())) {
            showErrorMessage('email', 'Please enter a valid email address.');
            return;
        } else {
            hideErrorMessage('email');
        }

        const passwordValue = passwordInput.value.trim();
        if (passwordValue === '') {
            showErrorMessage('password', 'Please enter a password.');
            return;
        } else if (!isPasswordValid(passwordValue)) {
            showErrorMessage('password', 'Password should contain at least 6 characters including uppercase, lowercase, number, and special symbol.');
            return;
        } else {
            hideErrorMessage('password');
        }

        const passwordRepeatValue = passwordRepeatInput.value.trim();
        if (passwordRepeatValue === '') {
            showErrorMessage('password-repeat', 'Please confirm your password.');
            return;
        } else if (passwordRepeatValue !== passwordValue) {
            showErrorMessage('password-repeat', 'Passwords do not match.');
            return;
        } else {
            hideErrorMessage('password-repeat');
        }

        if (!agreeInput.checked) {
            showErrorMessage('agree', 'Please agree to the license terms.');
            return;
        } else {
            hideErrorMessage('agree');
        }

        // If form is valid, submit the form
        form.submit();
    });

    // Add event listeners for real-time validation...
    nameInput.addEventListener('input', function () {
        if (!isNameValid(this.value.trim())) {
            showErrorMessage('name', 'Name should only contain letters.');
        } else {
            hideErrorMessage('name');
        }
    });

    // ... (similar event listeners for email, password, password-repeat, and agree inputs) ...
});

// ... (rest of your validation functions and code) ...
