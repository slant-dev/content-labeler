from django import template
from django.utils.safestring import mark_safe

import hashlib
import urllib.parse

register = template.Library()

''' Gravatar stuff. '''

print('Loading template tags...')

# return only the URL of the gravatar
# TEMPLATE USE:  {{ email|gravatar_url:150 }}
def gravatar_url(email, size=40):
  email = email.encode('utf-8')
  default = "mp"
  return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.lower()).hexdigest(), urllib.parse.urlencode({'d':default, 's':str(size)}))

# return an image tag with the gravatar
# TEMPLATE USE:  {{ email|gravatar:150 }}
def gravatar(email, size=40):
    url = gravatar_url(email, size)
    return mark_safe('<img class="gravatar" src="%s" height="%d" width="%d">' % (url, size, size))

register.filter('gravatar_url', gravatar_url)
register.filter('gravatar', gravatar)
