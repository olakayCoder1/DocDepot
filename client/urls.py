from xml.etree.ElementInclude import include
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home , name='home'), 
    path('document', views.FileUploadApiView.as_view(), name='upload_document'),
    path('folder/files/documents', views.FolderFileApiView.as_view(), name='folder_document'),
    path('folder/<str:folder_name>', views.folder_file, name='folder_document'),
]