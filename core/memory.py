import json
import os

class Memory:
    def __init__(self):
        self.history = []
        # If you have a save file, this might be loading the bad data
        self.file_path = "memory.json" 
        self.load()

    def get(self):
        """
        Returns the history, but FILTERS out broken/empty messages first.
        This prevents the 'content argument must not be empty' crash.
        """
        clean_history = []
        for msg in self.history:
            # Check 1: Does it have 'parts'?
            # Check 2: Is the text inside 'parts' not empty?
            if "parts" in msg and msg["parts"] and msg["parts"][0].strip():
                clean_history.append(msg)
        
        return clean_history

    def update(self, user_text, ai_text):
        # Only save valid text
        if not user_text.strip() or not ai_text.strip():
            return

        self.history.append({"role": "user", "parts": [user_text]})
        self.history.append({"role": "model", "parts": [ai_text]})
        self.save()

    def save(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.history, f)
        except Exception as e:
            print(f"[Memory Error] Could not save: {e}")

    def load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    self.history = json.load(f)
            except:
                self.history = []