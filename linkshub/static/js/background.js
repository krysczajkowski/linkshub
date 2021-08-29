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


// Change image when pick file 
const imgPreview = document.getElementById('imgPreview')
const imageField = document.getElementById('imageField')

// Image validation

// image-box is the id of the div element that will store our cropping image preview
const imagebox = document.getElementById('image-box')
    // crop-btn is the id of button that will trigger the event of change original file with cropped file.
const crop_btn = document.getElementById('crop-btn')

const imageFeedback = document.querySelector('.image-feedback')

imageField.addEventListener('change', () => {
    imageFeedback.classList.remove('is-invalid')
    imageFeedback.classList.remove('is-valid')
    imageFeedback.style.display = 'none'

    const allowedExtensions =  ['jpg','png', 'jpeg'],
          sizeLimit = 5000000; // 5 megabyte

    // destructuring file name and size from file object
    const { name:fileName, size:fileSize } = imageField.files[0];

    const fileExtension = fileName.split(".").pop();

    if (!allowedExtensions.includes(fileExtension.toLowerCase())) {
        // File type not allowed
        console.log('image invalid')

        // Dispable submit button
        console.log('zle')

        imageFeedback.style.display = 'block'
        imageFeedback.innerHTML = 'File type is not allowed.'
    } else if (fileSize > sizeLimit) {
        // File size is too large

        console.log('image invalid')
        // Dispable submit button
        console.log('zle')
        imageField.classList.add('is-invalid')

        imageFeedback.style.display = 'block'
        imageFeedback.innerHTML = 'File size is too large.'
    } else {
        // Image is valid
        console.log('image valid')

        imageField.classList.remove('is-invalid')
        imageField.classList.add('is-valid')

        // Getting image file object from the input variable
        const img_data = imageField.files[0]
        // createObjectURL() static method creates a DOMString containing a URL representing the object given in the parameter.
        // The new object URL represents the specified File object or Blob object.
        const url = URL.createObjectURL(img_data)

        // Creating a image tag inside imagebox which will hold the cropping view image(uploaded file) to it using the url created before.
        imagebox.innerHTML = `<img src="${url}" id="image" style="width:100%;">`

        // Storing that cropping view image in a variable
        const image = document.getElementById('image')

        // Creating a croper object with the cropping view image
        // The new Cropper() method will do all the magic and diplay the cropping view and adding cropping functionality on the website
        // For more settings, check out their official documentation at https://github.com/fengyuanchen/cropperjs
        const cropper = new Cropper(image, {
            autoCropArea: 1,
            viewMode: 1,
            scalable: false,
            zoomable: false,
            movable: false,
            minCropBoxWidth: 100,
            minCropBoxHeight: 100,
        })

        // When crop button is clicked this event will get triggered
        crop_btn.addEventListener('click', ()=>{
            // This method coverts the selected cropped image on the cropper canvas into a blob object
            cropper.getCroppedCanvas().toBlob((blob)=>{
                
                // Gets the original image data
                let fileInputElement = document.getElementById('imageField');
                // Make a new cropped image file using that blob object, image_data.name will make the new file name same as original image
                let file = new File([blob], img_data.name,{type:"image/*", lastModified:new Date().getTime()});
                // Create a new container
                let container = new DataTransfer();
                // Add the cropped image file to the container
                container.items.add(file);
                // Replace the original image file with the new cropped image file

                fileInputElement.files = container.files;


                imgPreview.src = URL.createObjectURL(file)

                var data = new FormData()
                data.append('background_image', file)

                console.log(data)

                // Send file to backend
                fetch('background/bg/image', {
                    body: data,
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'X-CSRFToken': csrftoken,
                        'X-Requested-With':'XMLHttpRequest'
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

                });
        });

    }

})