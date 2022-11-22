from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'f0'

urlpatterns = [
    path('', views.f0_calc_view, name='f0-calc-view'),
    path('/calc',views.f0_calculation,name='f0-calculation-view')
]