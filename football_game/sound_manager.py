import pygame
import numpy as np


def _generate_tone(frequency, duration_ms, volume=0.4, wave="sine"):
    """Generate a simple synthetic sound and return a pygame.Sound object."""
    sample_rate = 44100
    num_samples = int(sample_rate * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, num_samples, endpoint=False)

    if wave == "sine":
        wave_data = np.sin(2 * np.pi * frequency * t)
    elif wave == "square":
        wave_data = np.sign(np.sin(2 * np.pi * frequency * t))
    else:
        wave_data = np.sin(2 * np.pi * frequency * t)

    # Fade out to avoid clicking
    fade = np.linspace(1.0, 0.0, num_samples)
    wave_data = wave_data * fade * volume

    # Convert to 16-bit stereo
    wave_int = (wave_data * 32767).astype(np.int16)
    stereo = np.column_stack((wave_int, wave_int))
    sound = pygame.sndarray.make_sound(stereo)
    return sound


class SoundManager:
    """Manages sound effects used in the game.

    Attributes:
        kick_sound  -- sound played when a player kicks the ball
        goal_sound  -- sound played when a goal is scored
        timeout_sound -- sound played when match time runs out
    """

    def __init__(self):
        self.kick_sound = None
        self.goal_sound = None
        self.timeout_sound = None
        self.load_sounds()

    def load_sounds(self):
        """Load or generate all game sounds."""
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            except Exception:
                return

        try:
            # Try loading from files first (assets/sounds/*.wav)
            self.kick_sound = pygame.mixer.Sound("assets/sounds/kick.wav")
            self.goal_sound = pygame.mixer.Sound("assets/sounds/goal.wav")
            self.timeout_sound = pygame.mixer.Sound("assets/sounds/timeout.wav")
        except Exception:
            # Fall back to synthetic tones
            try:
                self.kick_sound = _generate_tone(300, 80, volume=0.35, wave="square")
                self.goal_sound = self._generate_goal_fanfare()
                self.timeout_sound = _generate_tone(220, 600, volume=0.5, wave="sine")
            except Exception:
                # If numpy is unavailable or mixer fails, silently skip
                pass

    def _generate_goal_fanfare(self):
        """Generate a short ascending fanfare for goals."""
        sample_rate = 44100
        notes = [523, 659, 784, 1047]  # C5 E5 G5 C6
        duration_each = 120  # ms
        all_samples = []

        for freq in notes:
            num_samples = int(sample_rate * duration_each / 1000)
            t = np.linspace(0, duration_each / 1000, num_samples, endpoint=False)
            wave = np.sin(2 * np.pi * freq * t)
            fade = np.linspace(1.0, 0.0, num_samples)
            wave = wave * fade * 0.45
            all_samples.append((wave * 32767).astype(np.int16))

        combined = np.concatenate(all_samples)
        stereo = np.column_stack((combined, combined))
        return pygame.sndarray.make_sound(stereo)

    def play_kick(self):
        """Play the kick sound effect."""
        if self.kick_sound:
            self.kick_sound.play()

    def play_goal(self):
        """Play the goal sound effect."""
        if self.goal_sound:
            self.goal_sound.play()

    def play_timeout(self):
        """Play the timeout / full-time whistle sound."""
        if self.timeout_sound:
            self.timeout_sound.play()

    def play_menu(self):
        """Play a menu navigation sound (placeholder)."""
        pass
