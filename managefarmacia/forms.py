from django import forms
from .models import *

class nuevo_producto(forms.Form):
    codigo = forms.CharField(max_length=50)
    nombre_generico = forms.CharField(max_length=50)
    nombre_cientifico = forms.CharField(max_length=50)
    descripcion = forms.CharField(widget=forms.Textarea)
    categoria = forms.ModelChoiceField(queryset=categoria.objects.all())
    via = forms.ModelChoiceField(queryset=via_consumo.objects.all())
    req_receta = forms.BooleanField()
    laboratorio = forms.ModelChoiceField(queryset=laboratorio.objects.all())
    unidad_Medida = forms.ModelChoiceField(queryset=unidad_Medida.objects.all())
    
class nueva_compra(forms.Form):
    proveedor = forms.ModelChoiceField(queryset=proveedor.objects.all(), required=True)
    producto = forms.ModelChoiceField(queryset=producto.objects.all(), required=True)
    cantidad = forms.IntegerField(required=True)
    precio_unidad = forms.FloatField(required=True)
    fecha_vencimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'].index,
        required=True
    )
    
