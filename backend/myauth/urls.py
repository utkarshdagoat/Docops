from django.urls import path
from . import  views



urlpatterns = [
        path('token/' , views.TokenApiView.as_view()),
        path('token/redirect/' , views.TokenRedirectAPIView.as_view()),
        path('logout/' , views.LogoutAPIView.as_view()),
        path('user/<int:pk>' , views.UserAPIView.as_view() , name="user-detail"),
        path('user/spaces' , views.UserSpaceAPIView.as_view())
    ]
