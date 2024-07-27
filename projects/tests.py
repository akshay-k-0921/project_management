from rest_framework.test import APITestCase
from rest_framework import status

from django.test import TestCase
from django.contrib.auth.models import User

from api.v1.projects.serializers import MilestoneSerializer, NotificationSerializer, ProjectSerializer, TaskSerializer
from .models import Milestone, Notification, Project, Task


#-------------------------- Project Model Tests Start --------------------------
class ProjectModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_project(self):
        project = Project.objects.create(
            name='Test Project',
            description='Test description',
            owner=self.user
        )
        self.assertEqual(project.name, 'Test Project')
        self.assertEqual(project.description, 'Test description')
        self.assertEqual(project.owner, self.user)

    def test_str_representation(self):
        project = Project.objects.create(
            name='Test Project',
            description='Test description',
            owner=self.user
        )
        self.assertEqual(str(project), 'Test Project')


class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_task(self):
        task = Task.objects.create(
            title='Test Task',
            description='Test description',
            status='todo',
            due_date='2022-01-01',
            assignee=self.user
        )
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Test description')
        self.assertEqual(task.status, 'todo')
        self.assertEqual(task.due_date, '2022-01-01')
        self.assertEqual(task.assignee, self.user)

    def test_str_representation(self):
        task = Task.objects.create(
            title='Test Task',
            description='Test description',
            status='todo',
            due_date='2022-01-01',
            assignee=self.user
        )
        self.assertEqual(str(task), 'Test Task')


class MilestoneModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_milestone(self):
        milestone = Milestone.objects.create(
            title='Test Milestone',
            description='Test description',
            due_date='2022-01-01',
            project=self.user
        )
        self.assertEqual(milestone.title, 'Test Milestone')
        self.assertEqual(milestone.description, 'Test description')
        self.assertEqual(milestone.due_date, '2022-01-01')
        self.assertEqual(milestone.project, self.user)

    def test_str_representation(self):
        milestone = Milestone.objects.create(
            title='Test Milestone',
            description='Test description',
            due_date='2022-01-01',
            project=self.user
        )
        self.assertEqual(str(milestone), 'Test Milestone')

class NotificationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_notification(self):
        notification = Notification.objects.create(
            user=self.user,
            subject='Test Subject',
            message='Test message'
        )
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.subject, 'Test Subject')
        self.assertEqual(notification.message, 'Test message')
        self.assertFalse(notification.is_read)

    def test_str_representation(self):
        notification = Notification.objects.create(
            user=self.user,
            subject='Test Subject',
            message='Test message'
        )
        self.assertEqual(str(notification), f"Notification for {self.user.username}: Test Subject")
#-------------------------- Project Model Tests End --------------------------


#-------------------------- Project API Tests Start --------------------------
class ProjectAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        self.project = Project.objects.create(
            name='Test Project',
            description='Test description',
            owner=self.user
        )
        self.url_list = '/projects/' 
        self.url_detail = f'/projects/{self.project.id}/'

    def test_project_list_view(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure we have one project
        self.assertEqual(response.data[0]['name'], 'Test Project')

    def test_project_create_view(self):
        response = self.client.post(self.url_list, {
            'name': 'New Project',
            'description': 'New project description'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(name='New Project').exists())

class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test description'
        )
        self.url_list = '/tasks/' 
        self.url_detail = f'/tasks/{self.task.id}/'

    def test_task_list_view(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure we have one task
        self.assertEqual(response.data[0]['title'], 'Test Task')

    def test_task_create_view(self):
        response = self.client.post(self.url_list, {
            'title': 'New Task',
            'description': 'New task description'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_task_update_view(self):
        response = self.client.put(self.url_detail, {
            'title': 'Updated Task',
            'description': 'Updated description'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_task_delete_view(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


class MilestoneAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        self.milestone = Milestone.objects.create(
            user=self.user,
            title='Test Milestone',
            description='Test description'
        )
        self.url_list = '/milestones/' 
        self.url_detail = f'/milestones/{self.milestone.id}/'

    def test_milestone_list_view(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure we have one milestone
        self.assertEqual(response.data[0]['title'], 'Test Milestone')

    def test_milestone_create_view(self):
        response = self.client.post(self.url_list, {
            'title': 'New Milestone',
            'description': 'New milestone description'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Milestone.objects.filter(title='New Milestone').exists())
        

class NotificationAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        self.notification = Notification.objects.create(
            user=self.user,
            subject='Test Subject',
            message='Test message'
        )
        self.url_list = '/notifications/' 
        self.url_detail = f'/notifications/{self.notification.id}/'

    def test_notification_list_view(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure we have one notification
        self.assertEqual(response.data[0]['subject'], 'Test Subject')

    def test_notification_create_view(self):
        response = self.client.post(self.url_list, {
            'subject': 'New Subject',
            'message': 'New message'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Notification.objects.filter(subject='New Subject').exists())

#------------------------------ Project API Tests End --------------------------

class ProjectSerializerTests(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name='Test Project',
            description='Test description'
        )
        self.serializer = ProjectSerializer(instance=self.project)

    def test_project_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['name'], 'Test Project')
        self.assertEqual(data['description'], 'Test description')

    def test_project_serializer_validation(self):
        invalid_data = {'name': ''}
        serializer = ProjectSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['name']))

class TaskSerializerTests(APITestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title='Test Task',
            description='Test description'
        )
        self.serializer = TaskSerializer(instance=self.task)

    def test_task_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['title'], 'Test Task')
        self.assertEqual(data['description'], 'Test description')

    def test_task_serializer_validation(self):
        invalid_data = {'title': ''}
        serializer = TaskSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['title']))


class MilestoneSerializerTests(APITestCase):
    def setUp(self):
        self.milestone = Milestone.objects.create(
            title='Test Milestone',
            description='Test description'
        )
        self.serializer = MilestoneSerializer(instance=self.milestone)

    def test_milestone_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['title'], 'Test Milestone')
        self.assertEqual(data['description'], 'Test description')

    def test_milestone_serializer_validation(self):
        invalid_data = {'title': ''}
        serializer = MilestoneSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['title']))


class NotificationSerializerTests(APITestCase):
    def setUp(self):
        self.notification = Notification.objects.create(
            subject='Test Subject',
            message='Test message'
        )
        self.serializer = NotificationSerializer(instance=self.notification)

    def test_notification_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['subject'], 'Test Subject')
        self.assertEqual(data['message'], 'Test message')

    def test_notification_serializer_validation(self):
        invalid_data = {'subject': ''}
        serializer = NotificationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['subject']))


#------------------------------  Serializer Tests Start ----------------------------