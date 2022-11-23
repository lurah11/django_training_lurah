from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'digit'

urlpatterns = [
    path('', views.digit_home_view, name='digit-home-view'),
    path('calc',views.predict_digit_view,name='predict-digit-view')
]