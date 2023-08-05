from django.test import TestCase
from requestLogger.forms import RequestForm, ProjectForm

class RequestFormTest(TestCase):
    def test_form_has_fields(self):
        form = RequestForm()
        expected = ['subject', 'request_type', 'project', 'description'] 
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

class RequestFormTest(TestCase):

    def setUp(self):
        self.data = {
            'subject': 'Install Action Plans', 
            'description': 'Configure the application to use "Action Plans" functionality', 
            'project': 1,
            'description':'I would like for Action Plans to be configured within my ongoing build so that I can more effectively track my ongoing priorities'
        }  

    def test_form_has_fields(self):
        form = RequestForm()
        expected = ['name', 'description', 'version', 'status']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_form_valid(self):
        form = RequestForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        self.data.pop('subject') 
        form = RequestForm(data=self.data)
        self.assertFalse(form.is_valid())

class ProjectFormTest(TestCase):
    def test_form_has_fields(self):
        form = ProjectForm()
        expected = ['name', 'description', 'version', 'status'] 
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)


class ProjectFormTest(TestCase):

    def setUp(self):
        self.data = {
            'name': 'Salesforce FSC Implementation', 
            'description': 'Changes to Salesforce Org for Financial Services, Wealth Management Implementation', 
            'version': '1',
            'status':'New'
        } 

    def test_form_has_fields(self):
        form = ProjectForm()
        expected = ['name', 'description', 'version', 'owner', 'status'] 
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_form_valid(self):
        form = ProjectForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        self.data.pop('name') 
        form = ProjectForm(data=self.data)
        self.assertFalse(form.is_valid())