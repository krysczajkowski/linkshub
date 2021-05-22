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


// Url field validation
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

urlField.addEventListener('focusout', (e) => {
    const urlValue = e.target.value;

    urlFeedback.classList.remove('is-invalid')
    urlFeedback.classList.remove('is-valid')
    urlFeedback.style.display = 'none'

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


submitBtn.addEventListener('click', (e) => {
    
    submitBtn.disabled = true
    document.querySelector('#submitSpinner').classList.remove('d-none')

    document.getElementById("add-link-form").submit();
})