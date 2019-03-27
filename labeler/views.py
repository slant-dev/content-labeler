from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from .models import Article, Topic

import random

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

def get_next_article(user):
    articles = Article.objects.order_by('pub_date').all()
    return random.choice(articles)

def label_articles(request):
    article = get_next_article(request.user)
    if request.method == 'POST':
        data = serializers.serialize('json', [article])
        return HttpResponse(data, content_type="application/json")
    else:
        params = dict(
            article = article,
            topics  = Topic.objects.all()
        )
        return render(request, 'label_articles.html', params)

def label_sentences(request):
    return render(request, 'label_sentences.html')
