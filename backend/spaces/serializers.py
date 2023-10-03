import uuid

from rest_framework import serializers

from .models.space import Space
from .models.request import Request
from myauth.models import User

from .services import doesSpaceNameExist

from constants.constants import REQUEST_STATE


class PublicSpaceSerializer(serializers.ModelSerializer):
    creater = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    isPrivate = serializers.BooleanField(default=True , read_only=True)
    invite_code = serializers.UUIDField(default=uuid.uuid4 , read_only=True)
    class Meta:
        model = Space 
        fields= ['name' , 'creater' , 'isPrivate' , 'invite_code' ]

    def create(self, validated_data):
        validated_data['creater'] = self.context['request'].user 
        validated_data['isPrivate'] = False
        instance = Space.objects.create(**validated_data)
        return instance


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
        validated_data['creater'] = self.context['request'].user
        instance = Space.objects.create(**validated_data)
        return instance
        

class PrivateSpaceSerializer(serializers.ModelSerializer):
    creater = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    users = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='user-detail'
    )
    isPrivate = serializers.BooleanField(default=True , read_only=True)
    invite_code  = serializers.UUIDField(default=uuid.uuid4 , read_only=True)
    class Meta:
        model = Space
        fields = ['name' , 'creater' , 'users' , 'isPrivate' , 'invite_code']
    

    def create(self,validated_data):
        validated_data['creater'] = self.context['request'].user
        validated_data['isPrivate'] = True
        instance = Space.objects.create(**validated_data)
        return instance

class PrivateListSpaceSerializer(serializers.Serializer):
    creater = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    users = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='user-detail'
    )
    name = serializers.CharField(read_only=True)
    isPrivate = serializers.BooleanField(default=True , read_only=True)
    invite_code  = serializers.UUIDField(default=uuid.uuid4 , read_only=True)   


class SendRequestSerializer(serializers.ModelSerializer):
    space = serializers.HyperlinkedRelatedField(
        view_name='private-detail',
        read_only=True
    )
    from_user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    state = serializers.MultipleChoiceField(choices=REQUEST_STATE , default=REQUEST_STATE[0] , read_only=True)
    invite_code = serializers.CharField(max_length=56)
    class Meta:
        model = Request
        fields = ['space' , 'from_user' , 'state' , 'invite_code']

    def create(self,validated_data):
        validated_data['from_user'] = self.context['request'].user
        invite_code = uuid.UUID(validated_data['invite_code'])
        space = Space.objects.get(invite_code=invite_code)
        validated_data['space'] = space
        validated_data['state'] = REQUEST_STATE[0]
        instance = Request.objects.create(space=validated_data['space'] , from_user=validated_data['from_user'] , state=validated_data['state'])
        return instance

class RequestStateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Request
        fields = ['state']


class AcceptOrRejectRequestSerializer(serializers.ModelSerializer):

    state = serializers.ChoiceField(choices=[REQUEST_STATE[1] , REQUEST_STATE[2]])
    
    class Meta:
        model = Request
        fields = ['state']
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        space = instance.space
        print('here again')
        if space.creater != user:
            raise serializers.ValidationError('You are not the creater')
        state = validated_data['state']
        if state == 'accepted':
            print('here afain ')
            user = instance.from_user
            space.users.add(user)
        instance.state = state
        instance.save()
        print('saves')
        return instance
        