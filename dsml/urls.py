from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'dsml'

urlpatterns = [
    path('', views.dsml_home_view, name='dsml-home-view'),
    path('digit/',include('digit.urls'))
]