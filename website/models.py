from operator import mod
from django.db import models


class Admin(models.Model):
    user_name = models.CharField(verbose_name='User name', max_length=32)
    password = models.CharField(verbose_name='password', max_length=64)


class Department(models.Model):
    title = models.CharField(max_length=32)
    def __str__(self) -> str:
        return self.title

class Employee(models.Model):
    name = models.CharField(verbose_name='Name', max_length=16)
    password = models.CharField(max_length=64)

    # dept = models.ForeignKey(verbose_name='Department', to='Department', to_field='id', null=True, blank=True, on_delete=models.SET_NULL)
    dept = models.ForeignKey(verbose_name='Department', to='Department', to_field='id', on_delete=models.CASCADE)
    
    create_time = models.DateTimeField(verbose_name='Create Time')
    gender_choices = ((1, 'F'), (2, 'M'))
    gender = models.SmallIntegerField(verbose_name='Gender', choices=gender_choices)
    age = models.IntegerField(verbose_name='Age', null=True, blank=True)
