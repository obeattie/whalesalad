"""Context processors for the blog application."""
from whalesalad.blog.models import Post

def add_recent_posts(request):
    """Adds the 5 most recent posts to a recent_posts context variable."""
    return { 'recent_posts': Post.objects.get_published().order_by('-published')[:5] }
