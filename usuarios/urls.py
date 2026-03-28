from django.urls import path
from .views import (cadastro, google_login, logout_view, me, perfil, editar_perfil, deletar_usuario, )

urlpatterns = [
    path("cadastro/", cadastro, name="cadastro"),
    path("google/", google_login, name="google_login"),
    path("logout/", logout_view, name="logout"),
    path("me/", me, name="me"),
    path("perfil/", perfil, name="perfil"),
    path("perfil/editar/", editar_perfil, name="editar_perfil"),
    path("perfil/deletar/", deletar_usuario, name="deletar_usuario"),
]