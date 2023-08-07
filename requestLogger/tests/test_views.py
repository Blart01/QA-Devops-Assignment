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

    def test_index_view_with_logged_in_user(self):
        # Test the index view for a logged-in user
        url = reverse('index')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

        # Check if the context data is correct
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.context['num_projects'], 2)
        self.assertEqual(response.context['num_outstanding_requests'], 1)
        self.assertEqual(response.context['num_resolved_requests'], 1)

    def test_index_view_with_anonymous_user(self):
        # Test the index view for an anonymous user (not logged in)
        self.client.logout()
        url = reverse('index')
        response = self.client.get(url)

        self.assertRedirects(response, '/login/?next=/')  # Should be redirected to login page

    def test_index_view_with_no_projects(self):
        # Test the index view when the user's company has no projects
        self.project1.delete()
        self.project2.delete()

        url = reverse('index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

        # Check if the context data is correct
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.context['num_projects'], 0)
        self.assertEqual(response.context['num_outstanding_requests'], 0)
        self.assertEqual(response.context['num_resolved_requests'], 0)

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

    def test_project_list_view_for_staff_user(self):
        # Test the project list view for a staff user
        self.user.role = 'staff'
        self.user.save()

        url = reverse('project-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'requestLogger/project_list.html')
        self.assertQuerysetEqual(response.context['object_list'], ['<Project: Project 1>', '<Project: Project 2>'])

    def test_project_list_view_for_company_user(self):
        # Test the project list view for a user belonging to the company
        self.user.company = self.company
        self.user.save()

        url = reverse('project-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'requestLogger/project_list.html')
        self.assertQuerysetEqual(response.context['object_list'], ['<Project: Project 1>', '<Project: Project 2>'])

    def test_project_list_view_for_non_company_user(self):
        # Test the project list view for a user not belonging to any company
        self.user.company = None
        self.user.save()

        url = reverse('project-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'requestLogger/project_list.html')
        self.assertQuerysetEqual(response.context['object_list'], [])  # No projects should be visible


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


class TestProjectDetailView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            role='customer',
            company='1'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass',
            role='customer',
            company='2'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Project Description',
            version='1.0',
            status=Project.Status.ACTIVE,
            owner=self.user,
        )
        self.detail_url = reverse('project_detail', args=[str(self.project.id)])

    def test_detail_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200) # Check if response is OK
        self.assertEqual(response.context['object'], self.project) # Check if correct project is fetched

    def test_detail_view_unauthorized_user(self):
        self.client.login(username='otheruser', password='otherpass')
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 404) # Check if 404 is returned



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

    def test_update_view_staff(self):
        self.client.login(username='staffuser', password='staffpass')
        response = self.client.post(self.update_url, {
            'name': 'Updated Project',
            'description': 'Updated Project Description',
            'version': '2.0',
            'status': Project.Status.INACTIVE
        })
        self.assertEqual(response.status_code, 302) # Check if redirected
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Updated Project') # Check if project name is updated
        self.assertEqual(self.project.version, '2.0') # Check if project version is updated

    def test_update_view_normal_user(self):
        self.client.login(username='normaluser', password='normalpass')
        response = self.client.post(self.update_url, {
            'name': 'Updated Project',
            'description': 'Updated Project Description',
            'version': '2.0',
            'status': Project.Status.INACTIVE
        })
        self.assertEqual(response.status_code, 404) # Check if 404 is returned


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

    def test_delete_view_requester(self):
        self.client.login(username='requesteruser', password='requesterpass')
        response = self.client.post(self.delete_url2)
        self.assertEqual(response.status_code, 302) # Check if redirected
        self.assertFalse(Project.objects.filter(id=self.project2.id).exists()) # Check if project2 is deleted

    def test_delete_view_normal_user(self):
        self.client.login(username='normaluser', password='normalpass')
        response = self.client.post(self.delete_url1)
        self.assertEqual(response.status_code, 404) # Check if 404 is returned
        self.assertTrue(Project.objects.filter(id=self.project1.id).exists()) # Check if project1 is not deleted
