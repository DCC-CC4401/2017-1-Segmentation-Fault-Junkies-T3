from django.contrib import admin

from .models import Vendedor, Vendedor_Ambulante, Vendedor_Fijo, Alumno, Seguimiento, Producto

admin.site.register(Vendedor);
admin.site.register(Vendedor_Ambulante);
admin.site.register(Vendedor_Fijo);
admin.site.register(Alumno);
admin.site.register(Seguimiento);
admin.site.register(Producto);
