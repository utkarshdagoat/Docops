from rest_framework import serializers
from .models import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username' , 'year' , 'display_picture' , 'email']

class MessageSerializers(serializers.Serializer):
    message=serializers.CharField(max_length = 100)
