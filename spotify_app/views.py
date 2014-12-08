from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from spotify_app.player import Player

p = Player();
current_search = []

def playlist(request):
    global p
    context = {'playlist': p.get_playlist()}
    return render(request, 'spotify_app/playlist.html', context)

current_track = None

def play(request, track_id):
    global p
    global current_search
    if p.is_playing():
        p.queue(track_id)
    else:
        p.play(track_id)
    
    context = {'tracks': current_search, 'playlist': p.get_playlist(), "current_volume": p.get_volume()}
    return render(request, 'spotify_app/search.html', context)
    
def remove_from_queue(request, queue_id):
    global p
    p.remove_from_queue(queue_id)
    context = {'tracks': current_search, 'playlist': p.get_playlist(), "current_volume": p.get_volume()}
    return render(request, 'spotify_app/search.html', context)
    
def play_prev(request):
    global p
    p.play_prev()
    context = {'tracks': current_search, 'playlist': p.get_playlist(), "current_volume": p.get_volume()}
    return render(request, 'spotify_app/search.html', context)
    
def play_next(request):
    global p
    p.play_next()
    context = {'tracks': current_search, 'playlist': p.get_playlist(), "current_volume": p.get_volume()}
    return render(request, 'spotify_app/search.html', context)

def set_audio_output(request, output):
    global p
    p.set_audio_output(output)
    context = {'tracks': current_search, 'playlist': p.get_playlist(), "current_volume": p.get_volume()}
    return render(request, 'spotify_app/search.html', context)
   
def set_volume(request):
    global p
    p.set_volume(request.POST['volume'])
    context = {'tracks': current_search, 'playlist': p.get_playlist(), "current_volume": p.get_volume()}
    return render(request, 'spotify_app/search.html', context)
    
def login(request):
    return render(request, 'spotify_app/login.html')
    
def do_login(request):
    global p
    p.login(request.POST['username'], request.POST['password'])
    tracks = []
    return render(request, 'spotify_app/search.html', tracks)
    
def logout(request):
    global p
    p.logout()
    return render(request, 'spotify_app/login.html')
    
def search(request):
    global p
    global current_search
    current_search = p.search(request.POST.get('query', 'björnstammen'))
    context = {'tracks': current_search, 'playlist': p.get_playlist(), "current_volume": p.get_volume()}
    return render(request, 'spotify_app/search.html', context)