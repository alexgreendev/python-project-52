from django.test import TestCase, Client
from django.urls import reverse_lazy
from task_manager.read_json import load_data
from django.core.exceptions import ObjectDoesNotExist
from task_manager.included_apps.users.models import User
from task_manager.included_apps.statuses.models import Status
from task_manager.included_apps.tasks.models import Task


class TaskTestCase(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json']
    test_task = load_data('test_task.json')

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.client.force_login(self.user1)
        self.status1 = Status.objects.get(pk=1)
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.task3 = Task.objects.get(pk=3)
        self.tasks = Task.objects.all()
        self.count = Task.objects.count()


class TestTaskCreateView(TaskTestCase):
    def test_create_task_view(self):
        response = self.client.get(reverse_lazy('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/create.html')

    def test_create_task_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse_lazy('task_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_create_task(self):
        task_data = self.test_task['create']
        response = self.client.post(reverse_lazy('task_create'), data=task_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks_list'))
        self.assertEqual(Task.objects.count(), self.count + 1)


class TestTaskUpdateView(TaskTestCase):
    def test_update_task_view(self):
        response = self.client.get(reverse_lazy('task_update', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/update.html')

    def test_update_task(self):
        task_data = self.test_task['update']
        response = self.client.post(
            reverse_lazy('task_update', kwargs={'pk': 2}), data=task_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks_list'))
        self.assertEqual(Task.objects.count(), self.count)
        self.assertEqual(Task.objects.get(id=self.task2.id).name, task_data['name'])


class TestTaskDeleteView(TaskTestCase):
    def test_delete_task_view(self):
        response = self.client.get(reverse_lazy('task_delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/delete.html')

    def test_delete_task(self):
        response = self.client.post(reverse_lazy('task_delete', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks_list'))
        self.assertEqual(Task.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=self.task2.id)

    def test_delete_task_not_author(self):
        self.client.logout()
        response = self.client.post(reverse_lazy('status_delete', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertEqual(Task.objects.count(), self.count)
