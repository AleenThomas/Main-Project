document.addEventListener('DOMContentLoaded', function () {
    var firstNameInput = document.getElementById('fName');
    var lastNameInput = document.getElementById('sName');
    var emailInput = document.getElementById('eMail');
    var phoneInput = document.getElementById('phone');
    var cityInput = document.getElementById('ciTy');
    var zipInput = document.getElementById('zIp');
    var stateInput = document.getElementById('sTate');
    var streetInput = document.getElementById('Street');

    firstNameInput.addEventListener('input', function () {
        validateName(this, 'firstNameError');
    });

    lastNameInput.addEventListener('input', function () {
        validateName(this, 'lastNameError');
    });

    emailInput.addEventListener('input', function () {
        validateEmail(this, 'emailError');
    });

    phoneInput.addEventListener('input', function () {
        validatePhoneNumber(this, 'phoneError');
    });

    cityInput.addEventListener('input', function () {
        validateCity(this, 'cityError');
    });

    zipInput.addEventListener('input', function () {
        validateZipCode(this, 'zipError');
    });

    stateInput.addEventListener('input', function () {
        validateState(this, 'stateError');
    });

    streetInput.addEventListener('input', function () {
        validateStreet(this, 'streetError');
    });

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
            setErrorMessage(errorElement, 'Should contain only alphabets');
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
        var regex = /^\d{10}$/;

        if (!regex.test(inputValue)) {
            setErrorMessage(errorElement, 'Invalid phone number (10 digits)');
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
        var regex = /^\d{5}$/;

        if (!regex.test(inputValue)) {
            setErrorMessage(errorElement, 'Invalid zip code (5 digits)');
        } else {
            clearErrorMessage(errorElement);
        }
    }

    // ... Add more validation functions as needed ...
});
