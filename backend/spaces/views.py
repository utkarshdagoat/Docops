from rest_framework import generics , views , viewsets , permissions , authentication , mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status




from .models.space import Space
from .models.request import Request
from .serializers.space import PublicSpaceSerializer  , PrivateSpaceSerializer
from .serializers.request import SendRequestSerializer , AcceptOrRejectRequestSerializer , RequestStateSerializer
from .permission import IsInSpace , IsTheCreater
from myauth.models import User


class PublicSpaceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication ,]
    queryset = Space.objects.filter(isPrivate=False)
    serializer_class = PublicSpaceSerializer

    @action(methods=['GET'],detail=False)
    def add_user(self , request , *args , **kwargs):
        invite_code = request.GET.get('code' , '')
        space = Space.objects.get(invite_code=invite_code)
        assert (space.isPrivate == False)
        space.users.add(request.user)
        return Response("User Added SuccessFully")

class PrivateSpaceViewSet(viewsets.ModelViewSet):
    permission_classes = [ permissions.IsAuthenticated, IsInSpace]
    authentication_classes = [authentication.SessionAuthentication,]
    queryset = Space.objects.filter(isPrivate=True)
    serializer_class = PrivateSpaceSerializer

    def get_queryset(self):
        queryset = User.objects.get(pk=self.request.user.id).space_set.filter(isPrivate=True) | Space.objects.filter(creater=self.request.user , isPrivate=True)
        return queryset

class RequestAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication]
    queryset = Request.objects.all()
    serializer_class = SendRequestSerializer


    
class RequestStateAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Request.objects.all()
    serializer_class = RequestStateSerializer


    
class AcceptOrRejectRequestAPIView(generics.GenericAPIView, mixins.UpdateModelMixin):
    permission_classes = [permissions.IsAuthenticated , IsTheCreater]
    authentication_classes = [authentication.SessionAuthentication]
    queryset = Request.objects.all()
    serializer_class = AcceptOrRejectRequestSerializer

    def put(self,request,*args,**kwargs):
        return self.update(request=request , *args , **kwargs)



