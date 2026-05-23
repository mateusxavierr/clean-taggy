from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from api import views # Importa todas as suas views de uma vez

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('history/', views.history, name='history'),
    path('sustainability/', views.sustainability, name='sustainability'),
    path('community/', views.community, name='community'),
    path('profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='dashboard'), name='logout'),
<<<<<<< Updated upstream
]
=======
]
>>>>>>> Stashed changes
