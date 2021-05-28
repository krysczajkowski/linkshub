function load_profile (e) {

    fetch("/profile/" /*, options */)
    .then((response) => response.text())
    .then((html) => {
        document.getElementById("profile_preview").innerHTML = html;
    })
    .catch((error) => {
        console.warn(error);
    });
}

window.addEventListener('load', (event) => {
    load_profile()
});

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



bg_theme = document.querySelectorAll('.bg-theme')
// Choose a background theme
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
const bg_custom_submit = document.querySelector('#bg_custom_submit')

bg_custom_submit.addEventListener('click', event => {
    // Add spinnig effect
    bg_custom_submit.disabled = true
    document.querySelector('#bg_submitSpinner').classList.remove('d-none')
 
    // Delete spinning effect after .5s 
    setTimeout((e) => {
        bg_custom_submit.disabled = false
        document.querySelector('#bg_submitSpinner').classList.add('d-none')
    }, 500);

    // Get data
    bg_color = document.querySelector('#bg_background_color').value 
    font_color = document.querySelector('#bg_font_color').value 

    fetch('background/custom/choose', {
        body: JSON.stringify({'bg_color': bg_color, 'font_color': font_color}),
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


button_theme = document.querySelectorAll('.button-theme')
// Choose a button theme
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


// Set custom button theme
const btn_custom_submit = document.querySelector('#btn_custom_submit')

btn_custom_submit.addEventListener('click', event => {
    // Add spinnig effect
    btn_custom_submit.disabled = true
    document.querySelector('#btn_submitSpinner').classList.remove('d-none')
 
    // Delete spinning effect after .5s 
    setTimeout((e) => {
        btn_custom_submit.disabled = false
        document.querySelector('#btn_submitSpinner').classList.add('d-none')
    }, 500);

    // Get data
    bg_color = document.querySelector('#btn_background_color').value 
    font_color = document.querySelector('#btn_font_color').value 

    fetch('button/custom/choose', {
        body: JSON.stringify({'bg_color': bg_color, 'font_color': font_color}),
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