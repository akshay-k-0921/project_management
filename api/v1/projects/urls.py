from django.urls import re_path
from .views import AssigneeListCreateView, MilestoneListCreateView, MilestoneRetrieveUpdateDestroyView, ProjectListCreateView, ProjectRetrieveUpdateDestroyView, TaskListCreateView, TaskRetrieveUpdateDestroyView, AssignTaskView


app_name = 'api_v1_projects'

urlpatterns = [
    #projects
    re_path(r'^projects/$', ProjectListCreateView.as_view(), name='project-list-create'),
    re_path(r'^projects/(?P<pk>.*)/$', ProjectRetrieveUpdateDestroyView.as_view(), name='project-detail'),

    #tasks
    re_path(r'^tasks/$', TaskListCreateView.as_view(), name='task-list-create'),
    re_path(r'^tasks/(?P<pk>.*)/$', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
    re_path(r'^assignee-list/$', AssigneeListCreateView.as_view(), name='task-assignee-list'),
    re_path(r'^task-assign/(?P<pk>.*)/$', AssignTaskView.as_view(), name='task-assign'),

    #milestones
    re_path(r'^milestones/$', MilestoneListCreateView.as_view(), name='milestone-list-create'),
    re_path(r'^milestones/(?P<pk>.*)/$', MilestoneRetrieveUpdateDestroyView.as_view(), name='milestone-detail'),
]
