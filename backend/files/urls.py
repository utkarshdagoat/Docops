from django.urls import path
from . import  views


urlpatterns = [
        path('' , views.FileAPIView.as_view()),
        path('heading/<str:doc_id>' , views.UpdataHeadingAPIView.as_view()),
        path('cover/<str:doc_id>' , views.UpdateCoverAPIView.as_view()),
        path('get/<str:doc_id>' , views.RetrieveFileAPIView.as_view()),
        path('space/<int:space_id>' , views.ListFilesSpaceAPIView.as_view()),
        path('doc/<str:doc_id>' , views.UpdateFileAPIView.as_view()),
        path('text/<str:doc_id>' , views.FileTextAPIView.as_view())
]