const activeLinkSlider = document.querySelectorAll('.active_link_slider')
const deleteLink = document.querySelectorAll('.delete-link-btn')

// Activate link toggle
activeLinkSlider.forEach(item => {
    item.addEventListener('change', event => {
        const is_active = item.checked
        const link_id = item.id
        
        fetch('/profile/links/activate', {
            body: JSON.stringify({'is_active': is_active, 'link_id': link_id, 'link_type': link_type}),
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
            }
        });
    })
})


// Delete link
deleteLink.forEach(item => {
    item.addEventListener('click', event => {
        const link_id = item.id

        // Deleting effect
        item.disabled = true
        document.querySelector(`.deleteSpinner-${link_id}`).classList.remove('d-none')

        fetch('/profile/links/delete', {
            body: JSON.stringify({'link_id': link_id, 'link_type': link_type}),
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
                location.reload();
            }
        }); 

    })
})
