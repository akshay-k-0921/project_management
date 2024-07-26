from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from django.core.cache import cache

from projects.models import Project
from .serializers import ProjectSerializer
from core.permissions import IsAdminOrReadOnly, IsManagerOrReadOnly



class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.active_objects.all().select_related('owner').prefetch_related('tasks', 'milestones')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]
    
    # project list 
    def list(self, request, *args, **kwargs):
        cache_key = 'project_list'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60*15)
        return response
    # create
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        cache.delete('project_list')
    


class ProjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.active_objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_update(self, serializer):
        serializer.save()
        # Invalidate cache after updating a project
        cache.delete('project_list')  

    def perform_destroy(self, instance):
        #soft deleting the instance
        instance.is_deleted = True 
        instance.save()
        # Invalidate cache after updating a project
        cache.delete('project_list')

