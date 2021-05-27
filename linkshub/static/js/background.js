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



theme = document.querySelectorAll('.theme-contrainer')
// Choose a theme
theme.forEach(item => {
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
const custom_bg_submit = document.querySelector('#custom_bg_submit')

custom_bg_submit.addEventListener('click', event => {
    // Add spinnig effect
    custom_bg_submit.disabled = true
    document.querySelector('#submitSpinner').classList.remove('d-none')
 
    // Delete spinning effect after .5s 
    setTimeout((e) => {
        custom_bg_submit.disabled = false
        document.querySelector('#submitSpinner').classList.add('d-none')
    }, 500);

    // Get data
    bg_color = document.querySelector('#background_color').value 
    font_color = document.querySelector('#font_color').value 

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