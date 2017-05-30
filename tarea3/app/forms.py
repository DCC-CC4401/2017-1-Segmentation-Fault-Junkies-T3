from django import forms

from .models import OPCIONES_FORMAS_DE_PAGO, Producto


class Signup_Common(forms.Form):
    username = forms.CharField(label='Usuario', max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(), label='Contraseña', max_length=20)
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Repita la contraseña ingresada')
    nombre = forms.CharField(label='Nombre', max_length=30)
    email = forms.EmailField(label='Email')


class Signup_VendedorFijo(Signup_Common):
    formas_de_pago = forms.MultipleChoiceField(label='Formas de pago', choices=OPCIONES_FORMAS_DE_PAGO)
    hora_inicio = forms.TimeField(label='Hora de Inicio')
    hora_termino = forms.TimeField(label='Hora de Termino')
    foto_perfil = forms.ImageField(label='Foto de Perfil')


class Signup_VendedorAmbulante(Signup_Common):
    formas_de_pago = forms.MultipleChoiceField(label='Formas de pago', choices=OPCIONES_FORMAS_DE_PAGO)
    foto_perfil = forms.ImageField(label='Foto de Perfil')


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = [
            'nombre',
            'precio',
            'cantidad',
            'descripcion',
            'categoria',
            'foto',
        ]
        labels = {
            'nombre': 'Nombre del producto',
            'precio': 'Precio del producto',
            'cantidad': 'Stock del producto',
            'descripcion': 'Descripción',
            'categoria': 'Categoría',
            'foto': 'Imagen del producto',
        }