from django.urls import path
from . import views
from django.conf.urls import url, include

# ──────────────────────────────────────────────────────────────────────────────────────────────#
# Локальные переменные:
# urlpatterns - переменная, содержащая массив url адресов и соответствующих представлений.
# ──────────────────────────────────────────────────────────────────────────────────────────────#
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^latest-users/$', views.userlist, name='userlist'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^create_project/$', views.project_create, name='project_create'),
    path('project/<int:num>/', views.project_page, name="project_page"),
    path('create_file/<int:num>/', views.file_create, name='file_create'),
    path('file/<int:num>/', views.file_page, name="file_page"),
    path('file_change/<int:num>/', views.file_change, name="file_change"),
    path('change_page/<int:num>/', views.change_page, name="change_page"),
    path('old_file/<int:num>/', views.old_file, name="old_file"),
    path('add_user/<int:num>/', views.add_user, name="add_user"),
]