from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from api import views # Importa todas as suas views de uma vez
from api import auth_views as custom_auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('history/', views.history, name='history'),
    path('sustainability/', views.sustainability, name='sustainability'),
    path('community/', views.community, name='community'),
    path('profile/', views.profile, name='profile'),
    path('calcular-impacto/', views.calcular_impacto_viagem, name='calcular_impacto'),
    path('register/', custom_auth_views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='dashboard'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]