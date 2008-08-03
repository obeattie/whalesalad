from django import newforms as forms
from django.utils.safestring import mark_safe

class CommentPostForm(forms.Form):
    author_name = forms.CharField(label='Your name', max_length=250, required=True)
    author_email = forms.EmailField(label='Your email address', max_length=75, required=True, help_text='Never shared with anyone')
    author_url = forms.URLField(label='Your URL (optional)', max_length=200, required=False, help_text='For a link back to your site.')
    comment = forms.CharField(required=True, min_length=12, widget=forms.Textarea, \
        help_text=mark_safe(u'You may add formatting to your comment by using <a href="http://daringfireball.net/projects/markdown/syntax" target="new">Markdown Syntax</a>. <strong>Any HTML will be removed</strong>.'))
