//Csrf token
const csrftoken = document.getElementById('csrf-token').dataset.token
var user_id = document.getElementById('user-id').dataset.id

// Get user theme
function get_user_theme() {
    var profile_container = document.querySelector('.profile-container')
    var tutorial_helper_links = document.querySelectorAll('.tutorial-helper-links')
    var write_your_bio = document.getElementById('write-your-bio')

    var linkshub_label = document.getElementById('linkshub-label')


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

            // Style images inside links
            document.querySelectorAll('.link-image-size').forEach((img) => {
                img.classList.add(data.data.btn_outline)
            })

            // Style platforms
            document.querySelectorAll('.platform-link').forEach((platform) => {
                platform.style.color = data.data.bg_font_color
            })

            // Add (or not) linkshub label
            if(data.data.linkshub_label == true) {
                linkshub_label.innerHTML = "<a href='#' class='text-light'>Made with LinksHub.io</a>"
            }


            // Style background
            profile_container.style = data.data.bg_bg_color
            profile_container.style.color = data.data.bg_font_color

            // Style write your bio helper link
            if(write_your_bio) {
                write_your_bio.style.color = data.data.bg_font_color
            }

            // Style tutorial helper links
            tutorial_helper_links.forEach((link) => {
                link.style.color = data.data.bg_font_color;
                link.style.border = `2px dashed ${data.data.bg_font_color}`
            });
        }
    });
}

var premium_links_container = document.getElementById('premium-links-container')
var premium_links_error_msg = document.querySelector('#premium-links-error-msg')
var premium_submit = document.querySelector('#premium-links-submit')
// Check Premium Links password and display links if its correct
if (premium_submit) {
    premium_submit.addEventListener('click', (e) => {
        var premium_links_code = document.getElementById('premium_links_code').value
    
        if (premium_links_code.length > 0) {
            fetch('/profile/premium_links/check_password', {
                body: JSON.stringify({'premium_links_code': premium_links_code, 'user_id': user_id}),
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json; charset=UTF-8',
                    'X-CSRFToken': csrftoken
                },
            }).then(res=>res.json()).then(data=>{
                
                if(data.error) {
                    alert(data.error)
                } else if(data.error_msg) {
                    premium_links_error_msg.innerHTML = `<p class='text-center font-size-08'><span class='rounded text-danger bg-light px-4 py-1'>${data.error_msg}</span></p>`
                } else {
                    premium_links_error_msg.innerHTML = ''
                    premium_links_container.innerHTML = `<p class='font-size-08 fw-bold text-center mb-0'>PREMIUM LINKS</p>`
            
                    data.premium_links.forEach(link => {
                        premium_link_html = `
                        <div class="col-12 col-md-10 offset-md-1 col-xl-8 col-xxl-6 offset-xl-2 offset-xxl-3">
                            <div class="row my-2">
                                <div class="d-grid gap-2">
                                    <a href="${link.url}" id="${link.id}" class="btn mt-2 mx-0 row d-flex px-2 py-1 animate__animated animate__${link.animation} animate__infinite animate__slow styled-link premium-link-click" target="_blank">`
                        
                        if (link.image) {
                            premium_link_html += `
                            <div class="col-1 col-md-2 d-flex align-items-center justify-content-start p-0">
                                <img src="${link.image}" class="link-image-size">
                            </div>
                            <div class="col-9 col-md-8 py-2 ms-2 ms-md-0 d-flex align-items-center justify-content-center">
                                <div class="d-flex flex-column text-center">
                                    <span class='font-size-1'><strong style="letter-spacing: 0.5px;">${link.title}</strong></span>
                                    <span class="font-size-08 link-description">${link.description}</span>
                                </div>
                            </div>`
                        } else {
                            premium_link_html += `
                            <div class="col-12 py-2">
                                <div class="d-flex flex-column text-center">
                                    <span class='font-size-1'><strong style="letter-spacing: 0.5px;">${link.title}</strong></span>
                                    <span class='font-size-08'>${link.description}</span>
                                </div>
                            </div>`
                        }
            
                        premium_link_html += `</a></div></div></div>`
            
                        premium_links_container.innerHTML += premium_link_html
            
            
                       
                    });
            
                    // Styling premium links
                    get_user_theme()

                    count_premium_links_clicks()
                }
            });
        } else {
            premium_links_error_msg.innerHTML = `<p class='text-center font-size-08'><span class='rounded text-danger bg-light px-4 py-1'>PASSWORD IS INVALID</span></p>`
        }
    
    
    })
}


// Styling public links
get_user_theme()