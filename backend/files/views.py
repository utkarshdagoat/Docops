from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
# Create your views here
from docops.authentication import CsrfExemptSessionAuthentication



class TestView(views.APIView):
    permission_classes = [IsAuthenticated ,]
    authentication_classes = [CsrfExemptSessionAuthentication,]

    def post(self , request , *args , **kwargs):
        print(request.data)
        return Response('sup')



        