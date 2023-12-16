from django.test import TestCase, Client
from django.urls import reverse_lazy
from http import HTTPStatus


class TestPageCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_is_ok_page_home(self):
        response = self.client.get(reverse_lazy('home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_is_ok_page_login(self):
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_is_ok_page_register(self):
        response = self.client.get(reverse_lazy('user_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
