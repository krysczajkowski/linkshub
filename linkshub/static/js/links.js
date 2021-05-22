const activeLinkSlider = document.querySelectorAll('.active_link_slider')

activeLinkSlider.forEach(item => {
    item.addEventListener('change', event => {
        const is_active = item.checked
        const link_id = item.id
        
        fetch('links/activate', {
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

  