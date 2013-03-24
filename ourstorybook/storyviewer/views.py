from django.views.generic import CreateView, DetailView
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from forms import StoryCreateForm, PageCreateForm
from models import Story, Page

class StoryCreationView(CreateView):
    form_class = StoryCreateForm
    template_name = 'storyviewer/story_create.html'

    @method_decorator(permission_required('storyviewer.edit_story'))
    def dispatch(self, *args, **kwargs):
        return super(StoryCreationView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = self.request.user
        object.save()
        return HttpResponseRedirect('/stories/')

class StoryDetailView(DetailView):
    model = Story
    template_name='storyviewer/story_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(StoryDetailView, self).get_context_data(**kwargs)
        context['nodes'] = Page.objects.filter(story=self.object)
        return context

class PageCreationView(CreateView):
    form_class = PageCreateForm
    template_name='storyviewer/page_create.html'

    @method_decorator(permission_required('storyviewer.edit_page'))
    def dispatch(self, *args, **kwargs):
        self.story = Story.objects.get(id=kwargs['pk'])
        return super(PageCreationView, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(PageCreationView, self).get_context_data(**kwargs)
        context['story'] = self.story
        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = self.request.user
        object.story = self.story
        object.save()
        return HttpResponseRedirect('/stories/%s/' % self.story.id) # TODO
