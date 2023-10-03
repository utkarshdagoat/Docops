import uuid

from rest_framework import serializers

from spaces.models.space import Space
from spaces.models.request import Request
from myauth.models import User

from spaces.services import doesSpaceNameExist , SpaceInstanceFromContext , RequestInstanceForSendingRequest , updateRequestInstance

from constants.constants import REQUEST_STATE


class PublicSpaceSerializer(serializers.ModelSerializer):
    creater = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    isPrivate = serializers.BooleanField(default=False , read_only=True)
    invite_code = serializers.UUIDField(default=uuid.uuid4 , read_only=True)
    class Meta:
        model = Space 
        fields= ['name' , 'creater' , 'isPrivate' , 'invite_code' ]

    def create(self, validated_data):
        return SpaceInstanceFromContext(context=self.context , validated_data=validated_data)


class PrivateSpaceSerializer(serializers.ModelSerializer):
    creater = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True 
    )
    users = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    isPrivate = serializers.BooleanField(default=True , read_only=True)
    invite_code = serializers.UUIDField(default=uuid.uuid4 , read_only=True)
    class Meta:
        model=Space
        fields=[ 'name' ,'creater' , 'users' , 'invite_code' , 'isPrivate']

    def create(self,validated_data):
        return SpaceInstanceFromContext(context=self.context , validated_data=validated_data)

