from django.urls import path
from core import views
from users import views as users_views
from organization import views as organization_views
from django.contrib.auth.views import LogoutView

core_urlpatterns = [
    path('', views.home, name='home'),    
    path('check_profile', views.check_profile, name='check_profile'), 
    path('main_admin', views.main_admin, name='main_admin'),
    path('welcome/', users_views.welcome_view, name='welcome'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('crear-usuario/', users_views.crear_usuario_simple, name='crear_usuario_simple'),
    path('crear-direccion/', users_views.crear_direccion, name='crear_direccion'),
    path('listar-usuarios/', users_views.listar_usuarios, name='listar_usuarios'),
    path('asignar-cargo/', users_views.asignar_cargo, name='asignar_cargo'),
    path('administracion/', users_views.administracion, name='administracion'),
]