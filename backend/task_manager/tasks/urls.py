from django.urls import path
from .views import TaskListCreateView, TaskDetailView

urlpatterns = [
    path("create/", TaskListCreateView.as_view(),),
    path("tasks/<int:id>/", TaskDetailView.as_view(),),
]
