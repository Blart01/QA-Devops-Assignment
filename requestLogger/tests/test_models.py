from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import User, Company, Request, Comment

class CompanyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Company.objects.create(name='Test Company', address='123 Test St', contact_email='test@test.com')

    def test_name_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_address_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'address')

    def test_contact_email_label(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('contact_email').verbose_name
        self.assertEquals(field_label, 'contact email')

    def test_name_max_length(self):
        company = Company.objects.get(id=1)
        max_length = company._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_address_max_length(self):
        company = Company.objects.get(id=1)
        max_length = company._meta.get_field('address').max_length
        self.assertEquals(max_length, 500)

    def test_object_name_is_name(self):
        company = Company.objects.get(id=1)
        expected_object_name = f'{company.name}'
        self.assertEquals(expected_object_name, str(company))

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Company.objects.create(name='Test Company', address='123 Test St', contact_email='test@test.com')
        User.objects.create(username='testuser', role='customer', company=Company.objects.get(name='Test Company'))

    def test_role_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('role').verbose_name
        self.assertEquals(field_label, 'role')

    def test_company_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('company').verbose_name
        self.assertEquals(field_label, 'company')

    def test_phone_number_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('phone_number').verbose_name
        self.assertEquals(field_label, 'phone number')

    def test_employee_id_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('employee_id').verbose_name
        self.assertEquals(field_label, 'employee id')

    def test_role_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('role').max_length
        self.assertEquals(max_length, 8)

    def test_phone_number_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('phone_number').max_length
        self.assertEquals(max_length, 50)

    def test_employee_id_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('employee_id').max_length
        self.assertEquals(max_length, 20)


from django.test import TestCase
from django.utils import timezone
from ..models import Project, User, Company

class ProjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Company.objects.create(name='Test Company', address='123 Test St', contact_email='test@test.com')
        User.objects.create(username='testuser', role='customer', company=Company.objects.get(name='Test Company'))
        Project.objects.create(name='Test Project', description='A test project', owner=User.objects.get(username='testuser'), version='1.0.0')

    def test_name_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_description_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_owner_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('owner').verbose_name
        self.assertEquals(field_label, 'owner')

    def test_created_at_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'created at')

    def test_last_updated_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('last_updated').verbose_name
        self.assertEquals(field_label, 'last updated')

    def test_version_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('version').verbose_name
        self.assertEquals(field_label, 'version')

    def test_status_label(self):
        project = Project.objects.get(id=1)
        field_label = project._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'status')

    def test_name_max_length(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_version_max_length(self):
        project = Project.objects.get(id=1)
        max_length = project._meta.get_field('version').max_length
        self.assertEquals(max_length, 50)

    def test_object_name_is_name(self):
        project = Project.objects.get(id=1)
        expected_object_name = project.name
        self.assertEquals(expected_object_name, str(project))

    def test_get_absolute_url(self):
        project = Project.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(project.get_absolute_url(), '/project/1/')


class RequestModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.requester = User.objects.create(username='testuser')
        cls.project = Project.objects.create(name='Test Project', owner_id=cls.requester.id)
        cls.request = Request.objects.create(
            subject='Test Request',
            project=cls.project,
            requester=cls.requester,
            description='This is a test request',
            status=Request.Status.NEW,
        )

    def test_str_method(self):
        # Test the __str__ method of the Request model
        self.assertEqual(str(self.request), 'Service Request for Test Project by testuser')

    
    def test_default_status_value(self):
        # Test the default value of status field
        new_request = Request.objects.create(
            subject='Another Request',
            project=self.project,
            requester=self.requester,
            description='This is another test request',
        )
        self.assertEqual(new_request.status, Request.Status.NEW)

    def test_change_status(self):
        # Test changing the status of the request
        self.request.status = Request.Status.IN_PROGRESS
        self.request.save()
        updated_request = Request.objects.get(pk=self.request.pk)
        self.assertEqual(updated_request.status, Request.Status.IN_PROGRESS)
