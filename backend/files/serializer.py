from rest_framework import serializers
from files.models.file import File , FileText

from spaces.models.space import Space
from myauth.serializers.serializers import UserSerializers

import uuid


class FileSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    space = serializers.CharField(max_length=32, )
    invite_code = serializers.UUIDField(read_only=True )
    creater = UserSerializers(read_only=True)
    class Meta:
        model = File
        fields = ['cover' ,'creater', 'space' , 'isPrivate' , 'invite_code' , 'heading']

    def create(self,validated_data):
        name = validated_data['space']
        space = Space.objects.get(name=name)
        validated_data['space'] = space
        validated_data['createdBy'] = self.context['request'].user
        validated_data['inviteCode'] = uuid.uuid4()
        instance = File.objects.create(**validated_data)
        return instance




class FileRetriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['cover' , 'heading' ]



class HeadingFileSerializer(serializers.Serializer):
    heading = serializers.CharField(max_length=200)


    def update(self,instance,validated_data):
        heading = validated_data['heading']
        instance.heading = heading
        instance.save()
        return instance


class CoverFileSerializer(serializers.Serializer):
    cover = serializers.ImageField()

    def update(self,instance,validated_data):
        cover = validated_data['cover']
        instance.cover = cover
        instance.save()
        return instance



class FileSpaceShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['heading' , 'docId']

class FileTextSerializer(serializers.ModelSerializer):
    file = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model=FileText
        fields = ['file' , 'text']
    
    def update(self , instance , validated_data):
        instance.text = validated_data['text']
        instance.save()
        return instance