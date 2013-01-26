from django.db import models
from django.contrib.auth.models import User

# Story model (represents an entire story, made up of Chapters)
class Story(models.Model):
    class Meta():
        verbose_name_plural = 'stories'

    title = models.CharField(max_length=140)
    author = models.ForeignKey(User)

# Chapter model (represents a chapter/branch of a Story)
class Chapter(models.Model):
    title = models.CharField(max_length=140)
    author = models.ForeignKey(User)
    story = models.ForeignKey(Story)
    parent = models.ForeignKey('Chapter')
    content = models.TextField()
