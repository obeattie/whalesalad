"""URL-centric template filters."""
import hashlib, urllib, urlparse

from django.conf import settings
from django.contrib.sites.models import Site
from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

@register.filter('absoluteurl')
def absolute_url(value):
    """Ensures that the URL passed in is absolute (i.e. it has a
       domain name, and the http:// prepended to it.) The filter
       won't choke if you give it an already-absolute URL, however."""
    parsed = urlparse.urlparse(value)
    
    if parsed.hostname and parsed.scheme:
        # The URL is already absolute
        return value
    else:
        # The URL is relative
        if value[0] == '/':
            value = value[1:]
        return u'http://%s/%s' % (Site.objects.get_current().domain, value)

def default_gravatar_url():
    """The default (i.e. fallback URL to use when no Gravatar is available.)"""
    return absolute_url(settings.DEFAULT_AVATAR_PATH)

@register.filter
def gravatar(email, size=51):
    """Returns a Gravatar URL for the email passed in."""
    url = 'http://www.gravatar.com/avatar/%s?' % hashlib.md5(email.strip().lower()).hexdigest()
    url += urllib.urlencode({
        'size': unicode(int(size)),
        'r': 'pg',
        'd': default_gravatar_url(),
    })
    return mark_safe(url)
       