from django.conf.urls import url

from files.views import UploadFileAPIView

urlpatterns = [
    url(r'^1.0/upload/$', UploadFileAPIView.as_view(), name='upload_file'),
]