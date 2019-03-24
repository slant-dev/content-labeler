from datetime import datetime, timedelta

from newsapi import NewsApiClient
from random import shuffle

import argparse, pickle

# Curate my news
US_SOURCES = [ 'associated-press',
            'abc-news',
            'cnn',
            'fox-news',
            'nbc-news',
            'the-new-york-times',
            'the-wall-street-journal',
            'the-washington-post',
            'time',
            'usa-today',]

# Folder for storage
DATA_FOLDER = 'data'

# Get the most popular articles (in the US, in English)

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
    def __init__(self, api_key='f43be2cf7376472392acfa364f33cbbe'):
        self.api_key = api_key
        self.api = NewsApiClient(api_key=api_key)

    ''' Main API functions. '''

    def get_articles_for_date(self, day='2019-03-01'):
        # Get all articles from my sources (max 1000 articles per list anyway)
        articles = []
        for src in US_SOURCES:
            articles.extend(self.get_todays_articles(day=day, sources=src, max_articles=100))#0))

        print('Grabbed {} articles from {} sources'.format(len(articles), len(US_SOURCES)))

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
    def get_todays_articles(self, date=None, sources=US_SOURCES, max_articles=60):
        if not date: date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        return self.get_todays_articles_recur(date, sources=sources, page=1, max_articles=max_articles)


def validate_dates(start_date, end_date):
    '''Make sure valid start day and end day provided.'''
    if not end_date:
        end_date = start_date
    date1 = datetime.strptime(start_date, '%Y-%m-%d')
    date2 = datetime.strptime(end_date,   '%Y-%m-%d')
    days_between = (date2 - date1).days
    if days_between <= 0:
        print ("Start day must be before end day")
    elif days_between > 365:
        print ("Cannot grab more than one year's worth of data")
    return date1, date2

def pickle_list(_list, filename):
    with open(filename, 'wb') as f:
        pickle.dump(_list, f)

def grab_and_save_articles(start_date, end_date):
    news_client = NewsClient()
    date_obj = start_date
    while date_obj <= end_date:
        date = date_obj.strftime('%Y-%m-%d')
        all_articles = []
        for source in US_SOURCES:
            # get articles
            articles = news_client.get_todays_articles(date=date,
                        sources=source, max_articles=1000)
            all_articles.extend(articles)
        # dedupe
        deduped_articles = _dedupe_articles(all_articles)
        # save to file
        filename = '{}/articles-{}.pkl'.format(DATA_FOLDER, date)
        print('Saved {} articles from {}.'.format(len(deduped_articles), date))
        pickle_list(deduped_articles, filename)
        # inc to next date
        date_obj += timedelta(days=1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_date", required=True, help="start date for article scraping, like 2019-03-20")
    parser.add_argument("--end_date",   required=False, help="optional end date for article scraping, like 2019-03-22")
    args = parser.parse_args()
    start_date, end_date = validate_dates(args.start_date, args.end_date)
    grab_and_save_articles(start_date, end_date)

main()
