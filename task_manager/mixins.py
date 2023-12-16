from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.translation import gettext
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db.models import ProtectedError


class AuthenticateMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext('You are not logged in, please log in.'))
            return redirect(reverse_lazy('login'))

        return super().dispatch(request, *args, **kwargs)


class PermissionMixin(UserPassesTestMixin):
    permission_message = ''
    permission_url = ''

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class DeleteProtectionMixin:
    rejection_message = ''
    rejection_url = ''

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.rejection_message)
            return redirect(self.rejection_url)


class AuthorPermissionMixin(UserPassesTestMixin):
    author_permission_message = ''
    author_permission_url = ''

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.author_permission_message)
        return redirect(self.author_permission_url)
