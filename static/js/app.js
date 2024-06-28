// script.js

let clienteWindow;

let mapa_doc = {
    "Cédula Chilena": "chilena",
    "Documento Mercosur": "mercosur",
    "Pasaporte": "pasaporte"
};

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

async function sendData(data, url) {
    try {
        const response = await fetch(url, {
            method: "POST",
            body: data,
        });

        return await response;
    } catch (e) {
        console.error(e);
    }
}

async function queryData(data, url) {
    try {
        const response = await fetch(url + '?' + new URLSearchParams(data).toString())
            .then((response) => response.json())
        return response;
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
        const data_reserva = new FormData(form_hospedaje);

        data_reserva.append("nro_doc", data_cliente.get("nro_doc"));
        data_reserva.append("tipo_doc", data_cliente.get("tipo_doc"));

        sendData(data_reserva, reserva_url);
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
    });

    const form_servicio = document.querySelector('#servicio-form');
    form_servicio.addEventListener('submit', async (event) => {
        event.preventDefault();
        const data = new FormData(form_servicio);

        data_reserva = await queryData(data, reserva_get_url);

        data.append("fecha_inicio", data.get("fecha"));
        data.append("fecha_fin", data.get("fecha"));
        data.append("nro_doc", data_reserva.nro_documento);
        data.append("tipo_doc", mapa_doc[data_reserva.tipo_documento]);
        data.append("cant_personas", data_reserva.cant_personas);
        data.append("folio", data_reserva.folio);

        sendData(data, reserva_url);
    });
});


document.addEventListener('DOMContentLoaded', function() {
    
    const form_consulta = document.getElementById('form_consulta');
    
    form_consulta.addEventListener('submit', async (event) => {
        event.preventDefault();

        const eleccion_cliente = document.getElementById('opcion_consulta');
        console.log(eleccion_cliente.value);
        if(eleccion_cliente.value == 1){
            datos = new FormData(form_consulta);
            consulta = await queryData(datos, empleado_url);
            
        }
        else{
            datos = new FormData(form_consulta);
            consulta = await queryData(datos, cliente_url);
        }
        respuesta = this.getElementById('resultado_consulta');
        respuesta.innerText = '';
       console.log(consulta);
        for (let clave in consulta) {
            if (!Array.isArray(consulta[clave])) 
              respuesta.innerText += `${clave}: ${consulta[clave]}\n`;
            else{
                respuesta.innerText += `${clave} : \n`;
                reserva = consulta[clave];

                reserva.forEach(function(elemento) {
                    for (item in elemento){
                        respuesta.innerText += `${item}: ${elemento[item]} \n`;
                    }
                    respuesta.innerText += '\n\n\n';
                });
            }
            
          }
  
        if (consulta == undefined)
            respuesta.innerText = 'Persona no encontrada';
    })

   
});
