from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
    path('help/', views.help, name='help'),
]