''' Loads pickled articles from data/ into database.

Run in the django shell.'''

import pickle, glob, gzip

from labeler.models import Article

for filename in sorted(glob.glob('article-scraper/data/*')):
    print(filename)
    with gzip.open(filename, "rb") as fp:
        articles = pickle.load(fp)
        for article_json in articles:
            a = Article.parse_from_json(article_json)
            a.save()
