from fsupdater.helpers import get_news
from fsupdater.models import News


fs_list = ['bpom','fssc','gfsi','codex','usfda']

def reg_auto_update_view():
    News.objects.all().delete()
    print("deleted")

    for fs in fs_list :
        print(fs)
        get_news(fs)
        print("agustinusbatubara")

reg_auto_update_view()