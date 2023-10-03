import environ
import requests
import os
import traceback


from django.shortcuts import redirect
from django.contrib.auth import login , logout


from rest_framework import generics , views , mixins
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication , TokenAuthentication
# Create your views here.
from .models import User
from spaces.models.space import Space


from.services import UserFromRequest , headerFromCode
from .serializers import UserSerializers , UserSpacesSerializers
from constants.constants import AUTH_CODE_URL , BACKEND_URL_REDIRECT ,USER_INFO_URL , CLIENT_ID


class TokenApiView(views.APIView):
    permission_classes=[AllowAny,]
    authentication_classes=[SessionAuthentication,]
    def get(self , request , *args , **kwargs):
        REDIRECT_URL=f"{AUTH_CODE_URL}?client_id={CLIENT_ID}&redirect_uri={BACKEND_URL_REDIRECT}"
        return redirect(REDIRECT_URL)


class TokenRedirectAPIView(views.APIView):
    permission_classes=[AllowAny,]
    authentication_classes=[SessionAuthentication,]
    def get(self, request , *args , **kwargs):
        code = request.GET.get('code' , '') 
        _header = headerFromCode(code)
        # checks if there is error from code
        try:
            _header["error"]
            return Response(data=_header['res'],status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except  KeyError:
            pass
        user_data = requests.get(USER_INFO_URL , headers=_header).json()
        # user_data contains a dict with key detail on error
        try:
            if user_data['detail']:
                return Response(data=user_data , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            pass
        res = UserFromRequest(user_data)
        # response is empty if unable to make user
        if len(res) == 0 :
            err = {
                "message":"Unable to access user properties"
            }
            return Response(data=err , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # extract user and isMember from response
        user , isMember = res
        """
        if not isMember:
            err ={
            "message":"Application is IMG only"
            }
            return Response(data=err , status=status.HTTP_401_UNAUTHORIZED)
        """
        if user is None:
            err = {
                "meassage":"Unable to create user"
            }
            return Response(data=err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            login(request , user=user)
            success = {
                "message":"User SuccessFully logged in"
            }
            return Response(data=success ,status=status.HTTP_200_OK)
        except:
            err = {
                "message":"Unable to Login user"
            }
            traceback.print_exc()
            return Response(data=err , status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(views.APIView):
    permission_classes = [IsAuthenticated,]
    authentication_classes = [SessionAuthentication,]
    def get(self,request , *args , **kwargs):
        logout(request)
        success = {
            "message":"Logged out successfully"
        }
        return Response(data=success , status=status.HTTP_204_NO_CONTENT)
        


class UserAPIView(generics.GenericAPIView ,mixins.RetrieveModelMixin):

    queryset = User.objects.all()
    serializer_class = UserSerializers 
    permission_classes = [IsAuthenticated,]
    authentication_classes = [SessionAuthentication]

    def get(self, request , *args , **kwargs):
        return self.retrieve(request=request , *args , **kwargs)

class UserSpaceAPIView(generics.GenericAPIView , mixins.ListModelMixin):
    serializer_class = UserSpacesSerializers
    permission_classes = [IsAuthenticated,]
    authentication_classes = [SessionAuthentication,]
    
    def get_queryset(self):
        user_id = self.request.user.id
        user = User.objects.get(pk=user_id)
        return User.objects.get(pk=user_id).space_set.all() | Space.objects.filter(creater=user)

    def get(self , request , *args , **kwargs):
        return self.list(request=request , *args , **kwargs)