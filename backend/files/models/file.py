import uuid

from django.db import models
from myauth.models import User
from spaces.models.space import Space

# Create your models here.
class File(models.Model):
    createdBy =models.ForeignKey(to=User , on_delete=models.CASCADE)
    isPrivate = models.BooleanField(default=False)
    inviteCode = models.UUIDField(default=uuid.uuid4 , unique=True)
    users = models.ManyToManyField(to=User , related_name="allowed_user_for_file")
    space = models.ForeignKey(to=Space , on_delete=models.CASCADE)
    docId = models.CharField(max_length=24 , null=True , blank=True)
    heading  = models.CharField(max_length=64 , blank=True , null=True)
    cover = models.ImageField(upload_to="covers/" , null=True , blank=True)

    class Meta:
        permissions = [
           ('can_comment' , 'Can comment'),
           ('can_edit' , 'Can Edit')
        ]