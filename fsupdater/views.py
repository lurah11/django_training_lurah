from django.shortcuts import render
from django.http import JsonResponse
import requests
from datetime import date
from .models import Entity,News
from django.db import connection
from django.conf import settings
import os 
import threading
import schedule
import time 
from .helpers import get_news

# Create your views here.





# INITIAL SETUP 
base_dir = settings.BASE_DIR

sql_file = os.path.join(base_dir,"fsupdater","sql_to_populate_entity.txt")

with open (sql_file,"r") as sql_insert : 
    sql_statement = sql_insert.read()


qs_entity = Entity.objects.all()

if qs_entity : 
    pass 
else : 
    with connection.cursor() as cursor : 
        cursor.execute(sql_statement)

fs_list = ['bpom','fssc','gfsi','codex','usfda']

        


# VIEWS FUNCTION
def fsupdater_home_view(request): 
    
    return render(request,'fsupdater/fsupdater.html')


def reg_auto_update_view(): 
    News.objects.all().delete()
    print("deleted")

    for fs in fs_list : 
        get_news(fs)

def reg_check_view(request): 
    list_news = News.objects.all() 

    context = {
        'list_news': list_news
    }
    return render(request,'fsupdater/fsupdater.html',context=context)

def entity_detail_view(request):
    entities = Entity.objects.all()

    return render(request,'fsupdater/entity.html',context={'entities':entities})














# AUTO UPDATER FUNCTION 

def run_continuously(interval=1):
    cease_continuous_run = threading.Event()
    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.daemon=True
    continuous_thread.start()
    return cease_continuous_run


schedule.every().day.at("11:38:30").do(reg_auto_update_view)


# Start the background thread
stop_run_continuously = run_continuously()
        