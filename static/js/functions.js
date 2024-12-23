document.addEventListener('htmx:responseError', evt => {
    
    const obj = document.getElementById("message")
    var msg = evt.detail.xhr.responseText

    if (evt.detail.xhr.status == 422) {
        msg = "Invalid user data"
    }

    obj.innerHTML = msg
})