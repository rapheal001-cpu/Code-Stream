function SignupForm(event) {
event.preventDefault();

const submitBtn = document.getElementById('submitBtn');
const submitText = document.getElementById('submitText');
const idFirstName = document.querySelectorAll('id_first')

// Disable All Form Inputs


submitBtn.disabled = true;
submitBtn.classList.remove('bg-transparent');
submitBtn.classList.add('bg-white/20');
submitText.textContent = "Creating account...";

setTimeout(() => {
event.target.submit();
}, 4000);

}