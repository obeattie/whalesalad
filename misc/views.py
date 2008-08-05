import datetime

from django.conf import settings
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext

from whalesalad.blog.models import Post
from whalesalad.comments.models import Comment

def about(request):
    """The about page, which includes various statistics."""
    return render_to_response('static/about.html', {
        'akismet_counter': settings.INITIAL_AKISMET_COUNT + Comment.objects.filter(spam=True, approved=False, processed=True, timestamp__lte=datetime.datetime.now()).count(),
        'comments_counter': Comment.objects.get_public().count(),
        'posts_counter': Post.objects.get_published().count(),
    }, context_instance=RequestContext(request))
