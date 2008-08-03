from django.contrib import admin

from whalesalad.generic.tagging import models as tagging_models

admin.site.register(tagging_models.TaggedItem)
admin.site.register(tagging_models.Tag)
