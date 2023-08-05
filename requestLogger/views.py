from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project, Request, Comment
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RequestForm, ProjectForm, CommentForm
from django.views import generic
from django.db.models import Q



class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'index.html'

    login_url = '/login/'  # URL to redirect to if the user is not logged in
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        user_company = user.company
        
        # Get the number of projects owned by the user's company
        context['num_projects'] = Project.objects.filter(owner__company=user_company).count()

        # Get the number of outstanding requests related to projects owned by the user's company
        context['num_outstanding_requests'] = Request.objects.filter(
            project__owner__company=user_company,
            status='New'
        ).count()

        # Get the number of resolved requests related to projects owned by the user's company
        context['num_resolved_requests'] = Request.objects.filter(
            project__owner__company=user_company,
            status='Resolved'
        ).count()

        # Add the current user to the context
        context['user'] = user

        return context


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'requestLogger/project_list.html'
    login_url = '/login/'  # URL to redirect to if the user is not logged in


    def get_queryset(self):
        user = self.request.user
        if user.role == 'staff':
            return Project.objects.all()
        return Project.objects.filter(owner__company=user.company)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'requestLogger/project_form.html'
    login_url = '/login/'  # URL to redirect to if the user is not logged in

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'requestLogger/project_detail.html'
    login_url = '/login/'  # URL to redirect to if the user is not logged in

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['requests'] = Request.objects.filter(project=self.object)
        return context

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.role == 'staff' or obj.owner.company == user.company:
            return obj
        else:
            return get_object_or_404(Project, id=-1)  # Raises 404 as this user does not belong to the same organisation as the request


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'requestLogger/project_form.html'
    login_url = '/login/'  # URL to redirect to if the user is not logged in

    def form_valid(self, form):
        user = self.request.user
        if not user.role == 'staff':
            raise Http404("You don't have permission to edit this project.")
        return super().form_valid(form)


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'requestLogger/project_delete.html'
    success_url = reverse_lazy('project_list')
    login_url = '/login/'  # URL to redirect to if the user is not logged in

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.role == 'staff' or obj.requester == user:
            return obj
        else:
            return get_object_or_404(Project, id=-1)  # Will always raise Http404
        

class RequestDetailView(LoginRequiredMixin, DetailView):
    model = Request
    template_name = 'requestLogger/request_detail.html'
    login_url = '/login/'  # URL to redirect to if the user is not logged in

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(request=self.object).order_by('-created_date')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.request = self.object
            comment.author = request.user
            # Check if the logged in user is a staff member or belongs to the same organisation as the request
            if (not self.request.user.role == 'staff') and self.request.user.company != self.object.requester.company:
                return HttpResponseForbidden("You don't have permission to comment on this request.")
            comment.save()
            return self.get(self, request, *args, **kwargs)  # redirects back to the detail view

        context = self.get_context_data(**kwargs)
        context['comment_form'] = form
        return render(request, self.template_name, context)
    
    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.role == 'staff' or obj.requester.company == user.company:
            return obj
        else:
            return get_object_or_404(Project, id=-1)  # Will always raise Http404


class RequestCreateView(LoginRequiredMixin, CreateView):
    model = Request
    form_class = RequestForm
    template_name = 'requestLogger/request_form.html'
    login_url = '/login/'  # URL to redirect to if the user is not logged in

    def form_valid(self, form):
        form.instance.requester = self.request.user
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    def get_absolute_url(self):
        return reverse('request_detail', kwargs={'pk': self.pk})

class RequestUpdateView(LoginRequiredMixin, UpdateView):
    model = Request
    form_class = RequestForm
    template_name = 'requestLogger/request_form.html'
    login_url = '/login/'  # URL to redirect to if the user is not logged in

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        if form.instance.requester.company != self.request.user.company and not self.request.user.role == 'staff':
            raise Http404("You don't have permission to edit this request.")
        return super().form_valid(form)

    def get_absolute_url(self):
        return reverse('request_detail', kwargs={'pk': self.pk})
    

class RequestDeleteView(LoginRequiredMixin, DeleteView):
    model = Request
    template_name = 'requestLogger/request_delete.html'
    success_url = reverse_lazy('request_list')
    login_url = '/login/'  # URL to redirect to if the user is not logged in

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.role == 'staff' or obj.requester.company == user.company:
            return obj
        else:
            return get_object_or_404(Request, id=-1)  # Raises 404 as this user does not belong to the same organisation as the request


class RequestListView(LoginRequiredMixin, ListView):
    model = Request
    template_name = 'requestLogger/request_list.html'
    login_url = '/login/'  # URL to redirect to if the user is not logged in

    def get_queryset(self):
        user = self.request.user
        if user.role == 'staff':
            return Request.objects.all()
        return Request.objects.filter(requester__company=user.company)

class OpenRequestListView(LoginRequiredMixin, ListView):
    model = Request
    template_name = 'requestLogger/request_list.html'
    login_url = '/login/'  # URL to redirect to if the user is not logged in

    def get_queryset(self):
        user = self.request.user
        if user.role == 'staff':
            return Request.objects.filter(Q(status='New') | Q(status='In Progress'))
        
        return Request.objects.filter(requester__company=user.company and Q(status='New') | Q(status='In Progress'))


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'requestLogger/comment_form.html'
    login_url = '/login/'  # URL to redirect to if the user is not logged in

    def form_valid(self, form):
        form.instance.author = self.request.user
        request = get_object_or_404(Request, id=self.kwargs['request_id'])

        # Check if the logged in user is a staff member or belongs to the same organisation as the request
        if not self.request.user.role == 'staff' and self.request.user.company != request.requester.company:
            return HttpResponseForbidden("You don't have permission to comment on this request.")

        form.instance.request = request
        return super().form_valid(form)