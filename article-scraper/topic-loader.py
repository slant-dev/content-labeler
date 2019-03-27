''' Loads topics from topics.txt into the django database.

Run in the django shell.'''

from labeler.models import Topic

topics = open('topics.txt').readlines()

for line in topics:
    name, color = [w.strip() for w in line.split(',')]
    Topic(name=name, color=color).save()
