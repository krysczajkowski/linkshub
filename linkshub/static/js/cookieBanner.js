const cookieStorage = {
    setItem: (key, value) => {
        document.cookie = `${key}=${value}; max-age=31536000;`
    },
}

const storageType = cookieStorage;
const consentPropertyName = 'accept_cookies';

const saveToStorage = () => storageType.setItem(consentPropertyName, true)

const cookie_banner = document.querySelector('#cookie_banner')
const accept_cookies = document.querySelector('#cookieBtn')

window.onload = () => {
    value_or_null = (document.cookie.match(/^(?:.*;)?\s*accept_cookies\s*=\s*([^;]+)(?:.*)?$/)||[,null])[1]

    if (value_or_null == null) {
        cookie_banner.classList.remove('d-none')

        accept_cookies.addEventListener('click', () => {
            cookie_banner.classList.add('d-none')
            saveToStorage();
        })
    }
};
