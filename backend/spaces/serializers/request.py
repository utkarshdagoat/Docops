from spaces.models.request import Request
from constants.constants import REQUEST_STATE

from rest_framework import serializers

class SendRequestSerializer(serializers.ModelSerializer):
    space = serializers.HyperlinkedRelatedField(
        view_name='private-detail',
        read_only=True
    )
    from_user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    state = serializers.ChoiceField(choices=REQUEST_STATE , default=REQUEST_STATE[0] , read_only=True)
    invite_code = serializers.CharField(max_length=56)
    class Meta:
        model = Request
        fields = ['space' , 'from_user' , 'state' , 'invite_code']

    def create(self,validated_data):
        return  RequestInstanceForSendingRequest(context=self.context , validated_data=validated_data)

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
        return  updateRequestInstance(context=self.context , instance=instance , validated_data=validated_data)
        