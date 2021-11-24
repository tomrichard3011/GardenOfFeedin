// validates username
function validateUsername() {
    let user = document.getElementById("username").value
    let message = document.getElementById("user_message")
    let valid = true

    if (user == "") {
        message.innerHTML = "Please enter a username."
        valid = false;
    }
    else if (user.length < 5) {
        message.innerText = "Usernames must be at least 5 characters."
        valid = false;
    }
    else if (/[^a-zA-Z0-9_-]/.test(user)) {
        message.innerHTML = "Only a-z, A-Z, 0-9, - and _ allowed in usernames."
        valid = false;
    }
    return valid;
}

// validates password
function validatePassword() {
    let pass = document.getElementById("password").value
    let message = document.getElementById("pass_message")
    let valid = true
    let regex = new RegExp("^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$")

    // empty password check
    if (pass == "") {
        message.innerHTML = "Please enter a password."
        valid = false
    }
    // at least upper, lower, and number check
    else if (!regex.test(pass)) {
        message.innerHTML =  "Password must be at least 8 characters, and include a-z, A-Z, 0-9"
        valid = false
    }
    return valid
}

// function to call for validation
function validate() {
    let user = validateUsername()
    let pass = validatePassword()
    return user && pass
