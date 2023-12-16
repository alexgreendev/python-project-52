from django import forms
from django_filters import BooleanFilter, FilterSet, ModelChoiceFilter
from django.utils.translation import gettext_lazy as _
from .models import Task
from task_manager.included_apps.labels.models import Label


class TaskFilter(FilterSet):
    own_tasks = BooleanFilter(
        field_name='author',
        label=_('Only own tasks'),
        method='filtered_own_tasks',
        widget=forms.CheckboxInput,
    )

    labels = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=_('Label')
    )

    class Meta:
        model = Task
        fields = ['status', 'executor']

    def filtered_own_tasks(self, queryset, name, value):
        if value:
            user = self.request.user.pk
            return queryset.filter(author=user)
        return queryset
