from django.shortcuts import render
from django.http import HttpResponse

from .models import Article

''' Our HTML pages. '''
def index(request):
    return render(request, 'index.html')

def profile(request):
    return render(request, 'profile.html')

def statistics(request):
    return render(request, 'statistics.html')

def articles(request):
    max_articles = 100
    articles = Article.objects.order_by('pub_date').all()
    x = min(len(articles), max_articles)
    articles = articles[:x]
    params = dict(
        articles=articles
    )
    return render(request, 'articles.html', params)
