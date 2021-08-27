from rest_framework.generics import CreateAPIView

from files.serializers import FileSerializer


class UploadFileAPIView(CreateAPIView):
    """
    Endpoint to upload a file in Base64 format. Send the base64 data in the "file" field and use "form-data" encoding.
    """
    serializer_class = FileSerializer
    permission_classes = ()

