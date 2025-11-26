from django.urls import path
from .views import (
    TaskListCreateView,
    TaskRetrieveUpdateDeleteView,
    analyze_tasks_view,
    suggest_tasks_view
)

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('<int:pk>/', TaskRetrieveUpdateDeleteView.as_view(), name='task-edit-delete'),
    path('analyze/', analyze_tasks_view, name='analyze'),
    path('suggest/', suggest_tasks_view, name='suggest'),
]
