
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registerForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('password-repeat');
    const nameInput = document.getElementById('name');
  
    // Function to validate email
    function validateEmail() {
      const emailError = document.getElementById('email-error');
  
      if (!isValidEmail(emailInput.value)) {
        emailInput.classList.add('is-invalid');
        emailError.innerText = 'Please enter a valid email address.';
      } else {
        console.log("Entered");
        emailInput.classList.remove('is-invalid');
        emailError.innerText = '';
      }
    }
  
    // Function to validate password
    function validatePassword() {
      const passwordError = document.getElementById('password-error');
      const password = passwordInput.value;
  
      const errors = [];
      if (password.length < 6) {
        errors.push('Atleast 6 chars.');
      }
      if (!containsUppercase(password)) {
        errors.push('requires Uppercase,');
      }
      if (!containsLowercase(password)) {
        errors.push('Lowercasse,');
      }
      if (!containsSpecialCharacter(password)) {
        errors.push('Number.');
      }
      if(!containsNumber(password)) {
        errors.push('special symbol .');
      }
  
      if (errors.length > 0) {
        passwordInput.classList.add('is-invalid');
        passwordError.innerText = errors.join(' ');
      } else {
        passwordInput.classList.remove('is-invalid');
        passwordError.innerText = '';
      }
  
      validateConfirmPassword();
    }
  
    // Function to validate confirm password
    function validateConfirmPassword() {
      const confirmPasswordError = document.getElementById('password-repeat-error');
  
      if (confirmPasswordInput.value !== passwordInput.value) {
        confirmPasswordInput.classList.add('is-invalid');
        confirmPasswordError.innerText = 'Passwords do not match.';
      } else {
        confirmPasswordInput.classList.remove('is-invalid');
        confirmPasswordError.innerText = '';
      }
    }
  
    function validateName() {
      const nameError = document.getElementById('name-error');
      const name = nameInput.value.trim();
      const namePattern = /^[a-zA-Z ]+$/;
  
      if (!namePattern.test(name)) {
        nameInput.classList.add('is-invalid');
        nameError.innerText = 'Please enter a valid name.';
      } else {
        nameInput.classList.remove('is-invalid');
        nameError.innerText = '';
      }
    }
  
    // Helper functions for validation
    function containsUppercase(text) {
      return /[A-Z]/.test(text);
    }
  
    function containsLowercase(text) {
      return /[a-z]/.test(text);
    }
  
    function containsSpecialCharacter(text) {
      return /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(text);
    }
  
    function isValidEmail(email) {
      const emailRegex =  /^[a-zA-Z0-9._%+-]+@[a-z]+\.[a-zA-Z]+(?:\.[a-zA-Z]+)?$/;;
      return emailRegex.test(email);
    }
    function containsNumber(text) {
      return /[0-9]/.test(text);
    }
    // Event listeners for instant validation
    emailInput.addEventListener('input', validateEmail);
    passwordInput.addEventListener('input', validatePassword);
    confirmPasswordInput.addEventListener('input', validateConfirmPassword);
    nameInput.addEventListener('input', validateName);
  
    // Form submit event listener for final validation before submission
    form.addEventListener('submit', function (event) {
      validateEmail();
      validatePassword();
      validateConfirmPassword();
      validateName();
  
      if (emailInput.classList.contains('is-invalid') || passwordInput.classList.contains('is-invalid') || nameInput.classList.contains('is-invalid')){
        event.preventDefault();
      }
    });
  });
  