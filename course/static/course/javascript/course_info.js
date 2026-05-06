function toggleStudentList() {
const modal = document.getElementById('student-list');
const panel = document.getElementById('student-list-panel');

if (modal.classList.contains('hidden')) {
// Open
modal.classList.remove('hidden');
// Small delay to allow display:block to apply before transition
setTimeout(() => {
panel.classList.remove('scale-95', 'opacity-0');
panel.classList.add('scale-100', 'opacity-100');
}, 10);
} else {
// Close
panel.classList.remove('scale-100', 'opacity-100');
panel.classList.add('scale-95', 'opacity-0');
setTimeout(() => {
modal.classList.add('hidden');
}, 200);
}
}

// Close on Escape key
document.addEventListener('keydown', function(e) {
if (e.key === 'Escape') {
const modal = document.getElementById('student-list');
if (!modal.classList.contains('hidden')) {
toggleStudentList();
}
}
});