from django.db import models
from django.contrib.auth.models import User

# Story model (represents an entire story, made up of Chapters)
class Story(models.Model):
    title = models.CharField(max_length=140)
    author = models.ForeignKey(User, null=False)
    description = models.TextField(null=False)

    def __unicode__(self):
        return self.title

    class Meta():
        verbose_name_plural = "stories"

# Chapter model (represents a chapter/branch of a Story)
class Chapter(models.Model):
    title = models.CharField(max_length=140)
    author = models.ForeignKey(User, null=False)
    story = models.ForeignKey(Story, null=False)
    parent = models.ForeignKey("Chapter", blank=True, null=True, default=None)
    content = models.TextField(null=False)

    def __unicode__(self):
        return "%s: %s"% (self.story.title, self.title)
