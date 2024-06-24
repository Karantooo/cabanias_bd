// script.js
document.addEventListener('DOMContentLoaded', function() {
    const consultasSelect = document.getElementById('selectorHospedaje');
    const conditionalMenuItem = document.getElementById('nombre_cabaña');

    consultasSelect.addEventListener('change', function() {
        if (consultasSelect.value == 'cabaña') {
            conditionalMenuItem.style.display = 'block';
        } else {
            conditionalMenuItem.style.display = 'none';
        }
    });
});
