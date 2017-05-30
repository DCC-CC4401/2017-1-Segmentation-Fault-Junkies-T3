from django.contrib.auth import authenticate, login as enter, logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProductoForm
from .models import Alumno, Vendedor_Fijo, Vendedor_Ambulante, Vendedor, Producto, Seguimiento


def index(request):
    # Aquí es posible obtener el usuario adjunto en el request, ver si está autentificado, y si es necesario, obtener
    # detalles sobre él para pasárselos al template."""

    # Se utilizan los grupos de django para checkear rápidamente de qué tipo de usuario se trata. En el signup se le
    # asoció el grupo respectivo al usuario creado. Los grupos son "Clientes", "Vendedores_Fijos",
    # "Vendedores_Ambulantes" y deben ser creados manualmente en la máquina donde corre la aplicación
    # (e.g >>> Group.objects.create(name="Clientes"))
    context = get_global_context(request)
    context['map'] = True
    if not context['authenticated'] or context['user_type'] == "Clientes":
        return render(request, 'app/index.html', context)
    elif context['user_type'] == "Vendedores_Fijos" or context['user_type'] == "Vendedores_Ambulantes":
        return redirect('vendedor', id_vendedor=request.user.id)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            enter(request, user)
            return redirect('index')
        else:
            #TODO return error, 403 or w/e
            return redirect('login')

    else:
        return HttpResponse(render(request, 'app/login.html', {}))


def signup(request):
    if request.method == 'POST':
        # tipo de usuario
        tipo = request.POST['tipo']
        # nombre de la persona
        nombre = request.POST['nombre']
        # correo usuario, usado también como username
        email = request.POST['email']

        foto_perfil = request.POST['foto_perfil']
        contraseña = request.POST['password']
        contraseña_r = request.POST['password2']

        if contraseña == contraseña_r:
            if tipo != '1' and tipo != '2' and tipo != '3':
                return HttpResponse("Usuario no creado")
            u = User.objects.create_user(email, email, contraseña)
            u.first_name = nombre
            if tipo == '1':
                g = Group.objects.get(name="Vendedores_Fijos")
                Vendedor_Fijo.objects.create(user=u, foto_perfil=foto_perfil)
            elif tipo == '2':
                g = Group.objects.get(name="Vendedores_Ambulantes")
                Vendedor_Ambulante.objects.create(user=u, foto_perfil=foto_perfil)
            elif tipo == '3':
                g = Group.objects.get(name="Clientes")
                Alumno.objects.create(user=u, foto_perfil=foto_perfil)
            g.user_set.add(u)
            u.save()
            return redirect("login")

        else:
            return HttpResponse(render(request, 'app/signup.html', {'errores': "las constraseñas no coinciden"}))

    else:
        return HttpResponse(render(request, 'app/signup.html', {}))


def signout(request):
    logout(request)
    return redirect('index')


def vendedor(request):
    if not request.user.is_authenticated or request.user.groups.all()[0] == 'cliente':
        raise Http404("Alumno intenta acceder a su profile de vendedor.")
    if request.user.groups.all()[0].name == 'Vendedores_Ambulantes':
        return vendedor_ambulante(request, request.user.id)
    if request.user.groups.all()[0].name == 'Vendedores_Fijos':
        return vendedor_fijo(request, request.user.id)


def vendedor_ambulante(request, id_vendedor):
    v = get_object_or_404(Vendedor_Ambulante, pk=id_vendedor)
    context = get_global_context(request)
    context.update({
        'nombre_vendedor': v.user.first_name,
        'tipo_vendedor': 'Ambulante',
        'estado_vendedor': v.actividad,
        'formas_pago': v.formas_de_pago,
        'num_favoritos': Seguimiento.objects.filter(vendedor=id_vendedor).count(),
        'productos': Producto.objects.filter(vendedor=id_vendedor)
    })
    return render(request, 'app/vendedor-profile-page.html', context)


def vendedor_fijo(request, id_vendedor):
    v = get_object_or_404(Vendedor_Ambulante, pk=id_vendedor)
    context = get_global_context(request)
    context.update({
        'nombre_vendedor': v.user.first_name,
        'tipo_vendedor': 'Fijo',
        'horainicio_vendedor': v.hora_inicio,
        'horatermino_vendedor': v.hora_termino,
        'estado_vendedor': v.actividad,
        'formas_pago': v.formas_de_pago,
        'num_favoritos': Seguimiento.objects.filter(vendedor=id_vendedor).count(),
        'productos': Producto.objects.filter(vendedor=id_vendedor)
    })
    return render(request, 'app/vendedor-profile-page.html', context)


def gestion_productos(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = Vendedor.objects.get(user=request.user)
            producto.save()
            return redirect('index')
        else:
            print('no')
    else:
        form = ProductoForm()
    return render(request, 'app/producto_form.html', {'form':form})


# El contexto general que se pasa a los templates, incluye un bool que indica si hay usuario logeado, tipo de usuario,
# id, nombre.
def get_global_context(request):
    context = {}
    if not request.user.is_authenticated:
        context['authenticated'] = False
    else:
        g = request.user.groups.all()[0]
        context.update({
            'authenticated': True,
            'user_id': request.user.id,
            'user_name': request.user.get_short_name()
        })
        if g.name == "Clientes":
            context['user_type'] = 'cliente'
        elif g.name == "Vendedores_Fijos":
            context['user_type'] = 'vendedor_fijo'
        elif g.name == "Vendedores_Ambulantes":
            context['user_type'] = 'vendedor_ambulante'
    return context
