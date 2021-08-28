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
var premium_modal = document.getElementById("premium-modal")

// Profile preview
function load_profile (e) {

    var username = 'profile/'

    fetch('get_username', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken
        },
    }).then(res=>res.json()).then(data=>{
        if(data.error) {
            alert(data.error)
        }
        
        username = data['username']

        fetch(`/${username}` /*, options */)
        .then((response) => response.text())
        .then((html) => {
            document.getElementById("profile_preview").innerHTML = html;

            // Get user theme
            var user_id = document.getElementById('user-id').dataset.id
            var profile_container = document.querySelector('.profile-container')

            fetch('/profile/get_user_theme', {
                body: JSON.stringify({'user_id': user_id}),
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json; charset=UTF-8',
                    'X-CSRFToken': csrftoken
                },
            }).then(res=>res.json()).then(data=>{
                if(data.error) {
                    alert(data.error)
                } else {
                    // Style links
                    document.querySelectorAll(".styled-link").forEach((link) => {
                        link.style.backgroundColor = data.data.btn_bg_color;
                        link.style.color = data.data.btn_font_color;
                        link.style.border = `2px solid ${data.data.btn_border_color}`;
                        link.classList.add(data.data.btn_shadow)
                        link.classList.add(data.data.btn_outline)
                    });

                    document.querySelectorAll('.platform-link').forEach((platform) => {
                        platform.style.color = data.data.bg_font_color
                    })

                    // Style background
                    profile_container.style = data.data.bg_bg_color
                    profile_container.style.color = data.data.bg_font_color
                }
            });

        })
        .catch((error) => {
            console.warn(error);
        });

    });


}

// Load profile preview
window.addEventListener('load', (event) => {
    load_profile()
});


// Choose a background theme
bg_theme = document.querySelectorAll('.bg-theme')
bg_theme.forEach(item => {
    item.addEventListener('click', event => {
        const theme_id = item.id

        fetch('background/choose', {
            body: JSON.stringify({'theme_id': theme_id}),
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json; charset=UTF-8',
                'X-CSRFToken': csrftoken
            },
        }).then(res=>res.json()).then(data=>{
            console.log('data', data)
            if(data.error) {
                alert(data.error)
            } else {
                load_profile()
            }
        });
    })
})

// Set custom background theme
var font_color_input = document.querySelector('#bg_font_color')
font_color_input.addEventListener('change', event => {
    // Get data
    font_color = font_color_input.value 

    fetch('background/font/color', {
        body: JSON.stringify({'font_color': font_color}),
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken
        },
    }).then(res=>res.json()).then(data=>{
        console.log('data', data)
        if(data.error) {
            if (data.error == 'no-premium') {
                // Show premium modal
                var premiumModal = new bootstrap.Modal(premium_modal, {});
                premiumModal.show();
                
            } else {
                alert(data.error)
            } 
        } else {
            load_profile()
        }
    });
})


// Set custom background theme
var background_input = document.querySelector('#bg_background_color')
background_input.addEventListener('change', event => {
    // Get data
    bg_color = background_input.value 

    fetch('background/bg/color', {
        body: JSON.stringify({'bg_color': bg_color}),
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken
        },
    }).then(res=>res.json()).then(data=>{
        console.log('data', data)
        if(data.error) {
            if (data.error == 'no-premium') {
                // Show premium modal
                var premiumModal = new bootstrap.Modal(premium_modal, {});
                premiumModal.show();
                
            } else {
                alert(data.error)
            } 
        } else {
            load_profile()
        }
    });
})

// Choose a button theme
button_theme = document.querySelectorAll('.button-theme')
button_theme.forEach(item => {
    item.addEventListener('click', event => {
        const theme_id = item.id

        fetch('button/choose', {
            body: JSON.stringify({'theme_id': theme_id}),
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json; charset=UTF-8',
                'X-CSRFToken': csrftoken
            },
        }).then(res=>res.json()).then(data=>{
            console.log('data', data)
            if(data.error) {
                alert(data.error)
            } else {
                load_profile()
            }
        });
    })
})

// Set button custom background color
var button_bg_custom_color = document.querySelector('#btn_background_color')
button_bg_custom_color.addEventListener('change', event => {

    // Get data
    bg_color = button_bg_custom_color.value 

    fetch('button/bg/color', {
        body: JSON.stringify({'bg_color': bg_color}),
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken
        },
    }).then(res=>res.json()).then(data=>{
        console.log('data', data)
        if(data.error) {
            if (data.error == 'no-premium') {
                // Show premium modal
                var premiumModal = new bootstrap.Modal(premium_modal, {});
                premiumModal.show();
                
            } else {
                alert(data.error)
            } 
        } else {
            load_profile()
        }
    });
})


// Set button custom font color
var button_font_custom_color = document.querySelector('#btn_font_color')
button_font_custom_color.addEventListener('change', event => {
    // Get data
    font_color = button_font_custom_color.value 

    fetch('button/font/color', {
        body: JSON.stringify({'font_color': font_color}),
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken
        },
    }).then(res=>res.json()).then(data=>{
        console.log('data', data)
        if(data.error) {
            if (data.error == 'no-premium') {
                // Show premium modal
                var premiumModal = new bootstrap.Modal(premium_modal, {});
                premiumModal.show();
                
            } else {
                alert(data.error)
            } 
        } else {
            load_profile()
        }
    });
})


// Set button fill to transparent
btn_color_area = document.getElementById('btn-color-area')
btn_transparent = document.getElementById('btn-transparent')
btn_transparent.addEventListener('click', (e) => {
    fetch('button/fill', {
        body: JSON.stringify({'transparent': true, 'filled': false}),
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken
        },
    }).then(res=>res.json()).then(data=>{
        console.log('data', data)
        if(data.error) {
            alert(data.error)
        } else {
            load_profile()
        }
    });
})

// Set button fill to filled
btn_filled = document.getElementById('btn-filled')
btn_filled.addEventListener('click', (e) => {
    fetch('button/fill', {
        body: JSON.stringify({'transparent': false, 'filled': true}),
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken
        },
    }).then(res=>res.json()).then(data=>{
        console.log('data', data)
        if(data.error) {
            alert(data.error)
        } else {
            load_profile()
        }
    });
})

// Change button outline
btn_outline = document.querySelectorAll('.choose_outline')
btn_outline.forEach(item => {
    item.addEventListener('click', (e) => {
        const outline = item.dataset.outline 
    
        fetch('button/outline', {
            body: JSON.stringify({'outline': outline}),
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json; charset=UTF-8',
                'X-CSRFToken': csrftoken
            },
        }).then(res=>res.json()).then(data=>{
            if(data.error) {
                if (data.error == 'no-premium') {
                    // Show premium modal
                    var premiumModal = new bootstrap.Modal(premium_modal, {});
                    premiumModal.show();
                    
                } else {
                    alert(data.error)
                } 
            } else {
                load_profile()
            }
        });
    
    })
})

// Change button shadow
btn_shadow = document.querySelectorAll('.choose_shadow')
btn_shadow.forEach(item => {
    item.addEventListener('click', (e) => {
        const shadow = item.dataset.shadow 
        console.log(shadow)
    
        fetch('button/shadow', {
            body: JSON.stringify({'shadow': shadow}),
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json; charset=UTF-8',
                'X-CSRFToken': csrftoken
            },
        }).then(res=>res.json()).then(data=>{
            console.log('data', data)
            if(data.error) {
                if (data.error == 'no-premium') {
                    // Show premium modal
                    var premiumModal = new bootstrap.Modal(premium_modal, {});
                    premiumModal.show();
                    
                } else {
                    alert(data.error)
                } 
            } else {
                load_profile()
            }
        });
    
    })
})


// Click to copy
const click_to_copy = document.querySelector('#click-to-copy')
const click_to_copy_text = document.querySelector('#click-to-copy-text')
const click_to_copy_link = document.querySelector('#click-to-copy-link')
link = click_to_copy_link.textContent

var click_counter = 0

function resetCopyMessage() {
    // Set text back to Click To Copy
    reset = setTimeout(()=>{
        click_to_copy_text.innerHTML = 'Click To Copy' 
    }, 2000)
}

function displayNewCopyMessage(msg, color) {
    if(color == 'green') {
        click_to_copy_text.innerHTML = `<span class="text-success">${msg}</span>`
    } else if (color == 'yellow') {
        click_to_copy_text.innerHTML = `<span class="text-warning">${msg}</span>` 
    } else if (color == 'red') {
        click_to_copy_text.innerHTML = `<p class="text-danger m-0 p-0 animate__animated animate__shakeX animate__infinite">${msg}</p>` 
    }

    clearTimeout(reset);
    resetCopyMessage()
}

click_to_copy.addEventListener('click', () => {

    if (click_counter == 0) {
        // Set message that link was copied
        click_to_copy_text.innerHTML = 'Copied!'
        click_counter = 1
        resetCopyMessage()

    } else if (click_counter == 1) {
        displayNewCopyMessage('Double Copy!', 'green')
        click_counter = 2

    } else if (click_counter == 2) {
        displayNewCopyMessage('Tripple Copy!', 'green')
        click_counter = 3

    } else if (click_counter == 3) {
        displayNewCopyMessage('Dominating!!', 'green')
        click_counter = 4

    } else if (click_counter == 4) {
        displayNewCopyMessage('Rampage!!', 'green')
        click_counter = 5

    } else if (click_counter == 5) {
        displayNewCopyMessage('Mega Copy!!', 'green')
        click_counter = 6

    } else if (click_counter == 6) {
        displayNewCopyMessage('Unstoppable!!', 'green')
        click_counter = 7

    } else if (click_counter == 7) {
        displayNewCopyMessage('Wicked Sick!!', 'yellow')
        click_counter = 8

    } else if (click_counter == 8) {
        displayNewCopyMessage('Monster Copy!!', 'yellow')
        click_counter = 9

    } else if (click_counter == 9) {
        displayNewCopyMessage('GODLIKE!!!', 'red')
        click_counter = 10
        
    } else if (click_counter == 10) {
        displayNewCopyMessage('BEYOND GODLIKE!!!', 'red')
        
    }

    // Copy to clipboard
    var tempInput = document.createElement("input");
    tempInput.value = link;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);
})