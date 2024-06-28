async function sendData(data) {
    console.log(data);
    try {
        const response = await fetch(cliente_url, {
            method: "POST",
            body: data,
        });

        await response;
    } catch (e) {
        console.error(e);
    }

    console.log(data);
    window.opener.postMessage({data_cliente: data}, '*');

    window.close();
}

document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.querySelector('.client-form');

    formulario.addEventListener('submit', (event) => {
        event.preventDefault();
        const form_data = new FormData(formulario);

        const response = sendData(form_data);
    });
});
