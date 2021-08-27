from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest
from django.test import TestCase
from rest_framework.compat import View
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer

from kf.permissions import CustomActionPermissions
from kf.viewsets import MultipleSerializersViewSet


class CustomActionPermissionsTests(TestCase):
    def create_user(self):
        user = User()
        user.username = 'chewe'
        user.password = make_password('chewe')
        user.email = 'chewe@starwars.com'
        user.save()
        return user

    def create_permission_with_code(self, code):
        content_type = ContentType.objects.get_for_model(User)
        custom_permission = Permission.objects.create(codename=code, content_type=content_type)
        permission_to_check = '{0}.{1}'.format(custom_permission.content_type.app_label, custom_permission.codename)
        return custom_permission, permission_to_check

    def get_permission_code_and_user_with_permission(self, code):
        custom_permission, permission_to_check = self.create_permission_with_code(code)
        user = self.create_user()
        user.user_permissions.add(custom_permission)
        return permission_to_check, user

    def get_permission_code_and_user_without_permission(self, code):
        custom_permission, permission_to_check = self.create_permission_with_code(code)
        user = self.create_user()
        return permission_to_check, user

    def get_request_and_view_with_action(self, action):
        request = Request(HttpRequest())
        view = View()
        view.action = action
        return request, view

    def test_no_permissions_set(self):
        request, view = self.get_request_and_view_with_action('list')
        permission = CustomActionPermissions()
        self.assertEqual(permission.has_permission(request, view), True)

    def test_has_object_permission_true(self):
        request, view = self.get_request_and_view_with_action('list')
        permission = CustomActionPermissions()
        self.assertEqual(permission.has_object_permission(request, view, None), True)

    def test_has_list_permission_set_and_user_too(self):
        permission_to_check, user = self.get_permission_code_and_user_with_permission('can_list')
        request, view = self.get_request_and_view_with_action('list')
        request.user = user

        permission = CustomActionPermissions()
        permission.list_permission = permission_to_check
        permission.retrieve_permission = 'retrieve'
        permission.create_permission = 'create'
        permission.update_permission = 'update'
        permission.destroy_permission = 'destroy'

        self.assertEqual(permission.has_permission(request, view), True)

    def test_has_retrieve_permission_set_and_user_too(self):
        permission_to_check, user = self.get_permission_code_and_user_with_permission('can_retrieve')
        request, view = self.get_request_and_view_with_action('retrieve')
        request.user = user

        permission = CustomActionPermissions()
        permission.list_permission = 'list'
        permission.retrieve_permission = permission_to_check
        permission.create_permission = 'create'
        permission.update_permission = 'update'
        permission.destroy_permission = 'destroy'

        self.assertEqual(permission.has_permission(request, view), True)

    def test_has_create_permission_set_and_user_too(self):
        permission_to_check, user = self.get_permission_code_and_user_with_permission('can_create')
        request, view = self.get_request_and_view_with_action('create')
        request.user = user

        permission = CustomActionPermissions()
        permission.list_permission = 'list'
        permission.retrieve_permission = 'retrieve'
        permission.create_permission = permission_to_check
        permission.update_permission = 'update'
        permission.destroy_permission = 'destroy'

        self.assertEqual(permission.has_permission(request, view), True)

    def test_has_update_permission_set_and_user_too(self):
        permission_to_check, user = self.get_permission_code_and_user_with_permission('can_update')
        request, view = self.get_request_and_view_with_action('update')
        request.user = user

        permission = CustomActionPermissions()
        permission.list_permission = 'list'
        permission.retrieve_permission = 'retrieve'
        permission.create_permission = 'create'
        permission.update_permission = permission_to_check
        permission.destroy_permission = 'destroy'

        self.assertEqual(permission.has_permission(request, view), True)

    def test_has_destroy_permission_set_and_user_too(self):
        permission_to_check, user = self.get_permission_code_and_user_with_permission('can_destroy')
        request, view = self.get_request_and_view_with_action('destroy')
        request.user = user

        permission = CustomActionPermissions()
        permission.list_permission = 'list'
        permission.retrieve_permission = 'retrieve'
        permission.create_permission = 'create'
        permission.update_permission = 'destroy'
        permission.destroy_permission = permission_to_check

        self.assertEqual(permission.has_permission(request, view), True)

    def test_has_list_permission_set_and_user_not(self):
        permission_to_check, user = self.get_permission_code_and_user_without_permission('can_list')
        request, view = self.get_request_and_view_with_action('list')
        request.user = user

        permission = CustomActionPermissions()
        permission.list_permission = permission_to_check
        permission.retrieve_permission = 'retrieve'
        permission.create_permission = 'create'
        permission.update_permission = 'update'
        permission.destroy_permission = 'destroy'
        self.assertEqual(permission.has_permission(request, view), False)

    def test_has_retrieve_permission_set_and_user_not(self):
        permission_to_check, user = self.get_permission_code_and_user_without_permission('can_retrieve')
        request, view = self.get_request_and_view_with_action('retrieve')
        request.user = user

        permission = CustomActionPermissions()
        permission.list_permission = 'list'
        permission.retrieve_permission = permission_to_check
        permission.create_permission = 'create'
        permission.update_permission = 'update'
        permission.destroy_permission = 'destroy'

        self.assertEqual(permission.has_permission(request, view), False)

    def test_has_create_permission_set_and_user_not(self):
        permission_to_check, user = self.get_permission_code_and_user_without_permission('can_create')
        request, view = self.get_request_and_view_with_action('create')
        request.user = user

        permission = CustomActionPermissions()
        permission.list_permission = 'list'
        permission.retrieve_permission = 'retrieve'
        permission.create_permission = permission_to_check
        permission.update_permission = 'update'
        permission.destroy_permission = 'destroy'

        self.assertEqual(permission.has_permission(request, view), False)

    def test_has_update_permission_set_and_user_not(self):
        permission_to_check, user = self.get_permission_code_and_user_without_permission('can_update')
        request, view = self.get_request_and_view_with_action('update')
        request.user = user

        permission = CustomActionPermissions()
        permission.list_permission = 'list'
        permission.retrieve_permission = 'retrieve'
        permission.create_permission = 'create'
        permission.update_permission = permission_to_check
        permission.destroy_permission = 'destroy'

        self.assertEqual(permission.has_permission(request, view), False)

    def test_has_destroy_permission_set_and_user_not(self):
        permission_to_check, user = self.get_permission_code_and_user_without_permission('can_destroy')
        request, view = self.get_request_and_view_with_action('destroy')
        request.user = user

        permission = CustomActionPermissions()
        permission.list_permission = 'list'
        permission.retrieve_permission = 'retrieve'
        permission.create_permission = 'create'
        permission.update_permission = 'destroy'
        permission.destroy_permission = permission_to_check

        self.assertEqual(permission.has_permission(request, view), False)


class MultipleSerializerViewSetTests(TestCase):
    class DummySerializer(BaseSerializer):
        pass

    class ListSerializer(BaseSerializer):
        pass

    class RetrieveSerializer(BaseSerializer):
        pass

    class CreateSerializer(BaseSerializer):
        pass

    class UpdateSerializer(BaseSerializer):
        pass

    class DestroySerializer(BaseSerializer):
        pass

    def get_view_with_custom_serializers_for_action(self, action):
        view = MultipleSerializersViewSet()
        view.serializer_class = self.DummySerializer
        view.list_serializer_class = self.ListSerializer
        view.retrieve_serializer_class = self.RetrieveSerializer
        view.create_serializer_class = self.CreateSerializer
        view.update_serializer_class = self.UpdateSerializer
        view.destroy_serializer_class = self.DestroySerializer
        view.action = action
        return view

    def test_no_custom_serializers_set(self):
        view = MultipleSerializersViewSet()
        view.serializer_class = self.DummySerializer
        view.action = 'list'
        self.assertEqual(view.get_serializer_class(), self.DummySerializer)
        view.action = 'retrieve'
        self.assertEqual(view.get_serializer_class(), self.DummySerializer)
        view.action = 'create'
        self.assertEqual(view.get_serializer_class(), self.DummySerializer)
        view.action = 'update'
        self.assertEqual(view.get_serializer_class(), self.DummySerializer)
        view.action = 'destroy'
        self.assertEqual(view.get_serializer_class(), self.DummySerializer)

    def test_custom_list_serializer_set(self):
        view = self.get_view_with_custom_serializers_for_action('list')
        self.assertEqual(view.get_serializer_class(), self.ListSerializer)

    def test_custom_retrieve_serializer_set(self):
        view = self.get_view_with_custom_serializers_for_action('retrieve')
        self.assertEqual(view.get_serializer_class(), self.RetrieveSerializer)

    def test_custom_create_serializer_set(self):
        view = self.get_view_with_custom_serializers_for_action('create')
        self.assertEqual(view.get_serializer_class(), self.CreateSerializer)

    def test_custom_update_serializer_set(self):
        view = self.get_view_with_custom_serializers_for_action('update')
        self.assertEqual(view.get_serializer_class(), self.UpdateSerializer)

    def test_custom_destroy_serializer_set(self):
        view = self.get_view_with_custom_serializers_for_action('destroy')
        self.assertEqual(view.get_serializer_class(), self.DestroySerializer)
