from .views import RegistroUsuarioView, LoginUsuarioView, LogoutUsuarioView, PerfilUsuarioView, PerfilUsuarioDetailView
from django.urls import path

urlpatterns = [
    path('api/auth/registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('api/auth/login/', LoginUsuarioView.as_view(), name='login'),
    path('api/auth/logout/', LogoutUsuarioView.as_view(), name='logout'),
    path('api/auth/perfil/', PerfilUsuarioView.as_view(), name='perfil')
]