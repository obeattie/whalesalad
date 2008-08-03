"""Django-admin-related stuff for the blog application."""
from django.contrib import admin

from whalesalad.blog import models as blog_models

class PostAdmin(admin.ModelAdmin):
    """Admin component for whalesalad.blog.models.Post."""
    date_hierarchy = 'published'
    list_display = ('title', 'published', 'is_public', 'author', )
    list_filter = ('published', 'author', 'is_public', 'categories', )
    prepopulated_fields = { 'slug': ('title', ) }
    search_fields = ('title', 'slug', 'intro', )
admin.site.register(blog_models.Post, PostAdmin)
    