from django.db import models
from myauth.models import User
import uuid

# Create your models here.

class Space(models.Model):
    name = models.CharField(max_length=32 , unique=True)
    creater = models.ForeignKey(to=User ,related_name="workspace_creater", on_delete=models.CASCADE )
    isPrivate = models.BooleanField(default=False)# Create your models here.
    users = models.ManyToManyField(to=User , null=True)
    invite_code = models.UUIDField(default=uuid.uuid4)
    description = models.CharField(max_length=200)

    class Meta:
        permissions = [
            ('can_create_file' , "Can Create File"),
        ]