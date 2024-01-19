function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) return parts.pop().split(';').shift();
}

function nuevoProducto(){
    const f = document.getElementById('form');
    console.log(f['id_nombre_generico'].value);

    console.log("enviado al servidor");

    fetch('/guardar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            codigo: f['id_codigo'].value,
            nombre_generico: f['id_nombre_generico'].value,
            nombre_cientifico: f['id_nombre_cientifico'].value,
            descripcion: f['id_descripcion'].value,
            categoria: f['id_categoria'].value,
            via: f['id_via'].value,
            receta: f['id_req_receta'].value,
            laboratorio: f['id_laboratorio'].value,
            unidad: f['id_unidad_Medida'].value
        })
    })
    .then(response => response.json())
    .then(data => {
        //Esto convierte el id obtenido de la las seleccion de opciones y consigue el texto escrito en el select
        console.log(data.mensaje);
        if(data.mensaje != "El Código ya existe"){
            const concat = f.querySelector('#id_categoria'); 
            const textcat = concat.options[concat.selectedIndex].textContent;

            const conlab = f.querySelector('#id_laboratorio'); 
            const textlab = conlab.options[conlab.selectedIndex].textContent;

            const convia = f.querySelector('#id_via'); 
            const textvia = convia.options[convia.selectedIndex].textContent;

            //agrega el nuevo elemento en la tabla
            lista = document.getElementById('registrados');
            lista.innerHTML += `<td scope="row">`+ f['id_codigo'].value + `</td>
            <td>`+ f['id_nombre_generico'].value + `</td>
            <td>`+ textcat + `</td>
            <td>`+ textlab + `</td>
            <td>`+ textvia + `</td>`
        }else{
            alert("El producto ya existe o el Código esta repetido");
        }
        f.reset();
    })
}
