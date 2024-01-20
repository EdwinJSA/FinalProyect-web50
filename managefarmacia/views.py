from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import categoria, proveedor, unidad_Medida, laboratorio, via_consumo
from .forms import *
from django.http import HttpResponse, JsonResponse
import json
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, 'index.html')

def categoria_views(request):
    if request.method == 'POST':
        texto = request.POST['nuevaCategoria']
        newCat = categoria(
            nombre = texto
        )
        newCat.save()
        return render(request, 'categoria.html',{
            'categorias': categoria.objects.all()
        })
    return render(request, 'categoria.html',{
        'categorias': categoria.objects.all()
    })

def eliminarCategoria(request, id):
    categoria.objects.get(id=id).delete()
    return HttpResponseRedirect('/categoria')

def proveedor_views(request):
    if request.method == 'POST':
        texto = request.POST['nuevoProveedor']
        newProv = proveedor(
            nombre = texto
        )
        newProv.save()
        return render(request, 'proveedores.html',{
            'proveedores': proveedor.objects.all()
        })
    return render(request, 'proveedores.html',{
        'proveedores': proveedor.objects.all()
    })
    
def eliminarProveedor(request, id):
    proveedor.objects.get(id=id).delete()
    return HttpResponseRedirect('/proveedores')

def unidad_views(request):
    if request.method == 'POST':
        texto = request.POST['nuevaUnidad']
        min = request.POST['minimo']
        newUnidad = unidad_Medida(
            nombre = texto,
            minimo = min
        )
        newUnidad.save()
        return render(request, 'unidad.html',{
            'unidades': unidad_Medida.objects.all()
        })
    return render(request, 'unidad.html',{
        'unidades': unidad_Medida.objects.all()
    })
    
def eliminarUnidad(request, id):
    unidad_Medida.objects.get(id=id).delete()
    return HttpResponseRedirect('/unidad')

def laboratorio_views(request):
    if request.method=='POST':
        texto = request.POST['labname']
        laboratorio(nombre = texto).save()
        return render(request, 'laboratorio.html',{
            'laboratorios': laboratorio.objects.all()
            })
    return render(request, 'laboratorio.html',{
        'laboratorios': laboratorio.objects.all()
    })
    
def eliminarLaboratorio(request, id):
    laboratorio.objects.get(id=id).delete()
    return HttpResponseRedirect('/laboratorio')

def via_views(request):
    if request.method == 'POST':
        texto = request.POST['nuevaVia']
        via_consumo(nombre = texto).save()
        return render(request, 'via.html',{
            'vias': via_consumo.objects.all()
        })
    
    return render(request, 'via.html',{
        'vias': via_consumo.objects.all()
    })
    
def eliminarVia(request, id):
    via_consumo.objects.get(id=id).delete()
    return HttpResponseRedirect('/via')

def productos_views(request):
    return render(request, 'productos.html',{
        'form': nuevo_producto(),
        'productos': producto.objects.all().order_by('id').reverse()
    })
    
def guardar_producto_views(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        codigo = data['codigo']
        prod = producto.objects.all()
        
        for i in prod:
            if i.codigo == codigo:
                return JsonResponse({'mensaje': 'El Código ya existe'}, status=400)

        nombre_generico = data['nombre_generico']
        nombre_cientifico = data['nombre_cientifico']
        descripcion = data['descripcion']
        cat = data['categoria']
        via = data['via']
        receta = bool(data['receta'])
        lab = data['laboratorio']
        unidad_medida = data['unidad']
        codigo = data['codigo']
        
        producto(
            codigo = codigo,
            nombre_generico = nombre_generico,
            nombre_cientifico = nombre_cientifico,
            descripcion = descripcion,
            categoria = categoria.objects.get(id = cat),
            via = via_consumo.objects.get(id = via),
            req_receta = receta,
            laboratorio = laboratorio.objects.get(id = lab),
            unidad = unidad_Medida.objects.get(id = unidad_medida),
            precio = 0.0,
            fecha_vencimiento = '2023-01-01',
            cantidad = 0
        ).save()
        
        return JsonResponse({'mensaje': 'Producto guardado exitosamente'})
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)

def eliminarProducto_views(request, id):
    producto.objects.get(codigo=id).delete()
    return HttpResponseRedirect('/productos',{
        'form': nuevo_producto(),
        'productos': producto.objects.all().order_by('id').reverse()
    })
    
def compra_views(request):
    return render(request, 'compra.html',{
        'form': nueva_compra(),
    })
    
def nueva_compra_views(request):
    try:
        data = json.loads(request.body)
        print(data)
        cant = int(data['cantidad'])
        precio = float(data['precio'])
        
        compra(
            id_proveedor = proveedor.objects.get(id = data['proveedor']),
            id_producto = producto.objects.get(id = data['producto']),
            cantidad = data['cantidad'],
            precio_unidad = data['precio'],
            fecha_vencimiento = data['fecha']
        ).save()
        
        movimiento(
            entrada = False, 
            monto = float(cant*precio),
            fecha = datetime.now().date()
        ).save()
            
        prod = producto.objects.get(id = data['producto'])
        prod.fecha_vencimiento = data['fecha']
        prod.precio = (precio*1.35)
        prod.cantidad = prod.cantidad + cant
        prod.save()
        
        return JsonResponse({'mensaje': 'La compra se ha realizado con éxito'})	
    except Exception as e:
        return JsonResponse({'mensaje': str(e)})
    
def ventas_views(request):
    return render(request, 'ventas.html',{
        'form': nueva_venta(),
        'productos': producto.objects.all()
    })

def comprarProducto_views(request):
    try:
        carrito = json.loads(request.body)
        print(carrito)
        
        compras = carrito.get('compras', [])
        descuento = carrito.get('descuento', False)
        total = carrito.get('total', 0.0)
        medico = carrito.get('medico', '')
        codMinsa = carrito.get('codMinsa', '')
        
        for compra in compras:
            print(f"{compra['id']} {compra['cantidad']}")
            
            producto_id = compra.get('id')
            cantidad = compra.get('cantidad')
            precio_unitario = float(compra.get('precio'))
            
            producto_obj = producto.objects.get(id=producto_id)
            
            if descuento:
                monto = float(cantidad) * (producto_obj.precio * 0.9)
            else:
                monto = float(cantidad) * precio_unitario
            
            nueva_venta = venta(
                id_producto=producto_obj,
                cantidad=cantidad,
                monto=monto,
                fecha=datetime.now().date()
            )
            
            nueva_venta.save()
            print("Venta guardada correctamente.")
        
        movimiento(
            entrada = True,
            monto = total,
            fecha = datetime.now().date()
        ).save()
        
        if(medico and codMinsa):
            recetas(
                id_compra = nueva_venta,
                id_producto = producto.objects.get(codigo=producto_id),
                medico = medico,
                codMinsa = codMinsa
            ).save()
        
        #HACE FALTA AGREGAR EL MOVIMIENTO PARA EL INVENTARIO
        
        
        return JsonResponse({'mensaje': 'Entró al método correctamente'}, status=200)
    
    except producto.DoesNotExist as e:
        return JsonResponse({'mensaje': f'Error: Producto con id {producto_id} no encontrado.'}, status=400)
    except Exception as e:
        return JsonResponse({'mensaje': str(e)}, status=500)