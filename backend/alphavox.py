# AlphaVox module - main interface
"""
AlphaVox module providing voice synthesis and audio playback functionality.
"""

# Voice synthesis class
_voice_impl = None
try:
    from alphavox_ultimate_voice import alphavoxUltimateVoice
    _voice_impl = alphavoxUltimateVoice
except ImportError:
    pass

class AlphaVoxUltimateVoice:
    """AlphaVox voice synthesis interface"""
    def __init__(self):
        if _voice_impl:
            self._voice = _voice_impl()
        else:
            self._voice = None
            
    def speak(self, text: str) -> bool:
        """Speak the given text"""
        if self._voice:
            try:
                return self._voice.speak(text)
            except Exception:
                pass
        print(f"[AlphaVox]: {text}")
        return True

# Audio playback function
_playsound_func = None

try:
    from playsound3 import playsound as _ps3
    _playsound_func = _ps3
except ImportError:
    try:
        from playsound import playsound as _ps
        _playsound_func = _ps
    except ImportError:
        pass

def playsound(sound_file, block=True):
    """Play audio file"""
    if _playsound_func:
        try:
            return _playsound_func(sound_file, block)
        except Exception:
            pass
    print(f"[Audio]: Would play {sound_file}")
    return True

__all__ = ['AlphaVoxUltimateVoice', 'playsound']