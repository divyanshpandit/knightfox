
import tkinter as tk
import ctypes
from ctypes import windll

class AppWindow(tk.Tk):
    def __init__(self, on_toggle):
        super().__init__()
        self.title("KnightFox - Stealth Mode")
        self.geometry("700x550")
        
        # --- TRANSPARENCY ---
        # We keep this at 0.8 as per your KnightFox setup.
        self.attributes('-alpha', 0.8) 

        # --- PRIVACY SHIELD (The feature you requested) ---
        # This tells Windows to hide this specific window from screen capture/sharing.
        self.enable_privacy_shield()

        self.on_toggle = on_toggle
        self.recording = False

        self.chat = tk.Text(self, wrap="word", bg="white", fg="black")
        self.chat.pack(expand=True, fill="both", padx=10, pady=10)

        self.status = tk.Label(self, text="Ready", anchor="w")
        self.status.pack(fill="x", padx=10)

        # --- AUDIO SOURCE TOGGLE ---
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
            # Force window to render so we can get the correct Handle (HWND)
            self.update_idletasks()
            
            # Get the Window Handle
            hwnd = windll.user32.GetParent(self.winfo_id())
            
            # Constants for SetWindowDisplayAffinity
            # WDA_NONE = 0x00000000
            # WDA_MONITOR = 0x00000001 (Black box in capture)
            # WDA_EXCLUDEFROMCAPTURE = 0x00000011 (Invisible in capture - Windows 10 Ver 2004+)
            
            WDA_EXCLUDEFROMCAPTURE = 0x00000011
            
            # Apply the setting
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
        self.status.config(text=text)
