document.addEventListener('DOMContentLoaded', function () {
    var firstNameInput = document.getElementById('fName');
    var lastNameInput = document.getElementById('sName');
    var emailInput = document.getElementById('eMail');
    var phoneInput = document.getElementById('phone');
    var cityInput = document.getElementById('ciTy');
    var zipInput = document.getElementById('zIp');
    var stateInput = document.getElementById('sTate');
    var streetInput = document.getElementById('Street');
    var form = document.getElementById('profileform');

    // Validation functions
    function setErrorMessage(errorElement, message) {
        errorElement.innerHTML = `<span style="color: red;">${message}</span>`;
    }

    function clearErrorMessage(errorElement) {
        errorElement.textContent = '';
    }

    function validateName(input, errorId) {
        var inputValue = input.value;
        var errorElement = document.getElementById(errorId);
        var regex = /^[a-zA-Z]+$/;

        if (!regex.test(inputValue)) {
            setErrorMessage(errorElement, 'Should contain only letters');
        } else {
            clearErrorMessage(errorElement);
        }
    }

    function validateEmail(input, errorId) {
        var inputValue = input.value;
        var errorElement = document.getElementById(errorId);
        var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!regex.test(inputValue)) {
            setErrorMessage(errorElement, 'Invalid email format');
        } else {
            clearErrorMessage(errorElement);
        }
    }

    function validatePhoneNumber(input, errorId) {
        var inputValue = input.value;
        var errorElement = document.getElementById(errorId);
        var regex = /^[6789]\d{9}$/;

        if (!regex.test(inputValue)) {
            setErrorMessage(errorElement, 'Invalid phone number (10 digits starting with 6, 7, 8, or 9)');
        } else {
            clearErrorMessage(errorElement);
        }
    }

    function validateStreet(input, errorId) {
        var inputValue = input.value;
        var errorElement = document.getElementById(errorId);

        if (inputValue.trim() === '') {
            setErrorMessage(errorElement, 'Street cannot be empty');
        } else {
            clearErrorMessage(errorElement);
        }
    }

    function validateCity(input, errorId) {
        var inputValue = input.value;
        var errorElement = document.getElementById(errorId);
        var regex = /^[a-zA-Z\s]+$/;

        if (!regex.test(inputValue)) {
            setErrorMessage(errorElement, 'Invalid city name');
        } else {
            clearErrorMessage(errorElement);
        }
    }

    function validateState(input, errorId) {
        var inputValue = input.value;
        var errorElement = document.getElementById(errorId);
        var regex = /^[a-zA-Z\s]+$/;

        if (!regex.test(inputValue)) {
            setErrorMessage(errorElement, 'Invalid state name');
        } else {
            clearErrorMessage(errorElement);
        }
    }

    function validateZipCode(input, errorId) {
        var inputValue = input.value;
        var errorElement = document.getElementById(errorId);
        var regex = /^[1-9]\d{5}$/;

        if (!regex.test(inputValue)) {
            setErrorMessage(errorElement, 'Invalid zip code (6 digits starting from 1 to 9)');
        } else {
            clearErrorMessage(errorElement);
        }
    }

    // Real-time keyup event listeners for validation
  

    // Real-time keyup event listeners for validation
    firstNameInput.addEventListener('keyup', function () {
        validateName(this, 'firstNameError');
    });

    lastNameInput.addEventListener('keyup', function () {
        validateName(this, 'lastNameError');
    });

    emailInput.addEventListener('keyup', function () {
        validateEmail(this, 'emailError');
    });

    phoneInput.addEventListener('keyup', function () {
        validatePhoneNumber(this, 'phoneError');
    });

    cityInput.addEventListener('keyup', function () {
        validateCity(this, 'cityError');
    });

    zipInput.addEventListener('keyup', function () {
        validateZipCode(this, 'zipError');
    });

    stateInput.addEventListener('keyup', function () {
        validateState(this, 'stateError');
    });

    // Form submission and clearing invalid data functions
    firstNameInput.addEventListener('keyup', function () {
        validateName(this, 'firstNameError');
        checkFormValidity();
    });

    lastNameInput.addEventListener('keyup', function () {
        validateName(this, 'lastNameError');
        checkFormValidity();
    });

    emailInput.addEventListener('keyup', function () {
        validateEmail(this, 'emailError');
        checkFormValidity();
    });

    phoneInput.addEventListener('keyup', function () {
        validatePhoneNumber(this, 'phoneError');
        checkFormValidity();
    });

    cityInput.addEventListener('keyup', function () {
        validateCity(this, 'cityError');
        checkFormValidity();
    });

    zipInput.addEventListener('keyup', function () {
        validateZipCode(this, 'zipError');
        checkFormValidity();
    });

    stateInput.addEventListener('keyup', function () {
        validateState(this, 'stateError');
        checkFormValidity();
    });

    function checkFormValidity() {
        var errorMessages = document.querySelectorAll('.error-message');
        var isFormValid = true;

        errorMessages.forEach(function (errorMessage) {
            if (errorMessage.textContent !== '') {
                isFormValid = false;
            }
        });

        if (!isFormValid) {
            form.querySelector('button[type="submit"]').disabled = true;
        } else {
            form.querySelector('button[type="submit"]').disabled = false;
        }
    }

    form.addEventListener('submit', function (event) {
        // Prevent form submission if there are errors
        if (!checkFormValidity()) {
            event.preventDefault();
        }
    });
    // ... Rest of your code ...
});
