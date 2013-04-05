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
        return super(StoryCreationView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = self.request.user
        object.save()
        return HttpResponseRedirect('/stories/')

class StoryDetailView(DetailView):
    model = Story
    template_name = 'storyviewer/story_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(StoryDetailView, self).get_context_data(**kwargs)
        context['nodes'] = Page.objects.filter(story=self.object)
        return context

class PageCreationView(CreateView):
    form_class = PageCreateForm
    template_name = 'storyviewer/page_create.html'

    #
    #   TODO - attach storyid and parentid to POST request in forms/template
    #   ensure input is cleaned
    #   do some magic in form_valid to ensure parents are set (see django-mptt docs)
    #
    @method_decorator(permission_required('storyviewer.edit_page'))
    def dispatch(self, *args, **kwargs):
        # On GET requests, story/parent_page ID will come in via the url querystrings
        # On POST requests, the story/parent_page ID will come in via POST data
        if self.request.method == 'GET':
            request_method = self.request.GET
        elif self.request.method == 'POST':
            request_method = self.request.POST
        
        #import pdb; pdb.set_trace();
        
        self.story = get_object_or_404(Story, pk=request_method.get('story'))
        try:
            self.parent_page = Page.objects.get(pk=request_method.get('parent_page'))
        except Page.DoesNotExist:
            self.parent_page = None
        
        return super(PageCreationView, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(PageCreationView, self).get_context_data(**kwargs)
        context['story'] = self.story
        context['parent_page'] = self.parent_page
        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.author = self.request.user
        object.story = self.story
        object.save()
        return HttpResponseRedirect('/stories/%s/' % self.story.id)
        
class PageDetailView(DetailView):
    model = Page
    template_name = 'storyviewer/page_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)
        context['nodes'] = self.object.get_descendants()
        return context
