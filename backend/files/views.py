from django.shortcuts import render
from rest_framework import views , mixins,generics
from rest_framework.response import Response 
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication


# Create your views here
from docops.authentication import CsrfExemptSessionAuthentication
from files.models.file_store import FileDoc
from files.models.file import File
from .serializer import FileSerializer , HeadingFileSerializer , CoverFileSerializer , FileRetriveSerializer
from rest_framework import parsers
from files.parser import MultiPartJsonParser


class RetrieveFileAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CsrfExemptSessionAuthentication,]
    serializer_class = FileSerializer
    
    def get(self , request , *args , **kwargs):
        try:
            instance = File.objects.get(docId=self.kwargs['doc_id'])
            cover = instance.cover if(instance.cover) else None
            data = {
                "cover":cover,
                "heading":instance.heading
            }
            file  = FileDoc.objects.get(id=instance.docId)
            serializer = FileRetriveSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            res = {
                "meta":serializer.data,
                "doc":file.doc
            }
            return Response(res)
            return Response(serializer.errors)
        except File.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class FileAPIView(generics.GenericAPIView , mixins.ListModelMixin):
    permission_classes = [IsAuthenticated ,]
    authentication_classes = [CsrfExemptSessionAuthentication,]
    parser_classes=[parsers.JSONParser]
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get(self , request,*args,**kwargs):
        try:
            instance = File.objects.get(docId=self.kwargs['doc_id'])
            serailizer = FileSerializer(data=instance)
            if serailizer.is_valid():
                serailizer.save()
                return Response(serailizer.data)
            return Response(serailizer.errors)
        except File.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    def post(self , request , *args , **kwargs):
        serializer_data = {
            "space":request.data['space'],
            "isPrivate":False
        }
        serializer  = FileSerializer(data=serializer_data , context={'request':request})
        serializer.is_valid(raise_exception=True)
        file = serializer.save()
        fileStore = FileDoc(sqlRef=file.id)
        fileStore.save()
        file.docId = str(fileStore.id)
        docId = file.docId
        file.save()
        return Response(docId)




class UpdateFileAPIView(views.APIView):
    permission_classes = [IsAuthenticated ,]
    authentication_classes = [CsrfExemptSessionAuthentication,]
    parser_classes=[MultiPartJsonParser , parsers.JSONParser]

    def put (self,request,doId ,*args,**kwargs):
        docInstance = FileDoc.objects.get(id=docId)
        docInstance.doc = request.data['doc']
        docInstance.save()
        return Response("True")



class UpdataHeadingAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CsrfExemptSessionAuthentication]
    lookup_url_kwarg = 'doc_id'
    serializer_class = HeadingFileSerializer
    queryset = File.objects.all()

    def put(self , request ,  *args , **kwargs ):
        try:
            instance = File.objects.get(docId=self.kwargs['doc_id'])
            serailizer = HeadingFileSerializer(instance , data=request.data)
            if serailizer.is_valid():
                serailizer.save()
                return Response(serailizer.data)
            return Response(serailizer.errors)
        except File.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class UpdateCoverAPIView(generics.GenericAPIView , mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [CsrfExemptSessionAuthentication]
    lookup_url_kwarg = 'doc_id'
    serializer_class = CoverFileSerializer
    parser_classes = [parsers.MultiPartParser]
    queryset = File.objects.all()

    def put(self , request ,  *args , **kwargs ):
        try:
            instance = File.objects.get(docId=self.kwargs['doc_id'])
            serailizer = CoverFileSerializer(instance , data=request.data)
            if serailizer.is_valid():
                serailizer.save()
                return Response(serailizer.data)
            return Response(serailizer.errors)
        except File.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        