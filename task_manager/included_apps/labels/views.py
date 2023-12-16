from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import LabelForm
from .models import Label
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import AuthenticateMixin, DeleteProtectionMixin


class LabelsView(ListView):
    template_name = 'labels/labels_list.html'
    model = Label
    context_object_name = 'labels'


class LabelCreateView(AuthenticateMixin, SuccessMessageMixin, CreateView):
    template_name = 'labels/create.html'
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully created')


class LabelUpdateView(AuthenticateMixin, SuccessMessageMixin, UpdateView):
    template_name = 'labels/update.html'
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully updated')


class LabelDeleteView(AuthenticateMixin, DeleteProtectionMixin,
                      SuccessMessageMixin, DeleteView):
    template_name = 'labels/delete.html'
    model = Label
    success_url = reverse_lazy('labels_list')
    success_message = _('Label successfully deleted')
    rejection_message = _('Unable to delete label because it is in use')
    rejection_url = reverse_lazy('labels_list')
