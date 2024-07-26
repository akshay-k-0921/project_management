from django.urls import re_path
from .views import ProjectListCreateView, ProjectRetrieveUpdateDestroyView


app_name = 'api_v1_projects'

urlpatterns = [
    re_path(r'^projects/$', ProjectListCreateView.as_view(), name='project-list-create'),
    re_path(r'^projects/(?P<pk>.*)/$', ProjectRetrieveUpdateDestroyView.as_view(), name='project-detail'),
]
