function SignupForm(event) {
event.preventDefault();

const submitBtn = document.getElementById('submitBtn');
const submitText = document.getElementById('submitText');
const idFirstName = document.querySelectorAll('id_first')

// Disable All Form Inputs
idFirstName.disabled = true;
idLastName.disabled = true;
isUsername.disabled = true;
idEmail.disabled = true;
idPassword1.disabled = true;
idPassword2.disabled = true;


submitBtn.disabled = true;
submitBtn.classList.remove('bg-transparent');
submitBtn.classList.add('bg-white/20');
submitText.textContent = "Creating account...";

setTimeout(() => {
event.target.submit();
}, 4000);

}