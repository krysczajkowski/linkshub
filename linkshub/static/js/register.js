// Fetch submit button
const submitBtn = document.querySelector('#submitBtn')

// Username validation
const usernameField = document.querySelector('#usernameField')
const usernameFeedback = document.querySelector('.username-feedback')

usernameField.addEventListener('keyup', (e) => {
    const usernameValue = e.target.value;

    usernameField.classList.remove('is-invalid')
    usernameField.classList.remove('is-valid')
    usernameFeedback.style.display = 'none'

    if (usernameValue.length > 0) {
        fetch('/authentication/validate-username', {
            body: JSON.stringify({'username': usernameValue}),
            method: 'POST',
        }).then(res=>res.json()).then(data=>{
            console.log('data', data)
            if(data.username_error) {
                // Dispable submit button
                submitBtn.setAttribute('disabled', 'disabled')
                submitBtn.disabled = true

                usernameField.classList.add('is-invalid')

                usernameFeedback.style.display = 'block'
                usernameFeedback.innerHTML = `<p>${data.username_error}</p>`
            } else {
                submitBtn.removeAttribute('disabled')

                usernameField.classList.remove('is-invalid')
                usernameField.classList.add('is-valid')
            }
        });
    }
})


// Email validation
const emailField = document.querySelector('#emailField')
const emailFeedback = document.querySelector('.email-feedback')

emailField.addEventListener('focusout', (e) => {
    const emailValue = e.target.value;

    emailFeedback.classList.remove('is-invalid')
    emailFeedback.classList.remove('is-valid')
    emailFeedback.style.display = 'none'

    fetch('/authentication/validate-email', {
        body: JSON.stringify({'email': emailValue}),
        method: 'POST',
    }).then(res=>res.json()).then(data=>{
        console.log('data', data)
        if(data.email_error) {
            // Dispable submit button
            submitBtn.setAttribute('disabled', 'disabled')
            submitBtn.disabled = true
            emailField.classList.add('is-invalid')

            emailFeedback.style.display = 'block'
            emailFeedback.innerHTML = `<p>${data.email_error}</p>`
        } else {
            submitBtn.removeAttribute('disabled')

            emailField.classList.remove('is-invalid')
            emailField.classList.add('is-valid')
        }
    });
})


// Password validation
const passwordField = document.querySelector('#passwordField')
const passwordFeedback = document.querySelector('.password-feedback')

passwordField.addEventListener('focusout', (e) => {
    const passwordValue = e.target.value;

    passwordField.classList.remove('is-invalid')
    passwordField.classList.remove('is-valid')
    passwordFeedback.style.display = 'none'

    fetch('/authentication/validate-password', {
        body: JSON.stringify({'password': passwordValue}),
        method: 'POST',
    }).then(res=>res.json()).then(data=>{
        console.log('data', data)
        if(data.password_error) {
            // Dispable submit button
            submitBtn.setAttribute('disabled', 'disabled')
            submitBtn.disabled = true
            passwordField.classList.add('is-invalid')

            passwordFeedback.style.display = 'block'
            passwordFeedback.innerHTML = `<p>${data.password_error}</p>`
        } else {
            submitBtn.removeAttribute('disabled')

            passwordField.classList.remove('is-invalid')
            passwordField.classList.add('is-valid')
        }
    });
})


// Show password toggle
const showPasswordToggle = document.querySelector('.showPasswordToggle')

function handleToggleInput(e) {
    if (showPasswordToggle.innerHTML == '<i class="far fa-eye" aria-hidden="true"></i>') {
        showPasswordToggle.innerHTML = '<i class="far fa-eye-slash"></i>'

        passwordField.setAttribute('type', 'text')
    } else {
        showPasswordToggle.innerHTML = '<i class="far fa-eye"></i>'

        passwordField.setAttribute('type', 'password')
    }
}

showPasswordToggle.addEventListener('click', handleToggleInput)


// Checkbox validation
const form = document.getElementById('registration_form')
const terms_checkbox = document.querySelector('#terms')
const privacy_checkbox = document.querySelector('#privacy_policy')
const checkboxFeedback = document.querySelector('.checkbox-feedback')

form.addEventListener('submit', (event) => {
    // stop form submission
    event.preventDefault();

    if (terms_checkbox.checked == false || privacy_checkbox.checked == false) {
        checkboxFeedback.style.display = 'block'
        checkboxFeedback.innerHTML = '<p>All checkbox are required.</p>'
    } else {
        form.submit()
    }
});
