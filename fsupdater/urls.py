from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'fsupdater'

urlpatterns = [
    path('', views.fsupdater_home_view, name='fsupdater-home-view'),
    path('reg_update',views.reg_update_view,name='reg-update-view')
]