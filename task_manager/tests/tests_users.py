from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from task_manager.read_json import load_data
from django.utils.translation import gettext_lazy
from django.core.exceptions import ObjectDoesNotExist


class UserTestCase(TestCase):
    fixtures = ['users.json']
    test_user = load_data('test_user.json')

    def setUp(self):
        self.client = Client()
        self.user1 = get_user_model().objects.get(pk=1)
        self.user2 = get_user_model().objects.get(pk=2)
        self.user3 = get_user_model().objects.get(pk=3)
        self.users = get_user_model().objects.all()
        self.count = get_user_model().objects.count()


class TestUserCreateView(UserTestCase):
    def test_create_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse_lazy('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/create.html')

    def test_create_valid_user(self):
        test_user_data = self.test_user['create']['valid'].copy()
        response = self.client.post(reverse_lazy('user_create'), data=test_user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertEqual(get_user_model().objects.count(), self.count + 1)
        self.assertEqual(
            get_user_model().objects.last().username,
            test_user_data['username']
        )

    def test_create_invalid_username(self):
        test_user_data = self.test_user['create']['invalid']
        response = self.client.post(reverse_lazy('user_create'), data=test_user_data)
        errors = response.context['form'].errors
        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_user_model().objects.count(), self.count)
        self.assertIn('username', errors)
        self.assertEqual(
            [gettext_lazy('Enter a valid username. This value may contain only '
                          'letters, numbers, and @/./+/-/_ characters.')],
            errors['username']
        )

    def test_create_missing_password(self):
        test_user_data = self.test_user['create']['password_missing']
        response = self.client.post(reverse_lazy('user_create'), data=test_user_data)
        errors = response.context['form'].errors
        error_help = gettext_lazy('This field is required.')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_user_model().objects.count(), self.count)
        self.assertIn('password1', errors)
        self.assertEqual([error_help], errors['password1'])
        self.assertIn('password2', errors)
        self.assertEqual([error_help], errors['password2'])


class TestUserUpdateView(UserTestCase):
    def test_update_view(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse_lazy('user_update', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/update.html')

    def test_update_user(self):
        self.client.force_login(self.user2)
        test_user_data = self.test_user['update'].copy()
        response = self.client.post(
            reverse_lazy('user_update', kwargs={'pk': 2}),
            data=test_user_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users_list'))
        self.assertEqual(
            get_user_model().objects.get(id=self.user2.id).first_name,
            test_user_data['first_name']
        )


class TestUserDeleteView(UserTestCase):
    def test_delete_view_with_authoriz(self):
        self.client.force_login(self.user3)
        response = self.client.get(reverse_lazy('user_delete', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/delete.html')

    def test_delete_view_without_authoriz(self):
        response = self.client.get(reverse_lazy('user_delete', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_delete_self(self):
        self.client.force_login(self.user3)
        response = self.client.post(
            reverse_lazy('user_delete', kwargs={'pk': 3})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users_list'))
        self.assertEqual(get_user_model().objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            get_user_model().objects.get(id=self.user3.id)
