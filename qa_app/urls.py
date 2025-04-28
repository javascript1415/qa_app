from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('qa/<int:document_id>/', views.qa, name='qa'),
    path('delete/<int:document_id>/', views.delete, name='delete'),
]