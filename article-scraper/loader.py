''' Loads pickled articles from data/ into database.

Run in the django shell.'''

import pickle, glob

from labeler.models import Article

for filename in  glob.glob('article-scraper/data/*'):
    print(filename)
    with open(filename, "rb") as fp:
        articles = pickle.load(fp)
        for article_json in articles:
            # print(article_json)
            # clean_article_json = article_json.encode('utf-8').strip()
            a = Article.parse_from_json(article_json)
            # print('a:', a)
            a.save()
