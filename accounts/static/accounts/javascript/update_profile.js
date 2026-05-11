function UpdateProfileForm(event) {
  event.preventDefault();

  const submitBtn = document.getElementById('submitBtn');
  const submitText = document.getElementById('submitText');
  const inputs = document.querySelectorAll('input')

  // Disable All Form Inputs
  inputs.forEach(input => {
    if (input.name != 'csrfmiddlewaretoken') {
      input.disabled = true;
    }
  });

  submitBtn.disabled = true;
  submitBtn.classList.remove('bg-transparent');
  submitBtn.classList.add('bg-white/20');
  submitText.textContent = "Updating profile...";

  setTimeout(() => {
    event.target.submit();
  }, 4000);

}


const idAvatar = document.getElementById('id_avatar');
const avatarPreview = document.getElementById('avatar-preview');



idAvatar.addEventListener('change', (e) => {
  const f = e.target.files[0];
  avatarPreview.src = URL.createObjectURL(f);
})
