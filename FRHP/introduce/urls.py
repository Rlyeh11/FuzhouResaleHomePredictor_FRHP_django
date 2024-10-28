from django.urls import path
from introduce import views

urlpatterns = [
    path('', views.introduceIndex, name='introduceIndex'),
    path('predict/', views.predictIndex, name='predictIndex'),
    path('test/', views.testIndex, name='testIndex'),
]