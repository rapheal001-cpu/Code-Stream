const idAvatar = document.getElementById('id_avatar');
const avatarPreview = document.getElementById('avatar-preview');

idAvatar.addEventListener('change', (e) => {
  const f = e.target.files[0];
  avatarPreview.src = URL.createObjectURL(f);
})
