 (function() {
  const modal = document.getElementById('addVideoModal');
  const backdrop = document.getElementById('modalBackdrop');
  const panel = document.getElementById('modalPanel');
  const openBtn = document.getElementById('addVideoBtn');
  const closeBtn = document.getElementById('closeModalBtn');
  const cancelBtn = document.getElementById('cancelBtn');
   

  function openModal() {
  modal.classList.remove('hidden');
  void modal.offsetWidth;
  backdrop.classList.remove('opacity-0');
  panel.classList.remove('scale-95', 'opacity-0');
  panel.classList.add('scale-100', 'opacity-100');
  document.body.style.overflow = 'hidden';
  }

  function closeModal() {
  backdrop.classList.add('opacity-0');
  panel.classList.remove('scale-100', 'opacity-100');
  panel.classList.add('scale-95', 'opacity-0');
  setTimeout(() => {
  modal.classList.add('hidden');
  document.body.style.overflow = '';
  }, 200);
  }

  openBtn.addEventListener('click', openModal);
  closeBtn.addEventListener('click', closeModal);
  cancelBtn.addEventListener('click', closeModal);
  backdrop.addEventListener('click', closeModal);

  document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
  closeModal();
  }
  });
  })();