# management/views.py
from django.core.management import call_command
from django.http import JsonResponse

def run_check_deadlines(request):
    try:
        # Run the custom management command 'check_deadlines'
        call_command('checkdeadlines')
        return JsonResponse({"status": "success", "message": "Deadline check completed."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from core.models import Group, GroupUser, User
from django.core.management import call_command
from unittest.mock import patch

class UserTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('user-list')

    def test_add_user(self):
        data = {'username': 'newuser', 'password': 'newpass'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_validation(self):
        data = {'username': '', 'password': 'newpass'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class GroupTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.group = Group.objects.create(name='Test Group')
        GroupUser.objects.create(user=self.user, group=self.group)
        self.url = reverse('get_groups')

    def test_authenticated_user_with_groups(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['groups']), 1)

    def test_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_group_data_structure(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.url)
        group_data = response.data['groups'][0]
        self.assertIn('id', group_data)
        self.assertIn('name', group_data)
        self.assertIn('image', group_data)
        self.assertIn('expiringSoonCount', group_data)
        self.assertIn('unreadMessagesCount', group_data)

    def test_nonexistent_functionality(self):
        response = self.client.get('/nonexistent_endpoint/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ManagementCommandTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('run_check_deadlines')

    @patch('django.core.management.call_command')
    def test_run_check_deadlines(self, mock_call_command):
        mock_call_command.return_value = None
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"status": "success", "message": "Deadline check completed."})
        mock_call_command.assert_called_once_with('checkdeadlines')