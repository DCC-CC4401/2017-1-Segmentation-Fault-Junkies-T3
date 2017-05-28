from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as enter
from django.contrib.auth.models import User, Group
from .models import Alumno


def index(request):
    return HttpResponse(render(request, 'app/index.html', {}))


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
            if tipo == '3':
                u = User.objects.create_user(email, email, contraseña)
                u.first_name = nombre
                u.save()
                Alumno.objects.create(user=u)
                return HttpResponse("Usuario creado")
            return HttpResponse("Usuario no creado")

        else:
            return HttpResponse(render(request, 'app/signup.html', {'errores': "las constraseñas no coinciden"}))

    else:
        return HttpResponse(render(request, 'app/signup.html', {}))


def vendedor(request):
    return HttpResponse(render(request, 'app/vendedor-profile-page.html', {}))
