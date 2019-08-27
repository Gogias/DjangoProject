from django.db import models
from django.contrib.auth.models import User

#──────────────────────────────────────────────────────────────────────────────────────────────#
# Project - Класс модели, содержащий описание полей и функций таблицы Project базы данных.
# Используемые функции:
# __str__ - функция строкового отображения экзепляра класса;
# get_absolute_url - Функция абсолютного url для конкретного экземпляра класса.
# Используемые переменные:
# name - имя проекта;
# date - дата создания проекта.
#──────────────────────────────────────────────────────────────────────────────────────────────#
class Project(models.Model):
    name = models.CharField(max_length=20)
    date = models.DateTimeField('date published', auto_now_add=True)
    #users = models.ForeignKey(UserProject) #был user
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
    	return "/project/%i/" % self.id


#──────────────────────────────────────────────────────────────────────────────────────────────#
# UserProject - Класс модели, содержащий описание полей и функций сводной таблицы UserProject базы данных.
# Используемые функции:
# __str__ - функция строкового отображения экзепляра класса;
# get_absolute_url - Функция абсолютного url для конкретного экземпляра класса.
# Используемые переменные:
# user - объект класса User;
# project - объект класса Project.
#──────────────────────────────────────────────────────────────────────────────────────────────#
class UserProject(models.Model):		#не было ничего
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)

	def __str__(self):
		return self.project

	def get_absolute_url(self):
		return "/project/%i/" % self.project.id


#──────────────────────────────────────────────────────────────────────────────────────────────#
# Files - Класс модели, содержащий описание полей и функций таблицы File базы данных.
# Используемые функции:
# __str__ - функция строкового отображения экзепляра класса;
# get_absolute_url - Функция абсолютного url для конкретного экземпляра класса.
# Используемые переменные:
# name - имя файла;
# create_date - дата создания файла;
# update_date - дата последнего обновления;
# text - текст файла;
# project - проект, к которому относится файл.
#──────────────────────────────────────────────────────────────────────────────────────────────#
class Files(models.Model):
    name = models.CharField(max_length=20)
    create_date = models.DateTimeField('date published',auto_now_add=True )
    update_date = models.DateTimeField('date updated',auto_now_add=True)
    text = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE) # требует дефолт

    def __str__(self):
    	return self.name

    def get_absolute_url(self):
    	return "/file/%i/" % self.id


#──────────────────────────────────────────────────────────────────────────────────────────────#
# Changes - Класс модели, содержащий описание полей и функций таблицы Changes базы данных.
# Используемые функции:
# __str__ - функция строкового отображения экзепляра класса;
# get_absolute_url - Функция абсолютного url для конкретного экземпляра класса.
# Используемые переменные:
# file - файл, который изменяется;
# choice_text - новый текст файла;
# change_date - дата обновления;
# text - текст файла;
# change_user - пользователь, который сделал изменение.
#──────────────────────────────────────────────────────────────────────────────────────────────#
class Changes(models.Model):
    file = models.ForeignKey(Files, on_delete=models.CASCADE)
    choice_text = models.TextField()
    change_date = models.DateTimeField('date published',auto_now_add=True)
    change_user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
 
    def __str__(self):
        return str(self.change_date)

    def get_absolute_url(self):
        return "/old_file/%i/" % self.id