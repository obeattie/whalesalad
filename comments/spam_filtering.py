from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template import context, loader
from django.utils.encoding import smart_str

from whalesalad.comments.lib import akismet

class CommentModerator(object):
    akismet = True
    email_notification = False
    
    def __init__(self, comment, *args, **kwargs):
        self.comment = comment
        return super(CommentModerator, self).__init__(*args, **kwargs)
    
    def moderate(self):
        """Returns boolean as to whether the comment should be marked as spam or
           not. Only implements Akismet filtering at present."""
        if not self.akismet:
            # Akismet is not used, comment can't be moderated
            return False
        else:
            # Akismet is enabled
            akismet_api = akismet.Akismet(key=settings.AKISMET_API_KEY, blog_url='http://%s/' % Site.objects.get_current().domain)
            if akismet_api.verify_key():
                akismet_data = {
                    'blog': u'http://%s/' % self.comment.site.domain,
                    'user_ip': self.comment.author_ip,
                    'user_agent': u'',
                    'comment_type': 'comment',
                    'comment_author': self.comment.author_name,
                    'comment_author_email': self.comment.author_email,
                }
                try:
                    akismet_data.update({ 'permalink': self.comment.content_object.get_absolute_url() })
                except AttributeError:
                    # Content object doesn't have get_absolute_url
                    pass
                if self.comment.author_url:
                    akismet_data.update({ 'comment_author_url': self.comment.author_url })
                # Send the request
                if akismet_api.comment_check(smart_str(self.comment.comment), data=akismet_data, build_data=True):
                    # SPAM ALERTZ!!!
                    return True
        return False
    
    def notify(self):
        if not self.email_notification:
            return
        recipient_list = [manager_tuple[1] for manager_tuple in settings.MANAGERS]
        t = loader.get_template('comments/comment_notification_email.txt')
        c = context.Context({ 'comment': self.comment.comment,
                      'content_object': self.comment.content_object })
        subject = u'[%s] New comment posted on "%s"' % (self.comment.site,
                                                          self.comment.content_object)
        message = t.render(c)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)
    
    def process(self):
        if self.moderate():
            self.comment.spam = True
        # Set the processed flag and save
        self.comment.processed = True
        self.comment.save()
        # Send notifications
        self.notify()
        return