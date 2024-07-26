from django.urls import re_path
from .views import AssigneeListCreateView, ProjectListCreateView, ProjectRetrieveUpdateDestroyView, TaskListCreateView, TaskRetrieveUpdateDestroyView


app_name = 'api_v1_projects'

urlpatterns = [
    #projects
    re_path(r'^projects/$', ProjectListCreateView.as_view(), name='project-list-create'),
    re_path(r'^projects/(?P<pk>.*)/$', ProjectRetrieveUpdateDestroyView.as_view(), name='project-detail'),

    #tasks
    re_path(r'^tasks/$', TaskListCreateView.as_view(), name='task-list-create'),
    re_path(r'^tasks/(?P<pk>.*)/$', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    re_path(r'^assignee-list/$', AssigneeListCreateView.as_view(), name='task-assignee-list'),
]
