import datetime

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q

class CommentManager(models.Manager):
    def get_public(self):
        return self.model.objects.filter(Q(
            Q(
                Q(Q(spam=False) & Q(processed=True)) | Q(approved=True)
            ) & Q(timestamp__lte=datetime.datetime.now())
        ))
    
    def get_for_object(self, obj, public_only=True):
        if public_only:
            qs = self.model.objects.get_public()
        else:
            qs = self.model.objects.all()
        return qs.filter(content_type=ContentType.objects.get_for_model(obj.__class__), object_id=obj.id)