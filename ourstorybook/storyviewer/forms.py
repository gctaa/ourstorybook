from django.conf import settings
from django.forms import CharField, ModelForm
from django.contrib.auth.forms import UserCreationForm
from models import Story, Page

class StoryCreateForm(ModelForm):
    class Meta:
        model = Story
        exclude = ("author")

class PageCreateForm(ModelForm):
    class Meta:
        model = Page
        exclude = ("author", "parent", "story")

class RichUserCreationForm(UserCreationForm):
    first_name = CharField(label = "First name")
    last_name = CharField(label = "Last name")

    def save(self, commit=True):
        user = super(RichUserCreationForm, self).save(commit=False)
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        user.first_name = first_name
        user.last_name = last_name
        if commit:
            user.save()
        return user

class TokenRegistrationForm(RichUserCreationForm):
    token = CharField(max_length=20, label="Registration Token")

    def clean_token(self):
        data = self.cleaned_data["token"]
        if data != settings.REGISTRATION_TOKEN:
            raise forms.ValidationError("Incorrect Registration Token!")
        return data
