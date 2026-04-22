import pygame
import numpy as np
import os

SR = 44100
_SND_DIR = "assets/sounds"


def _wav(name):
    return os.path.join(_SND_DIR, name)


def _make_stereo(arr):
    stereo = np.column_stack((arr, arr))
    return pygame.sndarray.make_sound(stereo)


def _syn_bell(freq=900, dur=0.55, vol=0.55):
    n = int(SR * dur)
    t = np.linspace(0, dur, n, endpoint=False)
    tone = (
        0.60 * np.sin(2*np.pi * freq       * t) * np.exp(-t * 5.0)
      + 0.25 * np.sin(2*np.pi * freq*2.76  * t) * np.exp(-t * 9.0)
      + 0.15 * np.sin(2*np.pi * freq*5.40  * t) * np.exp(-t * 14.0)
    )
    atk = int(0.002 * SR)
    env = np.ones(n)
    env[:atk] = np.linspace(0, 1, atk)
    out = np.clip(tone * env * vol, -1, 1)
    return (out * 32767).astype(np.int16)

def _syn_start_bell(vol=0.55):
    ding     = _syn_bell(freq=920, dur=0.55, vol=vol)
    gap_n    = int(0.18 * SR)   
    gap      = np.zeros(gap_n, dtype=np.int16)
    combined = np.concatenate([ding, gap, ding, gap, ding])
    return _make_stereo(combined)

def _syn_gong(freq=90, dur=2.0, vol=0.60):
    n = int(SR * dur)
    t = np.linspace(0, dur, n, endpoint=False)
    body = np.sin(2*np.pi * freq       * t) * np.exp(-t * 2.5)
    ring = np.sin(2*np.pi * freq*3.5   * t) * np.exp(-t * 4.0) * 0.4
    shim = np.sin(2*np.pi * freq*7.2   * t) * np.exp(-t * 6.0) * 0.2
    atk  = int(0.004 * SR)
    env  = np.ones(n); env[:atk] = np.linspace(0, 1, atk)
    out  = np.clip((body + ring + shim) * env * vol, -1, 1)
    return (out * 32767).astype(np.int16)

def _syn_end_gong(vol=0.60):
    strike   = _syn_gong(freq=90, dur=2.0, vol=vol)
    gap_n    = int(0.55 * SR)  
    gap      = np.zeros(gap_n, dtype=np.int16)
    strike2  = _syn_gong(freq=80, dur=2.0, vol=vol*0.80)
    combined = np.concatenate([strike, gap, strike2])
    return _make_stereo(combined)

def _syn_kick(vol=0.65):
    n = int(SR * 0.07)
    t = np.linspace(0, 0.07, n, endpoint=False)
    thud  = np.sin(2*np.pi*90  * t) * np.exp(-t*55)
    slap  = np.sin(2*np.pi*650 * t) * np.exp(-t*180)
    rng   = np.random.default_rng(3)
    click = rng.standard_normal(n) * np.exp(-t*400)
    out = np.clip((0.50*thud + 0.32*slap + 0.18*click)*vol, -1, 1)
    return _make_stereo((out*32767).astype(np.int16))

def _syn_goal():
    notes = [523, 659, 784, 1047]
    chunks = []
    for freq in notes:
        n = int(SR * 0.12)
        t = np.linspace(0, 0.12, n, endpoint=False)
        w = np.sin(2*np.pi*freq*t)
        chunks.append((w * np.linspace(1,0,n) * 0.45 * 32767).astype(np.int16))
    return _make_stereo(np.concatenate(chunks))


def _load_or(path, fallback_fn):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        try:
            return fallback_fn()
        except Exception:
            return None


class SoundManager:
    def __init__(self):
        self.start_sound   = None
        self.timeout_sound = None
        self.goal_sound    = None
        self.kick_sound    = None
        self._load_all()

    def _load_all(self):
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(frequency=SR, size=-16, channels=2, buffer=512)
            except Exception:
                return

        try:
            self.start_sound   = _syn_start_bell()
            self.timeout_sound = _syn_end_gong()
            self.goal_sound    = _syn_goal()
            self.kick_sound    = _load_or(_wav("kick.wav"), _syn_kick)
        except Exception:
            pass


    def play_start(self):
        if self.start_sound:
            self.start_sound.play()

    def play_timeout(self):
        if self.timeout_sound:
            self.timeout_sound.play()

    def play_goal(self):
        if self.goal_sound:
            self.goal_sound.play()

    def play_kick(self):
        if self.kick_sound:
            self.kick_sound.play()

    def play_menu(self):
        pass
