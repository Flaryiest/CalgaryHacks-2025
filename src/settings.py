import json

class Settings:
    def __init__(self, dir="settings.json"):
        self.dir = dir
        with open(self.dir, 'r') as f:
            self.settings = json.load(f)
    
    def edit(self, settings):
        with open(self.dir, "w") as f:
            f.write(settings)