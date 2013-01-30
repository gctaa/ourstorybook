from django.conf.urls import patterns, include, url
from django.views.generic import ListView, RedirectView
from storyviewer.models import Story

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url="/stories/")),
    url(r'^stories/$', ListView.as_view(model=Story, queryset=Story.objects.all())),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
