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
