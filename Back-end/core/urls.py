from django.contrib import admin
from django.urls import path
from api import views # Importa todas as suas views de uma vez

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('history/', views.history, name='history'),
    path('sustainability/', views.sustainability, name='sustainability'),
    path('community/', views.community, name='community'),
    path('profile/', views.profile, name='profile'),
]