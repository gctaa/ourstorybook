from django.forms import ModelForm
from models import Story

class StoryCreateForm(ModelForm):
    class Meta:
        model = Story
        exclude = ("author")
