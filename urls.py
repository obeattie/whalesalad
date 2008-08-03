from django.conf.urls.defaults import *
from django.contrib import admin

# Admin-site autodiscovery shiz
admin.autodiscover()

urlpatterns = patterns('',
    (r'^blog/', include('whalesalad.blog.urls')),
    
    # Django admin shiz
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)
