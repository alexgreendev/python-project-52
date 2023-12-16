from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import StatusForm
from .models import Status
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import AuthenticateMixin, DeleteProtectionMixin


class StatusesView(ListView):
    template_name = 'statuses/statuses_list.html'
    model = Status
    context_object_name = 'statuses'


class StatusCreateView(AuthenticateMixin, SuccessMessageMixin, CreateView):
    template_name = 'statuses/create.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status successfully created')


class StatusUpdateView(AuthenticateMixin, SuccessMessageMixin, UpdateView):
    template_name = 'statuses/update.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status successfully updated')


class StatusDeleteView(AuthenticateMixin, DeleteProtectionMixin,
                       SuccessMessageMixin, DeleteView):
    template_name = 'statuses/delete.html'
    model = Status
    success_url = reverse_lazy('statuses_list')
    success_message = _('Status successfully deleted')
    rejection_message = _('Unable to delete status because it is in use')
    rejection_url = reverse_lazy('statuses_list')
