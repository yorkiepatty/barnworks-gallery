"""Simple app module stub"""

class SimpleApp:
    def __init__(self):
        self.name = "AlphaVox Simple App"
    
    def run(self):
        return True

app = SimpleApp()

def get_app():
    return app

__all__ = ['SimpleApp', 'app', 'get_app']
