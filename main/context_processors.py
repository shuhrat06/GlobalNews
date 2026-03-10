import datetime
from .models import Article, Category
import os
import requests
from django.db.models import Count
import random

def uzb_week_day(day):
    match day:
        case 'Monday': return 'Du'
        case 'Tue': return 'Se'
        case 'Wed': return 'Chor'
        case 'Thu': return 'Pay'
        case 'Fri': return "Juma"
        case 'Sat': return 'Shan'
        case 'Sun': return 'Yak'

def get_info(request):
    r = requests.get(
        url='https://api.weatherapi.com/v1/current.json?q=ferghana&lang=uzbek&key=357598a7cc044fb299f113455253010'
    ).json()
    weather_icon = r['current']['condition']['icon']
    weather_temp = r['current']['temp_c']
    eng_today = datetime.date.today().strftime("%a, %d.%m.%Y").split(',')
    today = uzb_week_day(eng_today[0])+","+eng_today[1]
    trending_article = Article.objects.order_by('-views').first()
    context={
        'today': today,
        'trending_article': trending_article,
        'weather': {
            'temp': weather_temp,
            'icon': weather_icon
        }
    }
    return context

def get_footer_images(request):
    articles = Article.objects.filter(published=True).order_by('-views')[:9]
    photos = []
    for article in articles:
        photos.append(article.cover.url)
    random.shuffle(photos)
    context = {'footer_photos': photos}
    return context

def get_famous_categories(request):
    all_categories = Category.objects.annotate(
        count = Count('article')
    ).order_by('-count')
    context = {'all_categories': all_categories}
    return context

def recent_articles(request):
    recent_articles = Article.objects.order_by('-id')[:2]
    return {'recent_articles': recent_articles}

    
    
# import os

# for d,dirs,files in os.walk('media'):
#     print(d)
#     print(dirs)
#     print(files)