const submitBtn = document.getElementById('submitBtn')

// Change image when pick file 
const imgPreview = document.getElementById('imgPreview')
const imageField = document.getElementById('imageField')

imageField.addEventListener('change', (e)=>{
    console.log('adf')
    const [file] = imageField.files

    if (file) {
        imgPreview.src = URL.createObjectURL(file)
    }
})

// Image validation
const imageFeedback = document.querySelector('.image-feedback')

imageField.addEventListener('change', validateFile)

function validateFile(){
    console.log('onchange')

    imageFeedback.classList.remove('is-invalid')
    imageFeedback.classList.remove('is-valid')
    imageFeedback.style.display = 'none'

    const allowedExtensions =  ['jpg','png', 'jpeg'],
          sizeLimit = 5000000; // 5 megabyte

    // destructuring file name and size from file object
    const { name:fileName, size:fileSize } = this.files[0];

    const fileExtension = fileName.split(".").pop();

    if (!allowedExtensions.includes(fileExtension.toLowerCase())) {
        // File type not allowed
        console.log('image invalid')

        // Dispable submit button
        submitBtn.setAttribute('disabled', 'disabled')
        submitBtn.disabled = true
        imageField.classList.add('is-invalid')

        imageFeedback.style.display = 'block'
        imageFeedback.innerHTML = 'File type is not allowed.'
    } else if (fileSize > sizeLimit) {
        // File size is too large

        console.log('image invalid')
        // Dispable submit button
        submitBtn.setAttribute('disabled', 'disabled')
        submitBtn.disabled = true
        imageField.classList.add('is-invalid')

        imageFeedback.style.display = 'block'
        imageFeedback.innerHTML = 'File size is too large.'
    } else {
        // Image is valid
        console.log('image valid')
        submitBtn.removeAttribute('disabled')

        imageField.classList.remove('is-invalid')
        imageField.classList.add('is-valid')
    }

}

// Username validation
const usernameField = document.querySelector('#usernameField')
const usernameFeedback = document.querySelector('.username-feedback')

usernameField.addEventListener('keyup', (e) => {
    const usernameValue = e.target.value;

    usernameField.classList.remove('is-invalid')
    usernameField.classList.remove('is-valid')
    usernameFeedback.style.display = 'none'

    if (usernameValue.length > 0) {
        fetch('/authentication/validate-username', {
            body: JSON.stringify({'username': usernameValue}),
            method: 'POST',
        }).then(res=>res.json()).then(data=>{
            console.log('data', data)
            if(data.username_error) {
                // Dispable submit button
                submitBtn.setAttribute('disabled', 'disabled')
                submitBtn.disabled = true

                usernameField.classList.add('is-invalid')

                usernameFeedback.style.display = 'block'
                usernameFeedback.innerHTML = `<p>${data.username_error}</p>`
            } else {
                submitBtn.removeAttribute('disabled')

                usernameField.classList.remove('is-invalid')
                usernameField.classList.add('is-valid')
            }
        });
    }
})

// Description validation
const descriptionField = document.querySelector('#descriptionField')
const descriptionFeedback = document.querySelector('.description-feedback')

descriptionField.addEventListener('keyup', (e) => {
    const descriptionValue = e.target.value;

    descriptionField.classList.remove('is-invalid')
    descriptionField.classList.remove('is-valid')
    descriptionFeedback.style.display = 'none'

    if (descriptionValue.length < 300) {
        submitBtn.removeAttribute('disabled')

        descriptionField.classList.remove('is-invalid')
        descriptionField.classList.add('is-valid')
    } else {
        // Dispable submit button
        submitBtn.setAttribute('disabled', 'disabled')
        submitBtn.disabled = true

        descriptionField.classList.add('is-invalid')

        descriptionFeedback.style.display = 'block'
        descriptionFeedback.innerHTML = `<p>Description must be less than 300 characters.</p>`
    }
})

// Submit saving effect
submitBtn.addEventListener('click', (e) => {

    document.querySelector('#submitSpinner').classList.remove('d-none')

    document.getElementById("edit-form").submit();

    submitBtn.disabled = true

})