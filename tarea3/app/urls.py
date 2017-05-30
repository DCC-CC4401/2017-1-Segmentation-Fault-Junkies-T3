from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^vendedor/$', views.vendedor, name='vendedor'),
    url(r'^gestion-productos/$', views.gestion_productos, name='gestionproductos'),
    url(r'^signout/$', views.signout, name='signout'),
    # Es necesario para que un alumno pueda distinguir y visitar vendedores de distinto tipo
    # pero con mismo id.
    url(r'^vendedor/fijo/(?P<id_vendedor>[0-9]+)/$', views.vendedor_fijo, name='vendedor-fijo'),
    url(r'^vendedor/ambulante/(?P<id_vendedor>[0-9]+)/$', views.vendedor_ambulante, name='vendedor-ambulante')
]