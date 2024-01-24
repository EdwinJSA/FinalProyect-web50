var listaArticulos = [];
var total=0;

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
            <td>`+ textvia + `</td>
            <td><a href="{% url 'eliminarProducto' i.codigo %}">Borrar</a></td>`
        }else{
            alert("El producto ya existe o el Código esta repetido");
        }
        f.reset();
    })
}

function nuevaCompra(){
    const f = document.getElementById('form');
    fetch('/nuevaCompra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            proveedor: f['id_proveedor'].value,
            producto: f['id_producto'].value,
            cantidad: f['id_cantidad'].value,
            precio: f['id_precio_unidad'].value,
            fecha: f['id_fecha_vencimiento'].value
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.mensaje);
        f.reset();
    })
}

function activarBoton(){
    control = document.getElementById('controlClick');
    activar = document.getElementById('completar');
    
    activar.disabled = false;
    control.innerHTML = "Comprobado";
    control.style.backgroundColor = "green";
    control.style.color = "white";
    control.disabled = true;
}

document.addEventListener('keyup', (event) => {
    if(event.target.matches('#buscadorProductos')){
        document.querySelectorAll('.articulos').forEach(elemento => {
            if(!elemento.textContent.toLowerCase().includes(event.target.value.toLowerCase())){
                elemento.classList.add('d-none');
            }else{
                elemento.classList.remove('d-none');
            }
        })
    }
})


document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.articulos').forEach(function(elemento) {
        elemento.addEventListener('click', function() {
            var nombreCientifico = this.dataset.nombreCientifico;
            var precio = this.dataset.precio;
            var codigo = this.dataset.codigo;
            var receta = this.dataset.receta;

            const producto = document.getElementById('id_producto');
            const dinero = document.getElementById('id_precio_unidad');
            const id = document.getElementById('id_codigo');

            producto.value = nombreCientifico;
            dinero.value = precio;  
            id.value = codigo;

            var medico = document.getElementById("nombreMedico");
            console.log(medico)
            console.log("Receta: " + receta)

            if(receta == "True"){
                medico.classList.remove('d-none')
                medico.classList.add('d-block')
                console.log("Se tiene que ver")
            }
            else{
                medico.classList.remove('d-block')
                medico.classList.add('d-none')
                console.log("no se debe ver")
            }
        });
    });
});


function agregarCarrito(){
    car = document.getElementById('pr_registrados');

     listaArticulos.push({
        id: document.getElementById('id_codigo').value,
        cantidad: document.getElementById('id_cantidad').value,
        precio: document.getElementById('id_precio_unidad').value
    })

    localStorage.setItem('carrito', JSON.stringify(listaArticulos));

    car.innerHTML += `<tr id="${document.getElementById('id_codigo').value}">
    <td>`+ document.getElementById('id_codigo').value + `</td>
    <td>`+ document.getElementById('id_producto').value + `</td>
    <td>`+ document.getElementById('id_cantidad').value + `</td>
    <td>`+ document.getElementById('id_precio_unidad').value + `</td>
    <td>`+ document.getElementById('id_cantidad').value * document.getElementById('id_precio_unidad').value + `</td>
    <td><button type=button onclick="borrarArticulo(${document.getElementById('id_codigo').value})">Borrar</button></td></td>
    </tr>`

    total += document.getElementById('id_cantidad').value * document.getElementById('id_precio_unidad').value;

    document.getElementById('precioFinal').textContent = "Total: C$" + total;

    console.log(total);
}

function borrarArticulo(id) {
    console.log(localStorage.getItem('carrito'));

    var carrito = JSON.parse(localStorage.getItem('carrito'));

    for (var i = 0; i < carrito.length; i++) {
        if (carrito[i].id == id) {
            //The splice() method of Array instances changes the contents of an array by removing or replacing existing elements and/or adding new elements in place.
            carrito.splice(i, 1);
        }
    }

    total -= document.getElementById(id).children[4].textContent;

    localStorage.setItem('carrito', JSON.stringify(carrito));
    document.getElementById(id).remove();
}

function completarVenta(){
    var carrito = JSON.parse(localStorage.getItem('carrito'));
    var check = document.getElementById('aplicarDescuento').checked;
    var medico = document.getElementById("medico").value;
    var codMinsa = document.getElementById("codMinsa").value;

    console.log(carrito)

    fetch('comprarProducto',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            compras: carrito,
            descuento: check,
            total: total,
            medico: medico,
            codMinsa: codMinsa
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        listaArticulos = [];
        total=0;
        localStorage.clear();
        alert("Compra Realizada")
        setTimeout(function() {
            window.location.reload();
        }, 1000);
    })
}

document.addEventListener('DOMContentLoaded', function() {
    const aplicar = document.getElementById('aplicarDescuento');
    const precioFinalElement = document.getElementById('precioFinal');

    aplicar.addEventListener('change', () => {
        if (aplicar.checked) {
            total *= 0.9;
        }
        precioFinalElement.textContent = "Total: C$" + total.toFixed(2);
    });
})