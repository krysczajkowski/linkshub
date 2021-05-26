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
                location.reload();
            }
        });
    })
})

const custom_bg_submit = document.querySelector('#custom_bg_submit')
custom_bg_submit.addEventListener('click', event => {
  // Spinngin effect
  custom_bg_submit.disabled = true
  document.querySelector('#submitSpinner').classList.remove('d-none')

  // Submit form 
  document.querySelector('#custom_bg_form').submit()
})