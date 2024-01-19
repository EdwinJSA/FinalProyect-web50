from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import categoria, proveedor, unidad_Medida, laboratorio, via_consumo
from .forms import *
from django.http import HttpResponse, JsonResponse
import json
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
        ).save()
        
        return JsonResponse({'mensaje': 'Producto guardado exitosamente'})
    else:
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)