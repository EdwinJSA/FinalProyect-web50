from django.db import models

# Create your models here.
class categoria(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nombre}"

    
class laboratorio(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nombre}"
    
class unidad_Medida(models.Model):
    nombre = models.CharField(max_length=50)
    minimo = models.IntegerField()
    
    def __str__(self):
        return f"Unidad: {self.nombre} minimo: {self.minimo}"
    
class via_consumo(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nombre}"
    
class producto(models.Model):
    codigo = models.CharField(max_length=50)
    nombre_generico = models.CharField(max_length=50)
    nombre_cientifico = models.CharField(max_length=50)
    descripcion = models.TextField()
    categoria = models.ForeignKey(categoria, on_delete=models.CASCADE)
    via = models.ForeignKey(via_consumo, on_delete=models.CASCADE)
    req_receta = models.BooleanField()
    laboratorio = models.ForeignKey(laboratorio, on_delete=models.CASCADE)
    unidad = models.ForeignKey(unidad_Medida, on_delete=models.CASCADE)
    precio = models.FloatField()
    fecha_vencimiento = models.DateField()
    cantidad = models.IntegerField()
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre_generico}"

    
class proveedor(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nombre}"    

class compra(models.Model):
    id_producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    id_proveedor = models.ForeignKey(proveedor, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unidad = models.FloatField()
    fecha_vencimiento = models.DateField()
    
    def __str__(self):
        return f"Proveedor: {self.id_proveedor} - Producto: {self.id_producto}"

class movimiento(models.Model):
    entrada = models.BooleanField()
    monto = models.FloatField()
    fecha = models.DateField()
    
    def __str__(self):
        return f"Entrada: {self.entrada} - Monto: {self.monto}"
    
class venta(models.Model):
    id_producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    monto = models.FloatField()
    fecha = models.DateField()
    
    def __str__(self):
        return f"Producto: {self.id_producto} - Monto: {self.monto}"
    
class recetas(models.Model):
    id_compra = models.ForeignKey(compra, on_delete=models.CASCADE),
    id_producto = models.ForeignKey(producto, on_delete=models.CASCADE),
    medico = models.CharField(max_length=50),
    codMinsa = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Medico: {self.medico} - Medicamento: {self.id_producto}"