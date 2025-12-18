'''import tkinter as tk
import ctypes
from ctypes import windll

class AppWindow(tk.Tk):
    def __init__(self, on_toggle):
        super().__init__()
        self.title("KnightFox - Stealth Mode")
        self.geometry("700x550")
        
        
        
        self.attributes('-alpha', 0.8) 

        
        
        self.enable_privacy_shield()

        self.on_toggle = on_toggle
        self.recording = False

        self.chat = tk.Text(self, wrap="word", bg="white", fg="black")
        self.chat.pack(expand=True, fill="both", padx=10, pady=10)

        self.status = tk.Label(self, text="Ready", anchor="w")
        self.status.pack(fill="x", padx=10)

        
        self.audio_mode = tk.StringVar(value="mic")
        self.toggle_frame = tk.Frame(self)
        self.toggle_frame.pack(pady=5)

        tk.Radiobutton(self.toggle_frame, text="🎤 Mic", variable=self.audio_mode, value="mic").pack(side="left", padx=10)
        tk.Radiobutton(self.toggle_frame, text="💻 System Audio", variable=self.audio_mode, value="system").pack(side="left", padx=10)

        self.btn_toggle = tk.Button(
            self,
            text="🎙 Start Recording",
            height=2,
            command=self.toggle
        )
        self.btn_toggle.pack(pady=10)

    def enable_privacy_shield(self):
        """
        Uses Windows API SetWindowDisplayAffinity to exclude this window 
        from screen capture (OBS, Discord, Teams, etc.).
        """
        try:
            
            self.update_idletasks()
            
            
            hwnd = windll.user32.GetParent(self.winfo_id())
            
            
            
            
            
WDA_EXCLUDEFROMCAPTURE = 0x00000011
            
            
            windll.user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
            print("Privacy Shield: ENABLED (Window is hidden from screen recorders)")
            
        except Exception as e:
            print(f"Privacy Shield Error: {e}")

    def toggle(self):
        self.recording = not self.recording
        mode = self.audio_mode.get()
        self.on_toggle(self.recording, mode)

        if self.recording:
            self.btn_toggle.config(text="⏹ Stop & Ask AI")
            self.status.config(text=f"Recording ({mode.upper()})...")
        else:
            self.btn_toggle.config(text="🎙 Start Recording")
            self.status.config(text="Thinking…")

    def add_chat(self, user, ai):
        self.chat.insert("end", f"\nYou: {user}\nAI: {ai}\n")
        self.chat.see("end")

    def set_status(self, text):
        self.status.config(text=text)'''
import tkinter as tk
import ctypes
from ctypes import windll

class AppWindow(tk.Tk):
    def __init__(self, on_toggle):
        super().__init__()
        self.title("KnightFox - Stealth Mode")
        self.geometry("700x550")
        
        
        self.attributes('-alpha', 0.8) 


        try:
            self.attributes('-toolwindow', True)
        except Exception:
            
            pass


        self.enable_privacy_shield()

        self.on_toggle = on_toggle
        self.recording = False

        # Chat Area
        self.chat = tk.Text(self, wrap="word", bg="white", fg="black")
        self.chat.pack(expand=True, fill="both", padx=10, pady=10)

        # Status Bar
        self.status = tk.Label(self, text="Ready", anchor="w")
        self.status.pack(fill="x", padx=10)

        # Audio Toggle Frame
        self.audio_mode = tk.StringVar(value="mic")
        self.toggle_frame = tk.Frame(self)
        self.toggle_frame.pack(pady=5)

        tk.Radiobutton(self.toggle_frame, text="🎤 Mic", variable=self.audio_mode, value="mic").pack(side="left", padx=10)
        tk.Radiobutton(self.toggle_frame, text="💻 System Audio", variable=self.audio_mode, value="system").pack(side="left", padx=10)

        self.btn_toggle = tk.Button(
            self,
            text="🎙 Start Recording",
            height=2,
            command=self.toggle
        )
        self.btn_toggle.pack(pady=10)

    def enable_privacy_shield(self):
        """Hides window from OBS, Discord, Teams, Zoom screen shares."""
        try:
            
            WDA_EXCLUDEFROMCAPTURE = 17 
            
            
            self.update_idletasks()
            hwnd = windll.user32.GetParent(self.winfo_id())
            
           
            windll.user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
            print("[Privacy] Screen Share Shield: ENABLED")
        except Exception as e:
            print(f"[Privacy Error] {e}")

    def toggle(self):
        self.recording = not self.recording
        mode = self.audio_mode.get()
        self.on_toggle(self.recording, mode)

        if self.recording:
            self.btn_toggle.config(text="⏹ Stop & Ask AI")
            self.status.config(text=f"Recording ({mode.upper()})...")
        else:
            self.btn_toggle.config(text="🎙 Start Recording")
            self.status.config(text="Thinking…")

    def add_chat(self, user, ai):
        self.chat.insert("end", f"\nYou: {user}\nAI: {ai}\n")
        self.chat.see("end")

    def set_status(self, text):
        self.status.config(text=text)