import environ
import requests
import os
import traceback

from django.shortcuts import redirect
from django.contrib.auth import login , logout


from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

from docops.settings import BASE_DIR
from.services import UserFromRequest , headerFromCode
from .serializers import MessageSerializers

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


BACKEND_URL_REDIRECT=env("BACKEND_URL_REDIRECT")
AUTH_CODE_URL=env('AUTH_CODE_URL')
USER_INFO_URL=env('USER_INFO_URL')
CLIENT_ID=env('CLIENT_ID') 



class TokenApiView(views.APIView):
    permission_classes=[AllowAny,]
    def get(self , request , *args , **kwargs):
        print('entered')
        REDIRECT_URL=f"{AUTH_CODE_URL}?client_id={CLIENT_ID}&redirect_uri={BACKEND_URL_REDIRECT}"
        return redirect(REDIRECT_URL)


class TokenRedirectAPIView(views.APIView):
    permission_classes=[AllowAny,]
    def get(self, request , *args , **kwargs):

        code = request.GET.get('code' , '') 
        _header = headerFromCode(code)

        try:
            _header["error"]
            print(_header['res'])
            return Response(data=_header['res'],status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except  KeyError:
            pass


        user_data = requests.get(USER_INFO_URL , headers=_header).json()
        try:
            if user_data['detail']:
                return Response(data=user_data , status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            pass
        
        res = UserFromRequest(user_data)

        if len(res) == 0 :
            err = {
                "message":"Unable to access user properties"
            }
            return Response(data=err , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user , isMember = res
        print(isMember)
        print(user)

        if not isMember:
            err ={
            "message":"Application is IMG only"
            }
            return Response(data=err , status=status.HTTP_401_UNAUTHORIZED)

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

    def get(self,request , *args , **kwargs):
        logout(request)
        message = MessageSerializers(message="Logged out SuccessFully")
        return Response(message.data , status=status.HTTP_204_NO_CONTENT)
        








