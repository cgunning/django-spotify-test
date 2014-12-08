from django.conf.urls import patterns, url

from spotify_app import views

urlpatterns = patterns('',
    # ex: /polls/5/
    url(r'^login/$', views.login, name='login'),
    url(r'^do_login/$', views.do_login, name='do_login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^search/$', views.search, name='search'),
    url(r'^play/(?P<track_id>spotify:track:[0-9a-zA-Z]+)/$', views.play, name='play'),
    url(r'^remove_from_queue/(?P<queue_id>\d+)$', views.remove_from_queue, name='remove_from_queue'),
    url(r'^playlist/$', views.playlist, name='playlist'),
    url(r'^play_next/$', views.play_next, name='play_next'),
    url(r'^play_prev/$', views.play_prev, name='play_prev'),
    url(r'^set_audio_output/(?P<output>\d)$', views.set_audio_output, name='set_audio_output'),
    url(r'^set_volume/$', views.set_volume, name='set_volume'),
)