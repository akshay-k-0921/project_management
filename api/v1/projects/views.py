from rest_framework import generics, permissions,status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from django.core.cache import cache

from projects.tasks import send_email_notification
from projects.models import Milestone, Project, Task
from users.models import CustomUser
from .serializers import MilestoneSerializer, ProjectSerializer, TaskSerializer
from core.permissions import IsAdminOrReadOnly, IsManagerOrReadOnly
from api.v1.users.serializers import CustomUserSerializer



#-------------------------- Project Views Start --------------------------
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.active_objects.all().select_related('owner').prefetch_related('tasks', 'milestones')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]
    
    # project list 
    def list(self, request, *args, **kwargs):
        cache_key = 'project_list'
        # checking if the data is already cached
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)

        #caching the response data
        cache.set(cache_key, response.data, timeout=60*15)
        return response
    # create
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        cache.delete('project_list')

        response_data={
            "message": "Project created successfully",
            "data": serializer.data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    


class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.active_objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_update(self, serializer):
        serializer.save()
        # Invalidate cache after updating a project
        cache.delete('project_list')  
        response_data={
            "message": "Project updated successfully",
            "data": serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        #soft deleting the instance
        instance.is_deleted = True 
        instance.save()
        # deleting cache after deleting a project
        cache.delete('project_list')

        return Response('Project deleted successfully')
    
#-------------------------- Project Views End --------------------------


#--------------------------- Task Views Start --------------------------
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.active_objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        cache_key = 'task_list'
        # checking if the data is already cached
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)

        # caching the response data
        cache.set(cache_key, response.data, timeout=60*15)
        return response
    
    def perform_create(self, serializer):
        serializer.save()
        cache.delete('task_list')

        response_data={
            "message": "Task created successfully",
            "data": serializer.data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.active_objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_update(self, serializer):
        serializer.save()
        # Invalidate cache after updating a task
        cache.delete('task_list') 

        response_data={
            "message": "Task updated successfully",
            "data": serializer.data
        } 

        return Response(response_data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        #soft deleting the instance
        instance.is_deleted = True 
        instance.save()
        # deleting cache after deleting a task
        cache.delete('task_list')

        return Response('Task deleted successfully')


# assignee list for manager or admin to assign task
class AssigneeListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.filter(role='member')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        cache_key = 'assignee_list'
        # checking if the data is already cached
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)

        # caching the response data
        cache.set(cache_key, response.data, timeout=60*15)
        return response
    

class AssignTaskView(generics.UpdateAPIView):
    queryset = Task.active_objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_update(self, serializer):
        serializer.save()
        # Invalidate cache after updating a task
        cache.delete('task_list')

        return Response('Task assigned successfully')
#--------------------------- Task Views End --------------------------


#--------------------------- Milestone Views Start --------------------------
class MilestoneListCreateView(generics.ListCreateAPIView):
    queryset = Milestone.active_objects.all()
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        cache_key = 'milestone_list'
        # checking if the data is already cached
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)

        # caching the response data
        cache.set(cache_key, response.data, timeout=60*15)
        return response
    
    def perform_create(self, serializer):
        serializer.save()
        cache.delete('milestone_list')

        response_data={
            "message": "Milestone created successfully",
            "data": serializer.data
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    

class MilestoneRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Milestone.active_objects.all()
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_update(self, serializer):
        serializer.save()
        # Invalidate cache after updating a milestone
        cache.delete('milestone_list')

        response_data ={
            "message": "Milestone updated successfully",
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        #soft deleting the instance
        instance.is_deleted = True 
        instance.save()
        # deleting cache after deleting a milestone
        cache.delete('milestone_list')

        return Response('Milestone deleted successfully')

#--------------------------- Milestone Views End --------------------------