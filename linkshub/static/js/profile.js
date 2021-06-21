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

// User data
var user_data = document.querySelector('#user-id')
var user_id = user_data.dataset.id

// Link click counter
var links = document.querySelectorAll('.link-click')
links.forEach(link => {
    link.addEventListener('click', (e) => {
        const link_id = link.id 

        fetch('dashboard/link_click', {
            body: JSON.stringify({'user_id': user_id, 'link_id': link_id}),
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
        });
    })
})


// Platform click counter
var platforms = document.querySelectorAll('.platform-click')
platforms.forEach(platform => {
    platform.addEventListener('click', (e) => {
        const platform_id = platform.id 

        fetch('dashboard/platform_click', {
            body: JSON.stringify({'user_id': user_id, 'platform_id': platform_id}),
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
        });
    })
})

