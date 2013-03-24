from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
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

# Page model (represents a page of a Story)
class Page(MPTTModel):
    title = models.CharField(max_length=140, unique=True, null=False)
    author = models.ForeignKey(User, null=False)
    story = models.ForeignKey(Story, null=False)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="children")
    content = models.TextField(null=False)

    def __unicode__(self):
        return "%s: %s"% (self.story.title, self.title)

    class MPTTMeta:
        order_insertion_by = ['title']