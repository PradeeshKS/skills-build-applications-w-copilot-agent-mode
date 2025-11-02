from django.db import models
from djongo import models as djongo_models

class Team(models.Model):
    id = djongo_models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

class User(models.Model):
    id = djongo_models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    team = djongo_models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='members', to_field='id')
    is_superhero = models.BooleanField(default=False)

class Activity(models.Model):
    id = djongo_models.ObjectIdField(primary_key=True)
    user = djongo_models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities', to_field='id')
    type = models.CharField(max_length=50)
    duration = models.IntegerField(help_text='Duration in minutes')
    timestamp = models.DateTimeField(auto_now_add=True)

class Workout(models.Model):
    id = djongo_models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    suggested_for = djongo_models.ManyToManyField(User, blank=True)

class Leaderboard(models.Model):
    id = djongo_models.ObjectIdField(primary_key=True)
    team = djongo_models.ForeignKey(Team, on_delete=models.CASCADE, related_name='leaderboards', to_field='id')
    points = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
