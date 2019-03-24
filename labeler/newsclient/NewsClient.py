from newsapi import NewsApiClient
from random import shuffle

# Curate my news
MY_SRCS = [ 'associated-press',
            'abc-news',
            'cnn',
            'fox-news',
            'nbc-news',
            'the-new-york-times',
            'the-wall-street-journal',
            'the-washington-post',
            'time',
            'usa-today',]

# Get the most popular articles (in the US, in English)

import datetime

ARTICLES_PER_PAGE = 20
SORT_KEY = { 'popularity': 'popularity', 'relevancy': 'relevancy' }



def _dedupe_articles(articles):
    ''' Take a list of articles that may have duplicates and return a list of
        unique articles. (Articles are distinguished by headline.)'''
    # For now, let's just randomly choose one of the articles
    shuffle(articles)
    deduped_articles = []
    article_title_set = set()
    for article in articles:
        if article['title'] in article_title_set:
            continue
        else:
            article_title_set.add(article['title'])
            deduped_articles.append(article)
    print('Deduped {} articles down to {}'.format(len(articles), len(deduped_articles)))
    return deduped_articles

class NewsClient:
    def __init__(self, api_key='704b8497442b49b8a5cb33f734034509'):
        self.api_key = api_key
        self.api = NewsApiClient(api_key=api_key)

    ''' Main API functions. '''

    def get_articles_for_day(self, day='2019-03-01'):
        # Get all articles from my sources (max 1000 articles per list anyway)
        articles = []
        for src in MY_SRCS:
            articles.extend(self.get_todays_articles(day=day, sources=src, max_articles=100))#0))

        print('Grabbed {} articles from {} sources'.format(len(articles), len(MY_SRCS)))

        return _dedupe_articles(articles)


    ''' Helper functions, rarely called from outside the class. '''

    def get_todays_articles_recur(self, day, sources=None, page=1, max_articles=None):
        # print(max_articles)
        if max_articles <= 0:
            return []

        results = self.api.get_everything(sources=sources,
                                         from_param=day,
                                         to=day,
                                         page=page,
                                         language='en',
                                         sort_by=SORT_KEY['popularity'])
        articles = results['articles']
        if max_articles:
            max_articles -= len(articles)
        if len(articles) < ARTICLES_PER_PAGE:
            return articles
        else:
            return articles + self.get_todays_articles_recur(day, sources=sources, page=page+1, max_articles=max_articles)

    # day is in format like '2018-01-01'
    def get_todays_articles(self, day=None, sources=MY_SRCS, max_articles=60):
        if not day: day = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        return self.get_todays_articles_recur(day, sources=sources, page=1, max_articles=max_articles)
