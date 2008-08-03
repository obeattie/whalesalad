"""Redirects for the blog application."""
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from whalesalad.blog import models as blog_models

def post_detail(request, year, month, day, slug):
    """Redirects from the old Wordpress structure to the new Django one, if the post
       exists."""
    date = datetime.datetime.strptime('%s-%s-%s' % (year, month, day), '%Y-%m-%d').date()
    date_range = (datetime.datetime.combine(date, datetime.time.min), datetime.datetime.combine(date, datetime.time.max))
    
    post = get_object_or_404(blog_models.Post, published__range=date_range, slug=slug)
    
    # Serve the redirect
    return HttpResponseRedirect(post.get_absolute_url())
