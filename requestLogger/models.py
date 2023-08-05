from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    contact_email = models.EmailField()

    def __str__(self):
        return self.name

class User(AbstractUser):
    
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
    ]
    role = models.CharField(max_length=8, choices=ROLE_CHOICES)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    employee_id = models.CharField(max_length=20, null=True, blank=True)

    def clean(self):
        super().clean()
        if self.role == 'customer' and not self.company:
            raise ValidationError({
                'company': _('Customers must have a company associated with them.')
            })

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    version = models.CharField(max_length=50)

    class Status(models.TextChoices):
        ACTIVE = 'Active', _('Active')
        INACTIVE = 'Inactive', _('Inactive')
        DEPRECATED = 'Deprecated', _('Deprecated')
    
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.ACTIVE,)

    def get_absolute_url(self):
        return reverse('project_detail', args=[str(self.id)])

    def __str__(self):
        return self.name



class Request(models.Model):

    class RequestType(models.TextChoices):
        CHANGE = 'Change', _('Change')
        SERVICE_REQUEST = 'Service Request', _('Service Request')

    subject = models.CharField(max_length=100)
    request_type = models.CharField(max_length=15, choices=RequestType.choices, default=RequestType.SERVICE_REQUEST)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='requests')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    description = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    class Status(models.TextChoices):
        NEW = 'New', _('New')
        IN_PROGRESS = 'In Progress', _('In Progress')
        RESOLVED = 'Resolved', _('Resolved')
        REJECTED = 'Rejected', _('Rejected')
        CANCELLED = 'Cancelled', _('Cancelled')

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    def get_absolute_url(self):
        return reverse('request_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.request_type} for {self.project} by {self.requester}'

class Comment(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)