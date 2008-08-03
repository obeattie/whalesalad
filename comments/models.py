import datetime

#from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models

from whalesalad.comments.managers import CommentManager
from whalesalad.comments.spam_filtering import CommentModerator
from whalesalad.misc.templatetags.urls import absolute_url as generate_absolute_url

class Comment(models.Model):
    """A comment by an unauthenticated user."""
    author_name = models.CharField(max_length=250, blank=False, null=False)
    author_email = models.EmailField(blank=False, null=False)
    author_url = models.URLField(blank=True, null=True)
    author_ip = models.IPAddressField(blank=False, null=False)
    timestamp = models.DateTimeField(blank=True, null=False)
    comment = models.TextField(blank=False, null=False)
    # Flags
    approved = models.BooleanField('approved by staff', default=False, help_text=u'If True, then this comment will always be displayed, regardless of spam filtering stuff.')
    spam = models.BooleanField('akismet thinks this is spam', default=False, editable=False)
    processed = models.BooleanField('processed by the filters', default=False, editable=False)
    is_whale = models.BooleanField('This comment was written by Michael', default=False, editable=True, help_text=u'If this is true, Michael posted the comment so adjust the template to reflect it\'s his comment')
    # Content Types stuff
    content_type = models.ForeignKey(ContentType, blank=False, null=False)
    object_id = models.PositiveIntegerField(blank=False, null=False)
#    content_object = GenericForeignKey()
    # Sites stuff
    site = models.ForeignKey(Site, blank=True, null=False)
    # Manager
    objects = CommentManager()
    
    class Moderator(CommentModerator):
        akismet = True
        email_notification = False
    
    def __unicode__(self):
        return self.comment
    
    def save(self, *args, **kwargs):
        self.timestamp = self.timestamp or datetime.datetime.now()
        try:
            self.site = self.site
        except Site.DoesNotExist:
            self.site = Site.objects.get_current()
        return super(Comment, self).save(*args, **kwargs)
    
    def get_relative_url(self):
        return u'%s#comment-%i' % (self.get_content_object().relative_url, self.id)
    relative_url = property(get_relative_url)
    
    def get_absolute_url(self):
        return generate_absolute_url(self.relative_url)
    
    def get_content_object(self):
        return self.content_type.model_class().objects.filter(id=self.object_id)[0]
