from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.utils import simplejson, encoding

from blt.comments.models import Comment

def ajax_add_comment(request):
    """Adds a comment and returns a JSON response."""
    try:
        assert (
            'content_type_id' in request.GET and
            'object_id' in request.GET and
            'author_name' in request.GET and
            'author_email' in request.GET and
            'comment' in request.POST
        ), 'You did not supply all the required parameters'
    except AssertionError, error:
        return HttpResponse(simplejson.dumps({ 'response': 'error', 'extra': encoding.force_unicode(error.message) }))
    
    try:
        content_type = ContentType.objects.get_for_id(id=int(request.GET['content_type_id']))
        object_id = content_type.model_class().objects.filter(id=int(request.GET['object_id'])).id
    except:
        return HttpResponse(simplejson.dumps({ 'response': 'error', 'extra': u'Invalid parameters. (CT)' }))
    
    # Create the comment
    Comment.objects.create(
        author_name=request.GET['author_name'],
        author_email=request.GET['author_email'],
        author_url=request.GET['author_url'],
        author_ip=request.REMOTE_ADDR,
        comment=encoding.force_unicode(request.POST['comment']),
        approved=False,
        content_type=content_type,
        object_id=object_id
    )
    return HttpResponse(simplejson.dumps({
        'response': 'success',
        'extra': 'Your comment has been posted. Spam prevention measures and caching may cause it to take up to 5 minutes to appear on the site.'
    }))
