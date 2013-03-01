from django.forms import ModelForm
from models import Story, Chapter

class StoryCreateForm(ModelForm):
    class Meta:
        model = Story
        exclude = ("author")

class ChapterCreateForm(ModelForm):
    class Meta:
        model = Chapter
        exclude = ("author", "parent", "story")