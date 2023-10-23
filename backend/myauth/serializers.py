from rest_framework import serializers
from .models import User
from spaces.models import Space

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , 'year' , 'display_picture' , 'email']


class UserSpacesSerializers(serializers.ModelSerializer):
    users = UserSerializers(many=True , read_only=True)
    class Meta:
        model = Space
        fields = ['name' , 'description', 'users' , 'isPrivate' , 'creater' ,'invite_code']
    


class UserLoginResponseSerailizer(serializers.Serializer):
    isLoggedIn = serializers.BooleanField(default=False)
    user = UserSerializers()
    




















