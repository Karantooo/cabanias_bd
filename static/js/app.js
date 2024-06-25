// script.js

let clienteWindow;

const hospedajes = {};
hospedajes['cabana'] = [
    ["101", "Refugio del Bosque"],
    ["102", "Refugio del Sol"],
    ["103", "Refugio del Agua"],
    ["104", "Refugio de la Tierra"]
]
hospedajes['lodge'] = [
    ["201", "Habitación 1"],
    ["202", "Habitación 2"],
    ["203", "Habitación 3"],
    ["204", "Habitación 4"],
    ["205", "Habitación 5"],
    ["206", "Habitación 6"],
    ["207", "Habitación 7"]
]

const changeTipoHospedaje = () => {
    const tipo_hospedaje = document.getElementById("selector-hospedaje");
    const lista_hospedaje = document.getElementById("selector-nombre");

    const sel_hospedaje = tipo_hospedaje.options[tipo_hospedaje.selectedIndex].value;
    
    while(lista_hospedaje.options.length > 1) {
        lista_hospedaje.remove(1);
    }

    const lhospedaje = hospedajes[sel_hospedaje];
    if (lhospedaje) {
        for (let i = 0; i < lhospedaje.length; i++) {
            const nombre = lhospedaje[i][1];
            const id = lhospedaje[i][0];

            const hospedaje = new Option(nombre, id);
            lista_hospedaje.options.add(hospedaje);
        }
    }
}

async function sendData(data) {
    try {
        const response = await fetch(reserva_url, {
            method: "POST",
            body: data,
        });

        return await response;
    } catch (e) {
        console.error(e);
    }
}


async function openCrearCliente(form_hospedaje) {
    const params = 'scrollbars=no,resizable=no,status=no,location=no,toolbar=no,width=300,height=500';
    clienteWindow = window.open(crear_cliente_url, 'Registrar Cliente', params);

    const messageListener = new Promise((resolve) => {
        const listener = (event) => {
            window.removeEventListener('message', listener);
            if (event.data?.data_cliente) { 
                data_cliente = event.data.data_cliente;
                resolve(data_cliente);
            }
        }
        window.addEventListener('message', listener);
    }).then((result) => {
        const data_cliente = result;
        console.log(data_cliente);
        console.log(data_cliente.get("nro_doc"));
        const data_reserva = new FormData(form_hospedaje);
        console.log(data_reserva);

        data_reserva.append("nro_doc", data_cliente.get("nro_doc"));
        data_reserva.append("tipo_doc", data_cliente.get("tipo_doc"));

        console.log(data_reserva);
        sendData(data_reserva);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const hospedaje_select = document.getElementById('selector-hospedaje');

    hospedaje_select.addEventListener('change', changeTipoHospedaje);
    changeTipoHospedaje();

    const form_hospedaje = document.getElementById('form-hospedaje');
    form_hospedaje.addEventListener('submit', (event) => {
        event.preventDefault();
        openCrearCliente(form_hospedaje);
    })
});
