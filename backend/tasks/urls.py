from django.urls import path
from .views import analyze_tasks_view, suggest_tasks_view

urlpatterns = [
    path('analyze/', analyze_tasks_view),
    path('suggest/', suggest_tasks_view),
]
