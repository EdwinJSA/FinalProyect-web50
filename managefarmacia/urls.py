from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("categoria", views.categoria_views, name="categoria"),
    path("eliminarCategoria/<int:id>", views.eliminarCategoria, name="eliminarCategoria"),
    path("proveedores", views.proveedor_views, name="proveedor"),
    path("eliminarProveedor/<int:id>", views.eliminarProveedor, name="eliminarProveedor"),
    path("unidad", views.unidad_views, name="unidad"),
    path("eliminarUnidad/<int:id>", views.eliminarUnidad, name="eliminarUnidad"),
    path("laboratorio", views.laboratorio_views, name="laboratorio"),
    path("eliminarLaboratorio/<int:id>", views.eliminarLaboratorio, name="eliminarLaboratorio"),
    path("via", views.via_views, name="via"),
    path("eliminarVia/<int:id>", views.eliminarVia, name="eliminarVia"),
    path("productos", views.productos_views, name="productos"),
    path("guardar/", views.guardar_producto_views, name="guardar"),
    path("/eliminarProducto/<str:id>", views.eliminarProducto_views, name="eliminarProducto"),
    path("compra", views.compra_views, name="compra"),
    path("nuevaCompra", views.nueva_compra_views, name="nuevaCompra"),
    path("ventas", views.ventas_views, name="ventas"),
    path("comprarProducto/<str:codigo>", views.comprarProducto_views, name="comprarProducto"),
]
