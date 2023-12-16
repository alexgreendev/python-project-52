from django.test import TestCase, Client
from django.urls import reverse_lazy
from task_manager.read_json import load_data
from django.core.exceptions import ObjectDoesNotExist
from task_manager.included_apps.statuses.models import Status
from task_manager.included_apps.users.models import User


class StatusTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json']
    test_status = load_data('test_status.json')

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.get(pk=1)
        self.client.force_login(self.user1)
        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
        self.status3 = Status.objects.get(pk=3)
        self.statuses = Status.objects.all()
        self.count = Status.objects.count()


class TestStatusCreateView(StatusTestCase):
    def test_create_status_view(self):
        response = self.client.get(reverse_lazy('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/create.html')

    def test_create_status_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('status_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_create_status(self):
        status_data = self.test_status['create']
        response = self.client.post(reverse_lazy('status_create'), data=status_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('statuses_list'))
        self.assertEqual(Status.objects.count(), self.count + 1)


class TestStatusUpdateView(StatusTestCase):
    def test_update_status_view(self):
        response = self.client.get(reverse_lazy('status_update', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/update.html')

    def test_update_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('status_update', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_update_status(self):
        status_data = self.test_status['update']
        response = self.client.post(
            reverse_lazy('status_update', kwargs={'pk': 2}), data=status_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('statuses_list'))
        self.assertEqual(Status.objects.count(), self.count)
        self.assertEqual(Status.objects.get(id=self.status2.id).name, status_data['name'])


class TestStatusDeleteView(StatusTestCase):
    def test_delete_status_view(self):
        response = self.client.get(reverse_lazy('status_delete', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/delete.html')

    def test_delete_status(self):
        response = self.client.post(reverse_lazy('status_delete', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('statuses_list'))
        self.assertEqual(Status.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(id=self.status3.id)

    def test_delete_status_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse_lazy('status_delete', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertEqual(Status.objects.count(), self.count)
