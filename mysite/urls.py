from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^spotify_app/', include('spotify_app.urls', namespace="spotify_app")),
    url(r'^admin/', include(admin.site.urls)),
)