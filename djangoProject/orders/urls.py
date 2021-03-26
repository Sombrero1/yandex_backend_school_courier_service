from django.urls import path
from orders import views

urlpatterns = [
    path('', views.index),
    path('/assign', views.assign),
    path('/complete', views.complete),
]
