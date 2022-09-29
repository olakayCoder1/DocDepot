from django.shortcuts import render , redirect
from django.core.files.storage import FileSystemStorage
from .models import (
    Document, File, FileFolder, Folder ,TokenActivation , CustomUser
)
from .serializers import (
    FileUploadSerializer , FolderFileSerializer , FolderSerializer
)
from rest_framework import generics , status 
from rest_framework.response import Response
from rest_framework.decorators import APIView ,api_view
from django.conf import settings
import os

from client import serializers
# Create your views here.


def rename(url):
    image_path = str(url)
    image_path = str(settings.BASE_DIR) + str(url)
    print(image_path)
    print(settings.MEDIA_ROOT)
    return  image_path 


def home(request):
    
    for model in FileFolder.objects.all():
        # print(model.file) 
        name = str(model.file).split('/')[-1]
        # print(name)
        # print('**'*20)   
        # image_path = rename(model.file.url)
    return render(request, 'client/home.html')



def folder_file(request, folder_name):
    try:
        folder = Folder.objects.get(name=folder_name)
    except:
        return redirect('home')
    documents_in_folder = folder.files

    data = list(documents_in_folder.values('name'))
    # print(data)
    context = {
        'folder_name' : folder_name ,
        'files' : documents_in_folder,
        'data':data
    }
    return render(request, 'client/folder-file.html' , context )


class FileUploadApiView(generics.CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileUploadSerializer
     
class FolderFileApiView(generics.ListCreateAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

   
        


@api_view(['POST'])
def upload_file_api(request):
    serializer = FileUploadSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)