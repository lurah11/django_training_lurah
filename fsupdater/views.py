from django.shortcuts import render
from django.http import JsonResponse
import requests
from datetime import date

# Create your views here.

def fsupdater_home_view(request): 
    
    return render(request,'fsupdater/fsupdater.html')


def reg_update_view(request): 
    if request.method == 'POST': 
        news = request.POST.get('news')
        url = requests.get('https://www.pom.go.id/new/browse/more/pers/16-11-2022/23-11-2022/1')
        return JsonResponse({'ok':'terkirim'})