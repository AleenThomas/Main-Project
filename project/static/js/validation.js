document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('registerForm');
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');
  const confirmPasswordInput = document.getElementById('password-repeat');
  const nameInput = document.getElementById('name');

  function validateEmail() {
    const emailError = document.getElementById('email-error');

    if (!isValidEmail(emailInput.value)) {
      emailInput.classList.add('is-invalid');
      emailError.innerText = 'Please enter a valid email address.';
      emailError.style.color = 'red';
      emailError.style.fontSize = '12px';
    } else {
      emailInput.classList.remove('is-invalid');
      emailError.innerText = '';
    }
  }

  function validatePassword() {
    const passwordError = document.getElementById('password-error');
    const password = passwordInput.value;

    const errors = [];
    if (password.length < 6) {
      errors.push('Min 6 chars..');
    }
    if (!containsUppercase(password)) {
      errors.push('Uppercase required.');
    }
    if (!containsLowercase(password)) {
      errors.push('Lowercase required.');
    }
    if (!containsSpecialCharacter(password)) {
      errors.push('Special char required.');
    }
    if (!containsNumber(password)) {
      errors.push('Number required');
    }

    if (errors.length > 0) {
      passwordInput.classList.add('is-invalid');
      passwordError.innerText = errors.join(' ');
      passwordError.style.color = 'red';
      passwordError.style.fontSize = '12px';
      passwordInput.style.borderColor = 'initial';
    } else {
      passwordInput.classList.remove('is-invalid');
      passwordError.innerText = '';
      passwordInput.style.borderColor = 'green';
    }

    validateConfirmPassword();
  }

  function validateConfirmPassword() {
    const confirmPasswordError = document.getElementById('password-repeat-error');

    if (confirmPasswordInput.value !== passwordInput.value) {
      confirmPasswordInput.classList.add('is-invalid');
      confirmPasswordError.innerText = 'Passwords do not match.';
      confirmPasswordError.style.color = 'red';
      confirmPasswordError.style.fontSize = '12px';
      confirmPasswordInput.style.borderColor = 'initial';
    } else {
      confirmPasswordInput.classList.remove('is-invalid');
      confirmPasswordError.innerText = '';
      confirmPasswordInput.style.borderColor = 'green';
    }
  }

  function validateName() {
    const nameError = document.getElementById('name-error');
    const name = nameInput.value.trim();
    const namePattern = /^[a-zA-Z ]+$/;

    if (!namePattern.test(name)) {
      nameInput.classList.add('is-invalid');
      nameError.innerText = 'Please enter a valid name.';
      nameError.style.color = 'red';
      nameError.style.fontSize = '12px';
      nameInput.style.borderColor = 'initial';
    } else {
      nameInput.classList.remove('is-invalid');
      nameError.innerText = '';
      nameInput.style.borderColor = 'green';
    }
  }

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
    const emailRegex = /\S+@\S+\.\S+/;
    return emailRegex.test(email);
  }

  function containsNumber(text) {
    return /[0-9]/.test(text);
  }

  emailInput.addEventListener('input', validateEmail);
  passwordInput.addEventListener('input', validatePassword);
  confirmPasswordInput.addEventListener('input', validateConfirmPassword);
  nameInput.addEventListener('input', validateName);

  form.addEventListener('submit', function (event) {
    validateEmail();
    validatePassword();
    validateConfirmPassword();
    validateName();

    if (emailInput.classList.contains('is-invalid') || passwordInput.classList.contains('is-invalid') || nameInput.classList.contains('is-invalid')) {
      event.preventDefault();
    }
  });
});
