from django.urls import path, include, re_path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^api/v1/', include(

        [
            re_path(r'^users/', include('api.v1.users.urls', namespace='api_v1_users')),
            re_path(r'^projects/', include('api.v1.projects.urls', namespace='api_v1_projects')),
        ]
     )),
]
