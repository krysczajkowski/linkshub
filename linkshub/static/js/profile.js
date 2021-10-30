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

// Premium Link click counter
function count_premium_links_clicks() {
    var premium_links = document.querySelectorAll('.premium-link-click')
    premium_links.forEach(link => {
        link.addEventListener('click', (e) => {
            const link_id = link.id 

            fetch('dashboard/premium_link_click', {
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
}

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


// Register visitor
fetch('dashboard/register_visitor', {
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
    }
});