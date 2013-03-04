from django.forms import ModelForm
from models import Story, Page

class StoryCreateForm(ModelForm):
    class Meta:
        model = Story
        exclude = ("author")

class PageCreateForm(ModelForm):
    class Meta:
        model = Page
        exclude = ("author", "parent", "story")
