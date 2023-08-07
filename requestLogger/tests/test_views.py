from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Company, Project, Request
from ..views import ProjectListView, ProjectDetailView, ProjectUpdateView, ProjectDeleteView, IndexView, RequestListView, RequestDeleteView, RequestUpdateView, RequestDetailView, RequestCreateView, OpenRequestListView, ProjectCreateView
from django.contrib.auth import get_user_model


class IndexViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create a test company
        self.company = Company.objects.create(name='Test Company')

        # Create test projects owned by the test company
        self.project1 = Project.objects.create(name='Project 1', owner=self.company)
        self.project2 = Project.objects.create(name='Project 2', owner=self.company)

        # Create test requests related to the projects
        self.request1 = Request.objects.create(subject='Request 1', project=self.project1, requester=self.user, status=Request.Status.NEW)
        self.request2 = Request.objects.create(subject='Request 2', project=self.project2, requester=self.user, status=Request.Status.RESOLVED)



class ProjectListViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a test user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create a test company
        self.company = Company.objects.create(name='Test Company')

        # Create test projects owned by the test company
        self.project1 = Project.objects.create(name='Project 1', owner=self.company)
        self.project2 = Project.objects.create(name='Project 2', owner=self.company)




User = get_user_model()

class TestProjectCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.login_url = reverse('login')
        self.create_url = reverse('project_create')

    def test_not_logged_in(self):
        response = self.client.post(self.create_url, {
            'name': 'Test Project',
            'description': 'Test Project Description',
            'version': '1.0',
            'status': Project.Status.ACTIVE
        })
        self.assertRedirects(response, '{}?next={}'.format(self.login_url, self.create_url)) # Check if redirected to login


class TestProjectUpdateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='staffpass',
            role='staff'
        )
        self.normal_user = User.objects.create_user(
            username='normaluser',
            password='normalpass',
            role='customer'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Project Description',
            version='1.0',
            status=Project.Status.ACTIVE,
            owner=self.staff_user,
        )
        self.update_url = reverse('project_update', args=[str(self.project.id)])



class TestProjectDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='staffpass',
            role='staff'
        )
        self.requester_user = User.objects.create_user(
            username='requesteruser',
            password='requesterpass',
            role='normal'
        )
        self.normal_user = User.objects.create_user(
            username='normaluser',
            password='normalpass',
            role='normal'
        )
        self.project1 = Project.objects.create(
            name='Test Project 1',
            description='Test Project Description 1',
            version='1.0',
            status=Project.Status.ACTIVE,
            owner=self.staff_user,
        )
        self.project2 = Project.objects.create(
            name='Test Project 2',
            description='Test Project Description 2',
            version='1.0',
            status=Project.Status.ACTIVE,
            owner=self.requester_user,
        )
        self.delete_url1 = reverse('project_delete', args=[str(self.project1.id)])
        self.delete_url2 = reverse('project_delete', args=[str(self.project2.id)])

    def test_delete_view_staff(self):
        self.client.login(username='staffuser', password='staffpass')
        response = self.client.post(self.delete_url1)
        self.assertEqual(response.status_code, 302) # Check if redirected
        self.assertFalse(Project.objects.filter(id=self.project1.id).exists()) # Check if project1 is deleted

