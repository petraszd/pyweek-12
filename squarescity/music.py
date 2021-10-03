from pyglet.media import Player, ManagedSoundPlayer
import pyglet


def play_background_music():
    try:
        player = Player()
        player.eos_action = Player.EOS_LOOP
        player.volume = 0.9
        player.queue(pyglet.resource.media('data/music/music.ogg'))
        player.play()
    except Exception:
        pass # do nothing


def play_shoot():
    _play_sound('data/shoot.ogg', volume=0.4)


def play_explode():
    _play_sound('data/explode.ogg')


def _play_sound(filename, volume=1.0):
    try:
        player = ManagedSoundPlayer()
        player.queue(pyglet.resource.media(filename))
        player.volume = volume
        player.play()
    except Exception:
        pass # Do nothing
