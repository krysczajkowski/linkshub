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

