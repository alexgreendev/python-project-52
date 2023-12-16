from django.test import TestCase, Client
from django.urls import reverse_lazy
from task_manager.read_json import load_data
from django.core.exceptions import ObjectDoesNotExist
from task_manager.included_apps.users.models import User
from task_manager.included_apps.labels.models import Label


class LabelTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']
    test_label = load_data('test_label.json')

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.get(pk=1)
        self.client.force_login(self.user1)
        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)
        self.label3 = Label.objects.get(pk=3)
        self.labels = Label.objects.all()
        self.count = Label.objects.count()


class TestLabelCreateView(LabelTestCase):
    def test_create_label_view(self):
        response = self.client.get(reverse_lazy('label_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/create.html')

    def test_create_label_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('label_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_create_label(self):
        label_data = self.test_label['create']
        response = self.client.post(reverse_lazy('label_create'), data=label_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels_list'))
        self.assertEqual(Label.objects.count(), self.count + 1)


class TestStatusUpdateView(LabelTestCase):
    def test_update_label_view(self):
        response = self.client.get(reverse_lazy('label_update', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/update.html')

    def test_update_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('label_update', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_update_label(self):
        label_data = self.test_label['update']
        response = self.client.post(
            reverse_lazy('label_update', kwargs={'pk': 2}), data=label_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels_list'))
        self.assertEqual(Label.objects.count(), self.count)
        self.assertEqual(Label.objects.get(id=self.label2.id).name, label_data['name'])


class TestStatusDeleteView(LabelTestCase):
    def test_delete_label_view(self):
        response = self.client.get(reverse_lazy('label_delete', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/delete.html')

    def test_delete_label(self):
        response = self.client.post(reverse_lazy('label_delete', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels_list'))
        self.assertEqual(Label.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(id=self.label3.id)

    def test_delete_label_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse_lazy('label_delete', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertEqual(Label.objects.count(), self.count)
