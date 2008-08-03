"""Django administration stuff for the comments application."""
from django.contrib import admin

from whalesalad.comments import models as comments_models

class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ('author_name', 'author_email', 'timestamp', 'comment', 'approved', 'spam', 'processed', )
    list_filter = ('timestamp', 'approved', 'spam', 'site', )
    search_fields = ('comment', 'author_name', 'author_email', )
admin.site.register(comments_models.Comment, CommentAdmin)
