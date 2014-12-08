from __future__ import unicode_literals

from alsaaudio import Mixer

import sys
import threading
import subprocess

import spotify

class Player:
    def __init__(self):   
        self.logged_in = threading.Event()
        self.end_of_track = threading.Event()

        self.queue_playlist = []
        self.prev_playlist = []
        
        self.min_volume = 70
        
        config = spotify.Config()
        config.load_application_key_file(filename='/home/pi/django_projects/mysite/spotify_app/spotify_appkey.key')
        self.session = spotify.Session(config=config)
        
        self.loop = spotify.EventLoop(self.session)
        self.loop.start()
        
        self.current_track = None

        # Connect an audio sink
        self.audio = spotify.AlsaSink(self.session)
        self.mixer = Mixer('PCM', 0)
        
        self.session.on(spotify.SessionEvent.CONNECTION_STATE_UPDATED, self.on_connection_state_updated)
        self.session.on(spotify.SessionEvent.END_OF_TRACK, self.on_end_of_track)
        
    def login(self, username, password):
        self.session.login(username, password)
        self.logged_in.wait()
        self.player = self.session.player
    
    def logout(self):
        self.session.logout()
        
    def play(self, track_uri):
        track = self.session.get_track(track_uri).load()
        self.current_track = track
        self.player.load(track)
        self.player.play()
        
    def queue(self, track_uri):
        track = self.session.get_track(track_uri).load()
        self.queue_playlist.append(track)
        
    def pause(self):
        self.player.pause()
    
    def stop(self):
        self.current_track = None
        self.player.unload()
        
    def play_prev(self):
        if len(self.prev_playlist) == 0:
            self.play(self.current_track.link.uri)
        else:
            self.queue_playlist.insert(0, self.current_track)
            self.play(self.prev_playlist.pop(0).link.uri)
        
    def play_next(self):
        self.prev_playlist.insert(0, self.current_track)
        if len(self.queue_playlist) == 0:
            self.current_track = None
        else:
            self.play(self.queue_playlist.pop(0).link.uri);
    
    def set_audio_output(self, output):
        subprocess.call(["amixer", "cset", "numid=3", str(output)])
    
    def search(self, query):
        search = self.session.search(query);
        search.load()
        return search.tracks
    
    def get_playlist(self):
        return self.queue_playlist
        
    def is_playing(self):
        if self.current_track == None:
            return False
        else:
            return True
    
    def remove_from_queue(self, index):
        self.queue_playlist.pop(int(index))
    
    def set_volume(self, volume):
        if int(volume) == self.min_volume:
            volume = 0
        self.mixer.setvolume(int(volume))

    def get_volume(self):
        return self.mixer.getvolume()[0]
    
    def on_connection_state_updated(self, session):
        if session.connection.state is spotify.ConnectionState.LOGGED_IN:
            self.logged_in.set()
        else:
            self.logged_in.clear()

    def on_end_of_track(self, self2):
        self.play_next()