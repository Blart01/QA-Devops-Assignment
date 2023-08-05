from django import forms
from .models import Request, Project, Comment

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['subject','request_type', 'project', 'description']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if not user.is_staff:
            self.fields['project'].queryset = Project.objects.filter(owner__company=user.company)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'owner','version', 'status']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)