from django.db import models

class Article(models.Model):
    author = models.CharField(max_length=140, null=True)
    source_id = models.CharField(max_length=140)
    source_name = models.CharField(max_length=140)
    title = models.CharField(max_length=140) # A headline can't be longer than a tweet, right?
    url = models.CharField(max_length=400)
    image_url = models.CharField(max_length=400, null=True)
    content = models.TextField(null=True)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        """Return string representation of an Article.
        """
        return '"{}" – {}, {}'.format(self.title, self.author, self.source_name)

    def parse_from_json(json_obj):
        if ('title' not in json_obj or not json_obj['title']) \
                and 'description' in json_obj:
            json_obj['title'] = json_obj['description']
        for key in ['author', 'title', 'content', 'name',
            'urlToImage', 'url']:
            if key not in json_obj:
                json_obj[key] = None

        # print('source:', json_obj['source'])
        return Article(
            author = json_obj['author'],
            content = json_obj['content'],
            source_id = json_obj['source']['id'],
            source_name = json_obj['source']['name'],
            title = json_obj['title'],
            url = json_obj['url'],
            image_url = json_obj['urlToImage'],
            pub_date = json_obj['publishedAt'],
        )

class Topic(models.Model):
    name = models.CharField(max_length=40)
    color = models.CharField(max_length=12)

    def __str__(self):
        """ Returns a string representation of a Topic. """
        return '{} ({})'.format(self.name, self.color)
