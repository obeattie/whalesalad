"""Comment-related template tags (and filters?)"""
from django import template

from whalesalad.comments.models import Comment

register = template.Library()

class CommentsNode(template.Node):
    def __init__(self, variable, dest_var, *args, **kwargs):
        self.variable, self.dest_var = template.Variable(variable), dest_var
        return super(CommentsNode, self).__init__(*args, **kwargs)
    
    def render(self, context, just_return=False):
        variable = self.variable.resolve(context)
        comments = Comment.objects.get_for_object(obj=variable, public_only=True).order_by('timestamp')
        if just_return:
            return comments
        else:
            context[self.dest_var] = comments
            return ''

@register.tag
def get_comments(parser, token, node_class=CommentsNode):
    try:
        tag_name, content_object, as_name, dest_var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(u'%r tag requires a content object and "as foo" to denote where to store the variable' % token.contents.split())
    return node_class(variable=content_object, dest_var=dest_var)

class CommentCountNode(CommentsNode):
    def render(self, context):
        context[self.dest_var] = super(CommentCountNode, self).render(context=context, just_return=True).count()
        return ''

@register.tag
def get_comment_count(parser, token):
    return get_comments(parser=parser, token=token, node_class=CommentCountNode)
