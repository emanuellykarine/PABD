from .views import RegistroUsuarioView, LoginUsuarioView, LogoutUsuarioView, PerfilUsuarioView
from django.urls import path

urlpatterns = [
    path('auth/registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('auth/login/', LoginUsuarioView.as_view(), name='login'),
    path('auth/logout/', LogoutUsuarioView.as_view(), name='logout'),
    path('auth/perfil/', PerfilUsuarioView.as_view(), name='perfil'),
]