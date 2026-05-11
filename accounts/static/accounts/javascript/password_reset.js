function PasswordResetForm(event) {
  event.preventDefault();

  const submitBtn = document.getElementById('submitBtn');
  const submitText = document.getElementById('submitText');
  const input = document.querySelector('input[type=email]')


  input.disabled = true;
  submitBtn.disabled = true;
  submitBtn.classList.remove('bg-transparent');
  submitBtn.classList.add('bg-white/20');
  submitText.textContent = "Sending Reset Link...";

  setTimeout(() => {
    event.target.submit();
  }, 4000);

}