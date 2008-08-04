from django.contrib import admin
from django.contrib.admin.util import quote
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from whalesalad.blog.managers import PostManager
from whalesalad.comments.models import Comment
from whalesalad.generic.tagging.models import Tag as GenericTag, TagManager as GenericTagManager
from whalesalad.generic.tagging.fields import TagField
from whalesalad.metadata.models import Category

class PostTag(GenericTag):
    """Post tags."""
    objects = GenericTagManager()

class Post(models.Model):
    title = models.CharField(max_length=250, blank=False, null=False)
    slug = models.SlugField(unique=True, blank=True, null=False)
    # Metadata
    published = models.DateTimeField(blank=False, null=False)
    author = models.ForeignKey(User, blank=False, null=False)
    is_public = models.BooleanField(default=False, help_text=_(u'Whether or not the entry is publicly viewable'))
    categories = models.ManyToManyField(Category, blank=True, null=True, related_name='blog_posts')
    tags = TagField(blank=True, null=True, model=PostTag)
    # The post
    intro = models.TextField(_(u'introduction'), blank=False, null=False)
    body = models.TextField(_(u'post body'), blank=True, null=True)
    # Manager
    objects = PostManager()
    
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('whalesalad.blog.views.post_detail', (), {
            'year': self.published.year,
            'month': self.published.strftime('%b').lower(),
            'day': self.published.day,
            'slug': self.slug,
        })
    
    def get_admin_url(self):
        return u'/admin/blog/post/%s/' % quote(self.id)
