from django.conf.urls.defaults import *
from django.contrib import admin

# Admin-site autodiscovery shiz
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', { 'template' : 'home.html' }),
    (r'^about/$', 'django.views.generic.simple.direct_to_template', { 'template' : 'about.html' }),

    (r'^', include('whalesalad.blog.urls')),
    
    # Django admin shiz
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)
