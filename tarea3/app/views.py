from django.contrib.auth import authenticate, login as enter, logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Alumno, Vendedor_Fijo, Vendedor_Ambulante


def index(request):
    # Aquí es posible obtener el usuario adjunto en el request, ver si está autentificado, y si es necesario, obtener
    # detalles sobre él para pasárselos al template."""

    if not request.user.is_authenticated:
        context = {
            'authenticated': False
        }
        return render(request, 'app/index.html', context)

    # Se utilizan los grupos de django para checkear rápidamente de qué tipo de usuario se trata. En el signup se le
    # asoció el grupo respectivo al usuario creado. Los grupos son "Clientes", "Vendedores_Fijos",
    # "Vendedores_Ambulantes" y deben ser creados manualmente en la máquina donde corre la aplicación
    # (e.g >>> Group.objects.create(name="Clientes"))
    g = request.user.groups.all()[0]
    if g.name == "Clientes":
        c = Alumno.objects.get(user=request.user)
        # información para entregar al template
        context = {
            'authenticated': True,
            'user_type': 'cliente',
            'user_id': request.user.id
        }
        return render(request, 'app/index.html', context)

    if g.name == "Vendedor_Fijo" or g.name == "Vendedor_Ambulante":
        # TODO redireccionar a la landpage de vendedores
        pass


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
                g = Group.objects.get(name="Vendedor_Fijo")
                Vendedor_Fijo.objects.create(user=u, foto_perfil=foto_perfil)
            elif tipo == '2':
                g = Group.objects.get(name="Vendedor_Ambulante")
                Vendedor_Ambulante.objects.create(user=u, foto_perfil=foto_perfil)
            elif tipo == '3':
                g = Group.objects.get(name="Clientes")
                g.user_set.add(u)
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
    return HttpResponse(render(request, 'app/vendedor-profile-page.html', {}))
