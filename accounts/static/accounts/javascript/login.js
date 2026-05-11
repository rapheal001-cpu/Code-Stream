function LoginForm(event) {
event.preventDefault();

const submitBtn = document.getElementById('submitBtn');
const submitText = document.getElementById('submitText');
const idLogin = document.getElementById('id_login')
const idPassword = document.getElementById('id_password')

// Disable All Form Inputs
idLogin.disabled = true;
idPassword.disabled = true;

submitBtn.disabled = true;
submitBtn.classList.remove('bg-transparent');
submitBtn.classList.add('bg-white/20');
submitText.textContent = "Authenticating...";

setTimeout(() => {
event.target.submit();
}, 4000);

}