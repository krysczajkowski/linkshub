const activeLinkSlider = document.querySelectorAll('.active_link_slider')
const deleteLink = document.querySelectorAll('.delete-link-btn')

// Activate link toggle
activeLinkSlider.forEach(item => {
    item.addEventListener('change', event => {
        const is_active = item.checked
        const link_id = item.id
        
        fetch('activate', {
            body: JSON.stringify({'is_active': is_active, 'link_id': link_id}),
            method: 'POST',
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

        fetch('delete', {
            body: JSON.stringify({'link_id': link_id}),
            method: 'POST',
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
