from rest_framework import serializers
from files.models.file import File


class FileSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    space = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = File
        fields = ['heading' , 'cover' , 'space']
