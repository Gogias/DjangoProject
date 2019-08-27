from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import models
from django.contrib.auth.models import User
from .forms import *
from .models import *
import datetime


# ──────────────────────────────────────────────────────────────────────────────────────────────#
# register - Функция регистрация пользователя.
# Формальные параметры:
# request - обязательный параметр, передающий текущий запрос.
# Локальные переменные:
# f - объект класса формы.
# ──────────────────────────────────────────────────────────────────────────────────────────────#
def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Аккаунт успещно создан!')
            return redirect('/accounts/login/')
    else:
        f = UserCreationForm()
    return render(request, 'registration/register.html', {'form': f})


# ──────────────────────────────────────────────────────────────────────────────────────────────#
# index - Функция отображения главной страницы.
# Формальные параметры:
# request - обязательный параметр, передающий текущий запрос.
# ──────────────────────────────────────────────────────────────────────────────────────────────#
def index(request):
    return render(request ,"polls/homePage.html", )


# ──────────────────────────────────────────────────────────────────────────────────────────────#
# logout_view - Функция отображения страницы выхода из системы.
# Формальные параметры:
# request - обязательный параметр, передающий текущий запрос.
# ──────────────────────────────────────────────────────────────────────────────────────────────#
def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


# ──────────────────────────────────────────────────────────────────────────────────────────────#
# userlist - Функция отображения страницы с последними проектами текущего пользователя.
# Формальные параметры:
# request - обязательный параметр, передающий текущий запрос.
# Локальные переменные:
# user_project - объект класса формы;
# context - словарь с информацией, отслыаемый в шаблон. 
# ──────────────────────────────────────────────────────────────────────────────────────────────#
def userlist(request):
    user_project = UserProject.objects.filter(user=request.user)
    context = {'project_list': user_project,}
    return render(request, 'polls/user_list.html', context)


# ──────────────────────────────────────────────────────────────────────────────────────────────#
# project_page - Функция отображения страницы с проектом.
# Формальные параметры:
# num - переменная, хранящая id записи в базе данных;
# request - обязательный параметр, передающий текущий запрос.
# Локальные переменные:
# this_project, file_list  - объекты класса формы;
# context - словарь с информацией, отслыаемый в шаблон. 
# ──────────────────────────────────────────────────────────────────────────────────────────────#
def project_page(request, num = 0,):
    this_project = Project.objects.get(pk=num)
    file_list = Files.objects.filter(project = this_project)
    
    context = {'name': this_project.name, 'date' : this_project.date, 'id' : num, 'file_list' : file_list,}
    return render(request, 'polls/project_page.html', context)


# ──────────────────────────────────────────────────────────────────────────────────────────────#
# project_create - Функция создания нового проекта и добавления данных в базу данных.
# Формальные параметры:
# request - обязательный параметр, передающий текущий запрос.
# Локальные переменные:
# project_form - объекты класса формы;
# project_user - переменная, хранящая новую запись базы данных таблицы UserProject. 
# ──────────────────────────────────────────────────────────────────────────────────────────────#
def project_create(request):
    project_form = ProjectForm()
    if request.method == 'POST':
        project_form = ProjectForm(data=request.POST)
        if project_form.is_valid():
            new_project = project_form.save(commit=False)
            new_project.save()
            project_user = UserProject.objects.create(user=request.user, project=new_project)
            project_user.save()     
        return HttpResponseRedirect("/")
    return render(request, "polls/project_create.html", {"form": project_form})


# ──────────────────────────────────────────────────────────────────────────────────────────────#
# file_create - Функция создания нового файла и добавления данных в базу данных.
# Формальные параметры:
# num - переменная, хранящая id записи в базе данных;
# request - обязательный параметр, передающий текущий запрос.
# Локальные переменные:
# file_form - объекты класса формы.
# ──────────────────────────────────────────────────────────────────────────────────────────────#
def file_create(request, num):               
    file_form = FileForm()
    if request.method == 'POST':
        file_form = FileForm(data=request.POST)
        if file_form.is_valid():
            new_file = file_form.save(commit=False)
            new_file.project = Project.objects.get(pk=num)     
            new_file.save()
        return HttpResponseRedirect("/")
    return render(request, "polls/file_create.html", {"form": file_form})


# ──────────────────────────────────────────────────────────────────────────────────────────────#
# file_page - Функция отображения страницы файла.
# Формальные параметры:
# num - переменная, хранящая id записи в базе данных;
# request - обязательный параметр, передающий текущий запрос.
# Локальные переменные:
# context - словарь с информацией, отслыаемый в шаблон.
# ──────────────────────────────────────────────────────────────────────────────────────────────#
def file_page(request, num):
    file = Files.objects.get(pk=num)
    context = {'name': file.name, 'date_c' : file.create_date,'date_u' : file.update_date ,'id' : num, 'text' : file.text, 'project' : file.project}
    return render(request, 'polls/file_page.html', context)


# ──────────────────────────────────────────────────────────────────────────────────────────────#
# file_change - Функция создания новой версии файла, сохренения старой и добавления информации в базу данных.
# Формальные параметры:
# num - переменная, хранящая id записи в базе данных;
# request - обязательный параметр, передающий текущий запрос.
# Локальные переменные:
# change_form  - объект класса формы;
# change_file  - объект записи базы данных, хранящий изменяемый файл;
# text - новый текст файла.
# ──────────────────────────────────────────────────────────────────────────────────────────────#
def file_change(request, num):
    change_form = ChangeForm()
    change_file = Files.objects.get(pk=num)
    text = change_file.text
    if request.method == 'POST':
        change_form = ChangeForm(data=request.POST)
        if change_form.is_valid():
            new_change = change_form.save(commit=False)
            new_change.change_user = request.user
            new_change.file = change_file
            change_file.text = new_change.choice_text
            new_change.choice_text = text
            change_file.update_date = datetime.datetime.now()
            new_change.save()
            change_file.save()
        return HttpResponseRedirect("/")
    return render(request, "polls/file_change.html", {"form": change_form})


# ──────────────────────────────────────────────────────────────────────────────────────────────#
# change_page - Функция отображения истории изменения текущего файла.
# Формальные параметры:
# num - переменная, хранящая id записи в базе данных;
# request - обязательный параметр, передающий текущий запрос.
# Локальные переменные:
# this_file  - объект записи базы данных, хранящий текущий файл;
# change_list - список изменений файла;
# context - словарь с информацией, отслыаемый в шаблон.
# ──────────────────────────────────────────────────────────────────────────────────────────────#
def change_page(request, num):
    this_file = Files.objects.get(pk=num)
    change_list = Changes.objects.filter(file = this_file)
    context = {'name': this_file.name, 'date' : this_file.create_date, 'id' : num, 'change_list' : change_list,}
    return render(request, 'polls/change_page.html', context)


# ──────────────────────────────────────────────────────────────────────────────────────────────#
# old_file - Функция отображения старой версии файла.
# Формальные параметры:
# num - переменная, хранящая id записи в базе данных;
# request - обязательный параметр, передающий текущий запрос.
# Локальные переменные:
# this_change  - объект записи базы данных, хранящий текущий файл;
# context - словарь с информацией, отслыаемый в шаблон.
# ──────────────────────────────────────────────────────────────────────────────────────────────#
def old_file(request, num):
    this_change = Changes.objects.get(pk=num)
    context = {'user' : request.user,' change_user' : this_change.change_user.username, 'date' : this_change.change_date, 'text' : this_change.choice_text}
    return render(request, 'polls/old_file.html', context)


# ──────────────────────────────────────────────────────────────────────────────────────────────#
# add_user - Функция добавления пользователя в проект.
# Формальные параметры:
# num - переменная, хранящая id записи в базе данных;
# request - обязательный параметр, передающий текущий запрос.
# Локальные переменные:
# add_user_form  - объект класса формы;
# context - словарь с информацией, отслыаемый в шаблон.
# ──────────────────────────────────────────────────────────────────────────────────────────────#
def add_user(request, num):
    add_user_form = UserProjectForm()
    context = {'project' : Project.objects.get(pk=num),'form' : add_user_form }
    return render(request, 'polls/add_user.html', context)
