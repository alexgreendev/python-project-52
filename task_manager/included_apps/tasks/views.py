from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import AuthenticateMixin, AuthorPermissionMixin
from .forms import TaskForm
from .models import Task
from task_manager.included_apps.users.models import User
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView
from .filters import TaskFilter


class TasksView(AuthenticateMixin, FilterView):
    template_name = 'tasks/tasks_list.html'
    model = Task
    filterset_class = TaskFilter
    context_object_name = 'tasks'


class TaskView(DetailView):
    template_name = 'tasks/show_one_task.html'
    model = Task
    context_object_name = 'task'


class TaskCreateView(AuthenticateMixin, SuccessMessageMixin, CreateView):
    template_name = 'tasks/create.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = User.objects.get(pk=user.pk)
        return super().form_valid(form)


class TaskUpdateView(AuthenticateMixin, SuccessMessageMixin, UpdateView):
    template_name = 'tasks/update.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task successfully updated')


class TaskDeleteView(AuthenticateMixin, AuthorPermissionMixin,
                     SuccessMessageMixin, DeleteView):
    template_name = 'tasks/delete.html'
    model = Task
    success_url = reverse_lazy('tasks_list')
    success_message = _('Task successfully deleted')
    author_permission_message = _('Only the author of the task can delete it')
    author_permission_url = reverse_lazy('tasks_list')
