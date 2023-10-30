from django.db import models

from .space import Space
from myauth.models import User
from constants.constants import REQUEST_STATE


class Request(models.Model):
    space = models.ForeignKey(to=Space , on_delete=models.CASCADE)
    from_user = models.ForeignKey(to=User , on_delete=models.CASCADE)
    state = models.CharField(choices=REQUEST_STATE)

    @property
    def invite_code(self):
        return self.space.invite_code 
    
    @property
    def permission(self):
        return self.from_user.has_perm("spaces.can_edit_file")