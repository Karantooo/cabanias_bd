document.querySelector('.client-form').addEventListener('submit', function(e) {
    e.preventDefault(); // Previene el envío del formulario
    window.location.href = 'index.html'; // Redirige al usuario a index.html
});