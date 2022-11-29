from django.db import models

# Create your models here.

class Entity(models.Model): 
    name = models.CharField(max_length=100)
    fs = models.CharField(max_length=30)
    url = models.CharField(max_length=500)
    date_pat = models.CharField(max_length=100)
    news_pat = models.CharField(max_length=100)
    short_exp = models.CharField(max_length=500)

    def __str__(self) : 
        return f"{self.pk}-{self.name}"

class News(models.Model): 
    name = models.ForeignKey(Entity,on_delete=models.CASCADE)
    date = models.CharField(max_length=30)
    news = models.CharField(max_length=500)

    def __str__(self): 
        return f"{self.pk}-{self.name.name}-{self.date}"

