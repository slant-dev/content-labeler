from django.db import models

class Article(models.Model):
    author = models.CharField(max_length=60)
    headline = models.CharField(max_length=140) # A headline can't be longer than a tweet, right?
    pub_date = models.DateTimeField('date published')
