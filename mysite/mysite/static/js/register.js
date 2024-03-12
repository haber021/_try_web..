const submitBtn=document.querySelector(".submit-btn")

const showPasswordToggle = document.querySelector(".showPasswordToggle");
const passwordField = document.querySelector("#passwordField");


const handleToggleInput = (e) =>{
    if(showPasswordToggle.textContent ==='SHOW'){
        showPasswordToggle.textContent = 'HIDE';

        passwordField.setAttribute("type","text");
    } else {
        showPasswordToggle.textContent = 'SHOW';
        passwordField.setAttribute("type","password");
    }
};
showPasswordToggle.addEventListener('click', handleToggleInput);




const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput")

emailField.addEventListener('keyup', (e) => {
    const emailVal = e.target.value;

    emailSuccessOutput.style.display = "block";
    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";
    emailSuccessOutput.textContent = `checking ${emailVal}`;

    if (emailVal.length > 0) {
        fetch("/authentication/validate-email", {
            body: JSON.stringify({ email: emailVal }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                emailSuccessOutput.style.display = "none";
                if (data.email_error) {
                    submitBtn.disabled = true;
                    emailField.classList.add("is-invalid");
                    emailFeedBackArea.style.display = "block";
                    emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
                } else {
                    submitBtn.removeAttribute("disabled");
                    emailField.classList.remove("is-invalid");
                    emailFeedBackArea.style.display = "none";
                    emailFeedBackArea.innerHTML = ''; // Clear the error message
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                emailField.classList.remove("is-invalid");
                emailFeedBackArea.style.display = "none";
                emailFeedBackArea.innerHTML = ''; // Clear the error message
            });
    } else {
        emailField.classList.remove("is-invalid");
        emailFeedBackArea.style.display = "none";
        emailFeedBackArea.innerHTML = ''; // Clear the error message
    }
});




const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");

usernameField.classList.remove("is-invalid");
feedBackArea.style.display = "none";

usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;
    usernameSuccessOutput.style.display = "block";
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`;

    if (usernameVal.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({ username: usernameVal }),
            method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            usernameSuccessOutput.style.display = "none";
            console.log("data", data);
            if (data.username_error) {
                submitBtn.disabled = true;
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display = "block";
                feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
            } else {
                submitBtn.removeAttribute("disabled");
                usernameField.classList.remove("is-invalid");
                feedBackArea.style.display = "none";
                feedBackArea.innerHTML = ''; // Clear the error message
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            // Handle error
        });
    } else {
        usernameField.classList.remove("is-invalid");
        feedBackArea.style.display = "none";
        feedBackArea.innerHTML = ''; // Clear the error message
    }
});

