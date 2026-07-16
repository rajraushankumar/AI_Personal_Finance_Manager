// Password Show / Hide

const togglePassword = document.getElementById("togglePassword");
const password = document.getElementById("password");

togglePassword.addEventListener("click", function () {

    if (password.type === "password") {

        password.type = "text";
        this.classList.replace("fa-eye", "fa-eye-slash");

    } else {

        password.type = "password";
        this.classList.replace("fa-eye-slash", "fa-eye");

    }

});

// Confirm Password Show / Hide

const toggleConfirmPassword = document.getElementById("toggleConfirmPassword");
const confirmPassword = document.getElementById("confirmPassword");

toggleConfirmPassword.addEventListener("click", function () {

    if (confirmPassword.type === "password") {

        confirmPassword.type = "text";
        this.classList.replace("fa-eye", "fa-eye-slash");

    } else {

        confirmPassword.type = "password";
        this.classList.replace("fa-eye-slash", "fa-eye");

    }

});

// Password Match Validation

const form = document.getElementById("registerForm");
const error = document.getElementById("error");

form.addEventListener("submit", function (e) {

    if (password.value !== confirmPassword.value) {

        e.preventDefault();

        error.textContent = "Passwords do not match.";

    } else {

        error.textContent = "";

    }

});