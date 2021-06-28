const submitBtn = document.getElementById('submitBtn')

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
            aspectRatio: 1 / 1,
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

            });
        });

    }

})


// Username validation
/*
const usernameField = document.querySelector('#usernameField')
const usernameFeedback = document.querySelector('.username-feedback')

usernameField.addEventListener('keyup', (e) => {
    const usernameValue = e.target.value;

    usernameField.classList.remove('is-invalid')
    usernameField.classList.remove('is-valid')
    usernameFeedback.style.display = 'none'

    if (usernameValue.length >= 2 && usernameValue.length <= 80) {
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
    } else {
        // Dispable submit button
        submitBtn.setAttribute('disabled', 'disabled')
        submitBtn.disabled = true

        usernameField.classList.add('is-invalid')

        usernameFeedback.style.display = 'block'
        usernameFeedback.innerHTML = `<p>Username must be between 2 and 80 characters.</p>`
    }
})
*/

// Name validation
const nameField = document.querySelector('#nameField')
const nameFeedback = document.querySelector('.name-feedback')

nameField.addEventListener('keyup', (e) => {
    const nameValue = e.target.value;

    nameField.classList.remove('is-invalid')
    nameField.classList.remove('is-valid')
    nameFeedback.style.display = 'none'

    if (nameValue.length < 40) {
        submitBtn.removeAttribute('disabled')

        nameField.classList.remove('is-invalid')
        nameField.classList.add('is-valid')
    } else {
        // Dispable submit button
        submitBtn.setAttribute('disabled', 'disabled')
        submitBtn.disabled = true

        nameField.classList.add('is-invalid')

        nameFeedback.style.display = 'block'
        nameFeedback.innerHTML = `<p>Name must be less than 40 characters.</p>`
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