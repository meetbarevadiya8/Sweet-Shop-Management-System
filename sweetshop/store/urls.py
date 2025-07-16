from django.urls import path
from . import views

urlpatterns = [
    path('', views.sweet_list, name='sweet_list'),
    path('add/', views.add_sweet, name='add_sweet'),
    path('delete/<int:sweet_id>/', views.delete_sweet, name='delete_sweet'),
]