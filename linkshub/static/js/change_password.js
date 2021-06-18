// CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


// Show password toggle
function handleToggleInput(showPasswordToggle, passwordField) {
    if (showPasswordToggle.innerHTML == '<i class="far fa-eye" aria-hidden="true"></i>') {
        showPasswordToggle.innerHTML = '<i class="far fa-eye-slash"></i>'

        passwordField.setAttribute('type', 'text')
    } else {
        showPasswordToggle.innerHTML = '<i class="far fa-eye"></i>'

        passwordField.setAttribute('type', 'password')
    }
}

// Check if your current password is right
const current_password = document.querySelector('#current_password')
const current_passwordFeedback = document.querySelector('.current_password_feedback')

current_password.addEventListener('focusout', (e) => {
    console.log('xd')
    const passwordValue = e.target.value;

    current_password.classList.remove('is-invalid')
    current_password.classList.remove('is-valid')
    current_passwordFeedback.style.display = 'none'

    fetch('/settings/edit/password/check-current-password', {
        body: JSON.stringify({'password': passwordValue}),
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken
          },
    }).then(res=>res.json()).then(data=>{
        console.log('data', data)
        if(data.password_error) {
            // Dispable submit button
            submitBtn.setAttribute('disabled', 'disabled')
            submitBtn.disabled = true
            current_password.classList.add('is-invalid')

            current_passwordFeedback.style.display = 'block'
            current_passwordFeedback.innerHTML = `<p>${data.password_error}</p>`
        } else {
            submitBtn.removeAttribute('disabled')

            current_password.classList.remove('is-invalid')
            current_password.classList.add('is-valid')
        }
    });
})

// Validate new password (length etc)

// Check if 2 passwords are the same
