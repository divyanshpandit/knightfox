import tkinter as tk
import ctypes
from ctypes import windll, c_long, sizeof
import keyboard

class AppWindow(tk.Tk):
    def __init__(self, on_toggle):
        super().__init__()
        self.title("KnightFox - Stealth Mode")
        self.geometry("700x550")
        
        self.active_alpha = 0.7
        self.stealth_alpha = 0.2
        self.panic_key = "ctrl+shift+z"
        self.click_through_key = "ctrl+shift+x"
        
        self.attributes('-topmost', True)

        self.attributes('-alpha', self.active_alpha) 

        try:
            self.attributes('-toolwindow', True)
        except Exception:
            pass

        self.enable_privacy_shield()

        try:
            keyboard.add_hotkey(self.panic_key, self.toggle_visibility)
            keyboard.add_hotkey(self.click_through_key, self.toggle_click_through_hotkey)
            print(f"[Stealth] Panic: {self.panic_key} | Click-Through: {self.click_through_key}")
        except Exception as e:
            print(f"[Stealth Error] Hotkey bind failed: {e}")

        self.on_toggle = on_toggle
        self.recording = False
        self.is_visible = True
        self.click_through_active = False

        self.chat = tk.Text(self, wrap="word", bg="white", fg="black", font=("Arial", 10))
        self.chat.pack(expand=True, fill="both", padx=10, pady=10)

        self.status = tk.Label(self, text="Ready", anchor="w")
        self.status.pack(fill="x", padx=10)

        self.controls_frame = tk.Frame(self)
        self.controls_frame.pack(pady=5)

        self.audio_mode = tk.StringVar(value="mic")
        tk.Radiobutton(self.controls_frame, text="🎤 Mic", variable=self.audio_mode, value="mic").pack(side="left", padx=5)
        tk.Radiobutton(self.controls_frame, text="💻 System", variable=self.audio_mode, value="system").pack(side="left", padx=5)
        
        self.chk_click_through_var = tk.BooleanVar(value=False)
        self.chk_click_through = tk.Checkbutton(
            self.controls_frame, 
            text="👻 Click-Through", 
            variable=self.chk_click_through_var,
            command=self.toggle_click_through_ui
        )
        self.chk_click_through.pack(side="left", padx=15)

        self.btn_toggle = tk.Button(
            self,
            text="🎙 Start Recording",
            height=2,
            width=30,
            command=self.toggle
        )
        self.btn_toggle.pack(pady=10)

    def enable_privacy_shield(self):
        try:
            WDA_EXCLUDEFROMCAPTURE = 17 
            
            self.update_idletasks()
            hwnd = windll.user32.GetParent(self.winfo_id())
            
            result = windll.user32.SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)
            
            if result == 0:
                pass
                
        except Exception as e:
            print(f"[Stealth Error] Could not set privacy shield: {e}")

    def toggle_visibility(self):
        if self.is_visible:
            self.withdraw()
            self.is_visible = False
        else:
            self.deiconify()
            self.attributes('-alpha', self.stealth_alpha if self.click_through_active else self.active_alpha)
            self.is_visible = True
            
            self.after(100, self.enable_privacy_shield)

    def set_click_through(self, enable):
        try:
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            WS_EX_TRANSPARENT = 0x00000020

            hwnd = windll.user32.GetParent(self.winfo_id())
            if sizeof(c_long) == 8:
                GetWindowLong = windll.user32.GetWindowLongPtrW
                SetWindowLong = windll.user32.SetWindowLongPtrW
            else:
                GetWindowLong = windll.user32.GetWindowLongW
                SetWindowLong = windll.user32.SetWindowLongW

            style = GetWindowLong(hwnd, GWL_EXSTYLE)

            if enable:
                new_style = style | WS_EX_LAYERED | WS_EX_TRANSPARENT
                self.attributes('-alpha', self.stealth_alpha) 
                self.status.config(text="👻 Click-Through ON (Press Ctrl+Shift+X to disable)", fg="red")
            else:
                new_style = style & ~WS_EX_TRANSPARENT
                self.attributes('-alpha', self.active_alpha)
                self.status.config(text="Ready", fg="black")

            SetWindowLong(hwnd, GWL_EXSTYLE, new_style)
            self.click_through_active = enable
            self.chk_click_through_var.set(enable) 
            
            self.after(10, self.enable_privacy_shield)
            
        except Exception as e:
            print(f"Click-Through Error: {e}")

    def toggle_click_through_ui(self):
        self.set_click_through(self.chk_click_through_var.get())

    def toggle_click_through_hotkey(self):
        new_state = not self.click_through_active
        self.after(0, lambda: self.set_click_through(new_state))

    def toggle(self):
        self.recording = not self.recording
        mode = self.audio_mode.get()
        self.on_toggle(self.recording, mode)

        if self.recording:
            self.btn_toggle.config(text="⏹ Stop & Ask AI", bg="#ffcccc")
            self.status.config(text=f"Recording ({mode.upper()})...")
            self.attributes('-alpha', 1.0)
            
            self.enable_privacy_shield()
        else:
            self.btn_toggle.config(text="🎙 Start Recording", bg="SystemButtonFace")
            self.status.config(text="Thinking…")
            if not self.click_through_active:
                self.attributes('-alpha', self.active_alpha)
            else:
                self.attributes('-alpha', self.stealth_alpha)

    def add_chat(self, user, ai):
        self.chat.insert("end", f"\nYou: {user}\nAI: {ai}\n")
        self.chat.see("end")

    def set_status(self, text):
        self.status.config(text=text)
