from django.urls import path
from . import views

urlpatterns = [
    path('', views.sweet_list, name='sweet_list'),
    path('add/', views.add_sweet, name='add_sweet'),
    path('delete/<int:sweet_id>/', views.delete_sweet, name='delete_sweet'),
    path('purchase/', views.purchase_sweet, name='purchase_sweet'),
    path('purchase/<int:sweet_id>/', views.purchase_sweet, name='purchase_sweet'),
    path('restock/', views.restock_sweet, name='restock_sweet'),
    path('restock/<int:sweet_id>/', views.restock_sweet, name='restock_sweet'),
]