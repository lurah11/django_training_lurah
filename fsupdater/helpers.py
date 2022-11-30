from fsupdater.models import Entity,News
import re
import requests
from datetime import date,timedelta,datetime
from bs4 import BeautifulSoup as Bs
import re

# LIST OF CONSTANTS
indonesian_month_mapper = {
    'Januari':'January',
    'Februari':'February',
    'Maret':'March',
    'April':'April',
    'Mei':'May',
    'Juni':'June',
    'Agustus':'August',
    'September':'September',
    'Oktober' :'October',
    'November':'November',
    'Desember':'December'
}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

today = date.today()
last_week = today - timedelta(days=7)




def check_zero_pad_date(fs,str_date):
    if fs == "usfda":
        split = re.split(' |, ',str_date)

        if len(split[1]) == 1 :
            split[1] = "0" + split[1]

            return " ".join(split)
        else :


            return str_date
    elif fs == "fssc":
        split = re.split(' ',str_date)

        if len(split[0])==1:
            split[0] = "0"+split[0]
            return " ".join(split)
        else :
            return str_date
    elif fs == 'bpom':
        split = re.split(' ',str_date)
        split[1] = indonesian_month_mapper[split[1]]
        if len(split[0]) == 1 :
            split[0] = "0"+split[0]
            return " ".join(split)
        else :
            return " ".join(split)

def check_date_within_a_week(fs,d,last_week_date):
        date_object = None
        if fs == 'fssc':

            matched = re.findall('\d+ .+, \d{4}',d)
            if matched :
                new_str = check_zero_pad_date(fs,matched[0])
                date_object = datetime.strptime(new_str,"%d %B, %Y")

        elif (fs == 'gfsi' or fs == 'codex' or fs == 'bpom'):
            matched = re.findall('\d+ .+ \d{4}',d)
            if matched :
                if fs == 'gfsi':
                    date_object = datetime.strptime(matched[0],"%d %b %Y")
                elif fs == 'codex':
                    date_object = datetime.strptime(matched[0],"%d %B %Y")
                elif fs == 'bpom':
                    new_str = check_zero_pad_date(fs,matched[0])

                    date_object = datetime.strptime(new_str,"%d %B %Y")

        elif fs == "usfda":
            matched = re.findall('.+ \d+, \d{4}',d)
            if matched :
                new_str = check_zero_pad_date(fs,matched[0])
                date_object = datetime.strptime(new_str,"%B %d, %Y")
        if date_object :
            if date_object.date() >= last_week_date :
                str_date = date_object.date().strftime("%d %B %Y")


                return str_date
            else :
                return "not_valid"
        else :
            return "not_valid"



def create_news_dict(fs,list_news,list_dates,today_date,last_week_date):
     news_dict = {}
     for d,n in zip(list_dates,list_news):

          valid_date = check_date_within_a_week(fs,d,last_week_date)

          if valid_date != 'not_valid' :
              news_dict[n] = valid_date

     if len(news_dict) == 0 :
              str_today = today_date.strftime("%d %B %Y")
              news_dict["No update this week"] = str_today

     return news_dict


def get_news(fs):
        entity = Entity.objects.get(fs=fs)
        url = entity.url
        news_pat = entity.news_pat
        date_pat = entity.date_pat
        req = requests.get(url,headers=headers)
        bs = Bs(req.content,'lxml')
        dates = bs.select(date_pat)
        news = bs.select(news_pat)
        if entity.fs == 'usfda':
            list_date = [x.getText() for x in dates]
            list_news = []
            for n in news :
                new_n = re.sub('.+ \d+, \d{4}\n - ','',n.getText())
                list_news.append(new_n)
        else :
            list_date = [x.getText() for x in dates]
            list_news = [x.getText() for x in news]

        news_dict = create_news_dict(entity.fs,list_news,list_date,today,last_week)

        for key,value in news_dict.items() :
            is_exist = News.objects.filter(name=entity,news=key,date=value)
            if not is_exist:
                new_news = News.objects.create(
                    name = entity,
                    date = value,
                    news = key
                )
                new_news.save()





