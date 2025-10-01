from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from conta_comigo_app import views

router = DefaultRouter()
router.register(r'formularios', views.FormularioViewSet)
router.register(r'formularioquestoes', views.FormularioQuestaoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('conta_comigo_api/', include(router.urls)),
]
