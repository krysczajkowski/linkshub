const submitBtn = document.querySelector('#submitBtn')


// Title validation
const titleField = document.querySelector('#titleField')
const titleFeedback = document.querySelector('.title-feedback')

titleField.addEventListener('focusout', (e) => {
    const titleValue = e.target.value;

    titleFeedback.classList.remove('is-invalid')
    titleFeedback.classList.remove('is-valid')
    titleFeedback.style.display = 'none'

    if (titleValue.length < 1 || titleValue.length > 70) {
        // Dispable submit button
        submitBtn.setAttribute('disabled', 'disabled')
        submitBtn.disabled = true
        titleField.classList.add('is-invalid')

        titleFeedback.style.display = 'block'
        titleFeedback.innerHTML = 'Title length must be between 1 and 70 characters.'
    } else {
        submitBtn.removeAttribute('disabled')

        titleField.classList.remove('is-invalid')
        titleField.classList.add('is-valid')
    }
})


// Description validation
const descriptionField = document.querySelector('#descriptionField')
const descriptionFeedback = document.querySelector('.description-feedback')

descriptionField.addEventListener('focusout', (e) => {
    const descriptionValue = e.target.value;

    descriptionFeedback.classList.remove('is-invalid')
    descriptionFeedback.classList.remove('is-valid')
    descriptionFeedback.style.display = 'none'

    if (descriptionValue.length > 150) {
        // Dispable submit button
        submitBtn.setAttribute('disabled', 'disabled')
        submitBtn.disabled = true
        descriptionField.classList.add('is-invalid')

        descriptionFeedback.style.display = 'block'
        descriptionFeedback.innerHTML = 'Description length can not be over 150 characters.'
    } else {
        submitBtn.removeAttribute('disabled')

        descriptionField.classList.remove('is-invalid')
        descriptionField.classList.add('is-valid')
    }
})


// Detect youtube link function
function detect_youtube_url(url){
    var regExp = /^https?\:\/\/(?:www\.youtube(?:\-nocookie)?\.com\/|m\.youtube\.com\/|youtube\.com\/)?(?:ytscreeningroom\?vi?=|youtu\.be\/|vi?\/|user\/.+\/u\/\w{1,2}\/|embed\/|watch\?(?:.*\&)?vi?=|\&vi?=|\?(?:.*\&)?vi?=)([^#\&\?\n\/<>"']*)/i;
    var match = url.match(regExp);
    return (match && match[1].length==11)? match[1] : false;
}


// Url field validation function
function validURL(str) {
  var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
    '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
    '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
    '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
    '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
    '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
  return !pattern.test(str);
}

const urlField = document.querySelector('#urlField')
const urlFeedback = document.querySelector('.url-feedback')
const youtubeCheckboxArea = document.querySelector('#youtube-checkbox-area')

// Detect youtube url 
if (detect_youtube_url(urlField.value)) {
    youtubeCheckboxArea.classList.remove('d-none')
} else {
    youtubeCheckboxArea.classList.add('d-none')
}


urlField.addEventListener('focusout', (e) => {
    const urlValue = e.target.value;

    urlFeedback.classList.remove('is-invalid')
    urlFeedback.classList.remove('is-valid')
    urlFeedback.style.display = 'none'

    // Detect youtube url 
    if (detect_youtube_url(urlValue)) {
        youtubeCheckboxArea.classList.remove('d-none')
    } else {
        youtubeCheckboxArea.classList.add('d-none')
    }

    if (validURL(urlValue)) {
        // Dispable submit button
        submitBtn.setAttribute('disabled', 'disabled')
        submitBtn.disabled = true
        urlField.classList.add('is-invalid')

        urlFeedback.style.display = 'block'
        urlFeedback.innerHTML = 'Please provide valid URL.'
    } else {
        submitBtn.removeAttribute('disabled')

        urlField.classList.remove('is-invalid')
        urlField.classList.add('is-valid')

    }
})


// Image validation
const imageField = document.querySelector('#imageField')
const imageFeedback = document.querySelector('.image-feedback')

const imagebox = document.getElementById('image-box')
const crop_btn = document.getElementById('crop-btn')

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
        cropper.getCroppedCanvas({
            width: 200,
            height: 200
          }).toBlob((blob)=>{
            
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

            });
        });
    }

}


// Submit saving effect
submitBtn.addEventListener('click', (e) => {
    if (titleField.value.length <= 0 && urlField.value.length <= 0) {
        // Title field error
        titleField.classList.add('is-invalid')
        titleFeedback.style.display = 'block'
        titleFeedback.innerHTML = 'Title length must be between 1 and 70 characters.'

        // URL field error
        urlField.classList.add('is-invalid')
        urlFeedback.style.display = 'block'
        urlFeedback.innerHTML = 'Please provide valid URL.'
    } else if (titleField.value.length <= 0) {
        // Title field error
        titleField.classList.add('is-invalid')
        titleFeedback.style.display = 'block'
        titleFeedback.innerHTML = 'Title length must be between 1 and 70 characters.'
    } else if (urlField.value.length <= 0) {
        // URL field error
        urlField.classList.add('is-invalid')
        urlFeedback.style.display = 'block'
        urlFeedback.innerHTML = 'Please provide valid URL.'
    } else {
        document.querySelector('#submitSpinner').classList.remove('d-none')

        document.getElementById("add-link-form").submit();
    }

    submitBtn.disabled = true

})

