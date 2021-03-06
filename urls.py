from django.conf.urls.defaults import *
from django.contrib import admin

from whalesalad.blog import redirects as blog_redirects, views as blog_views
from whalesalad.misc import views as misc_views

# Admin-site autodiscovery shiz
admin.autodiscover()

urlpatterns = patterns('',
    # Application includes
    url(r'^blog/', include('whalesalad.blog.urls')),
    
    # Wordpress redirect relics
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[\w-]+)/$', blog_redirects.post_detail, name='wp_post_detail'),
    
    # Miscellaneous URLs and stuff
    url(r'^/?$', blog_views.index, name='home'),
    url(r'^about/$', misc_views.about, name='about'),
    
    # Static pages
    url(r'^elixir/$', 'django.views.generic.simple.direct_to_template', { 'template': 'static/elixir.html' }),
    # Contact as static for now until its dynamic :D
    url(r'^contact/$', 'django.views.generic.simple.direct_to_template', { 'template': 'static/contact.html' }),
    
    # Django admin shiz
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)
