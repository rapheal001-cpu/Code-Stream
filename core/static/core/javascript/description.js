// Character count and live preview
  const textarea = document.getElementById('id_description');
  const charCount = document.getElementById('char-count');
  const previewText = document.getElementById('preview-text');
  const maxLength = 500;

  function updateCharCount() {
    const current = textarea.value.length;
    charCount.textContent = `${current} / ${maxLength}`;
    
    if (current > maxLength * 0.9) {
      charCount.classList.add('text-amber-600');
      charCount.classList.remove('text-gray-500');
    } else {
      charCount.classList.remove('text-amber-600');
      charCount.classList.add('text-gray-500');
    }
  }

  function updatePreview() {
    const text = textarea.value.trim();
    previewText.textContent = text || 'No description yet. Write something about yourself!';
    previewText.classList.toggle('text-gray-400', !text);
    previewText.classList.toggle('text-gray-600', !!text);
  }

  textarea.addEventListener('input', () => {
    updateCharCount();
    updatePreview();
  });

  // Initialize
  updateCharCount();
  updatePreview();
