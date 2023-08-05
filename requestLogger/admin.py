from django.contrib import admin
from .models import Company, User, Project, Request

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact_email')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'company', 'phone_number', 'employee_id')
    list_filter = ('role', 'company')
    search_fields = ('username', 'email', 'phone_number')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner', 'version', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'owner__username', 'version')

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('subject', 'request_type', 'project', 'requester', 'status', 'date_submitted')
    list_filter = ('request_type', 'project', 'status')
    search_fields = ('subject', 'project__name', 'requester__username')
