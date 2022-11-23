from django.shortcuts import render



def dsml_home_view(request): 

    return render(request,'dsml/dsml.html')