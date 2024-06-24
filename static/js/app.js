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

document.getElementById('selectorHospedaje').addEventListener('change', function() {
    var valor = this.value;

    // Oculta ambos inputs inicialmente
    document.getElementById('nombre_cabana').style.display = 'none';
    document.getElementById('nombre_lodge').style.display = 'none';

    // Muestra el input correspondiente basado en la selección
    if (valor === 'cabana') {
        document.getElementById('nombre_cabana').style.display = 'flex';
    } else if (valor === 'lodge') {
        document.getElementById('nombre_lodge').style.display = 'flex';
    }
});