from django.views.generic import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from forms import StoryCreateForm

class StoryCreationView(CreateView):
    form_class = StoryCreateForm

    @method_decorator(permission_required("storyviewer.edit_story"))
    def dispatch(self, *args, **kwargs):
        return super(StoryCreationView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = self.request.user
        object.save()
        return HttpResponseRedirect("/stories/")
