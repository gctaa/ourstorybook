from django.views.generic import CreateView, DetailView
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from forms import StoryCreateForm, PageCreateForm
from models import Story, Page

class StoryCreationView(CreateView):
    form_class = StoryCreateForm
    template_name = 'storyviewer/story_create.html'

    @method_decorator(permission_required('storyviewer.edit_story'))
    def dispatch(self, *args, **kwargs):
        self.request.session['last_story_id'] = None
        self.request.session['last_page_id'] = None
        return super(StoryCreationView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = self.request.user
        object.save()
        return HttpResponseRedirect('/stories/')

class StoryDetailView(DetailView):
    model = Story
    template_name = 'storyviewer/story_detail.html'
    
    def dispatch(self, *args, **kwargs):
        self.request.session['last_story_id'] = self.get_object().id
        self.request.session['last_page_id'] = None
        return super(StoryDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StoryDetailView, self).get_context_data(**kwargs)
        context['nodes'] = Page.objects.filter(story=self.object)
        return context

class PageCreationView(CreateView):
    form_class = PageCreateForm
    template_name = 'storyviewer/page_create.html'

    #
    #   TODO - ensure input is cleaned
    #   do some magic in form_valid to ensure parents are set (see django-mptt docs)
    #
    @method_decorator(permission_required('storyviewer.edit_page'))
    def dispatch(self, *args, **kwargs):
        self.story = get_object_or_404(Story, pk=self.request.session.get('last_story_id'))
        parent_page_id = self.request.session.get('last_page_id')
        if parent_page_id:
            self.parent_page = Page.objects.get(pk=parent_page_id)
        else:
            self.parent_page = None
        return super(PageCreationView, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(PageCreationView, self).get_context_data(**kwargs)
        context['story'] = self.story
        context['parent_page'] = self.parent_page
        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.story = self.story
        object.parent = self.parent_page
        object.author = self.request.user
        object.save()
        return HttpResponseRedirect('/stories/%s/' % self.story.id)
        
class PageDetailView(DetailView):
    model = Page
    template_name = 'storyviewer/page_detail.html'
    
    def dispatch(self, *args, **kwargs):
        self.request.session['last_story_id'] = self.get_object().story.id
        self.request.session['last_page_id'] = self.get_object().id
        return super(PageDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)
        context['nodes'] = self.object.get_descendants()
        return context
