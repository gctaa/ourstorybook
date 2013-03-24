from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, RedirectView
from django.contrib.auth.views import login, logout
from storyviewer.models import Story
from storyviewer.views import StoryCreationView, StoryDetailView, PageCreationView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/stories/')),
    url(r'^stories/$', ListView.as_view(model=Story, queryset=Story.objects.all())),
    url(r'^stories/(?P<pk>\d+)/$', StoryDetailView.as_view()),
    url(r'^create_story/$', StoryCreationView.as_view()),
    url(r'^add_page/(?P<pk>\d+)/$', PageCreationView.as_view()),
    url(r'^login/$', login),
    url(r'^logout/$', logout, {'next_page': '/'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
