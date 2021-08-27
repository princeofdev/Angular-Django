from push_notifications.api.rest_framework import GCMDeviceAuthorizedViewSet


class FCMDeviceAuthorizedViewSet(GCMDeviceAuthorizedViewSet):

    def perform_create(self, serializer):
        if self.request.user.is_authenticated():
            serializer.save(user=self.request.user, cloud_message_type="FCM")
        return super(FCMDeviceAuthorizedViewSet, self).perform_create(serializer)