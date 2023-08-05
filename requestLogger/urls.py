from django.urls import path
from .views import ProjectListView, ProjectDetailView, ProjectUpdateView, ProjectDeleteView, IndexView, RequestListView, RequestDeleteView, RequestUpdateView, RequestDetailView, RequestCreateView, OpenRequestListView, ProjectCreateView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('project/', ProjectListView.as_view(), name='project_list'),
    path('project/new/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('request/', RequestListView.as_view(), name='request_list'),
    path('request/open', OpenRequestListView.as_view(), name='request_list_open'),
    path('request/<int:pk>/', RequestDetailView.as_view(), name='request_detail'),
    path('request/<int:pk>/edit/', RequestUpdateView.as_view(), name='request_edit'),
    path('request/<int:pk>/delete/', RequestDeleteView.as_view(), name='request_delete'),
    path('request/new/', RequestCreateView.as_view(), name='request_create'),
]
