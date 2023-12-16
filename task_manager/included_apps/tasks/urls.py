from django.urls import path
from .views import TasksView, TaskView, TaskCreateView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('', TasksView.as_view(), name='tasks_list'),
    path('<int:pk>/', TaskView.as_view(), name='show_one_task'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
