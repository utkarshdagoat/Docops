from rest_framework import serializers
from .models import User
from spaces.models import Space

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , 'year' , 'display_picture' , 'email']


class UserSpacesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = ['name','creater']
    