from django.db import models
from django.utils import timezone

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=30)
    groups = models.ManyToManyField('Group', related_name='persons', through='Membership')

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Membership(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='memberships')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='memberships')
    joined_on = models.DateField(default=timezone.now().utcnow())
