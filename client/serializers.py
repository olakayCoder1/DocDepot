from rest_framework import serializers
from .models import (
    File, CustomUser,
    FileFolder,Folder
)



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email']

class FileUploadSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        user = CustomUser.objects.get(id=user_id)
        file = validated_data.get("file")        
        return File.objects.create(user_id=user_id, file=file)

    user = CustomUserSerializer(read_only=True ) 
        
    class Meta:
        model = File
        # fields = '__all__'
        fields = ['user' , 'file', 'date_uploaded']
        extra_kwargs = {
            'date_uploaded':{'read_only': True},
        }

    

class FolderFileSerializer(serializers.ModelSerializer): 
    class Meta:
        model = FileFolder
        fields = ['name', 'file', 'date_uploaded']
        extra_kwargs = {
            'date_uploaded':{'read_only': True},
        }


class FolderSerializer(serializers.ModelSerializer): 
    files = FolderFileSerializer(read_only=True, many=True)
    class Meta:
        model = Folder
        fields = [ 'name', 'date_created', 'files']
        extra_kwargs = {
            'date_created':{'read_only': True},
        }
