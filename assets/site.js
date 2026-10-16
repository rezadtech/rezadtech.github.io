const originalTitle = document.title;
function resumeTitle() {
  if (!document.querySelector('[data-print]')) return;
  document.title = document.body.classList.contains('photonics')
    ? 'Reza_Dayhool_Photonics_Resume_2026'
    : 'Reza_Dayhool_Cybersecurity_Resume_2026';
}
window.addEventListener('beforeprint', resumeTitle);
window.addEventListener('afterprint', () => { document.title = originalTitle; });
document.querySelectorAll('[data-print]').forEach(button => {
  button.addEventListener('click', () => { resumeTitle(); window.print(); });
});
