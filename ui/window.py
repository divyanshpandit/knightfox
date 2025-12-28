'''import tkinter as tk
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
        self.status.config(text=text)'''



import tkinter as tk
import ctypes
from ctypes import windll, c_long, sizeof
import keyboard

# --- THEME PALETTE ---
COLOR_BG = "#121212"        # Main Background
COLOR_HEADER = "#1f1f1f"    # Header Background
COLOR_CHAT_BG = "#1e1e1e"   # Chat Background
COLOR_TEXT_MAIN = "#e0e0e0" # Bright Text
COLOR_TEXT_DIM = "#808080"  # Dim Text
COLOR_ACCENT = "#00d9f7"    # Cyan Neon Accent
COLOR_RECORD = "#ff3333"    # Bright Red

class AppWindow(tk.Tk):
    def __init__(self, on_toggle):
        super().__init__()
        self.title("KnightFox")
        self.geometry("700x600")
        self.configure(bg=COLOR_ACCENT) 
        
        # Borderless Window
        self.overrideredirect(True) 
        
        # --- CONFIGURATION ---
        self.active_alpha = 0.8
        self.stealth_alpha = 0.2
        
        # --- HOTKEYS ---
        self.panic_key = "ctrl+shift+z"
        self.click_through_key = "ctrl+shift+x"
        self.record_key = "Tab" 
        
        self.attributes('-topmost', True)
        self.attributes('-alpha', self.active_alpha) 
        self.enable_privacy_shield()

        # --- BINDING ---
        try:
            keyboard.add_hotkey(self.panic_key, self.toggle_visibility)
            keyboard.add_hotkey(self.click_through_key, self.toggle_click_through_hotkey)
            keyboard.add_hotkey(self.record_key, self.toggle_recording_hotkey)
            print(f"[Keys] Panic: {self.panic_key} | Rec: {self.record_key} | Ghost: {self.click_through_key}")
        except Exception as e:
            print(f"[Key Error] {e}")

        self.on_toggle = on_toggle
        self.recording = False
        self.is_visible = True
        self.click_through_active = False
        self.offset_x = 0
        self.offset_y = 0

        self._build_ui()

    def _build_ui(self):
        # Main Container
        self.main_frame = tk.Frame(self, bg=COLOR_BG)
        self.main_frame.pack(expand=True, fill="both", padx=1, pady=1) 

        # Header
        self.header = tk.Frame(self.main_frame, bg=COLOR_HEADER, height=35)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)
        self.header.bind("<Button-1>", self.start_move)
        self.header.bind("<B1-Motion>", self.do_move)

        lbl_title = tk.Label(self.header, text=" KNIGHTFOX // STEALTH", bg=COLOR_HEADER, fg=COLOR_ACCENT, font=("Consolas", 10, "bold"))
        lbl_title.pack(side="left", padx=10)
        lbl_title.bind("<Button-1>", self.start_move)

        btn_close = tk.Button(self.header, text="✕", bg=COLOR_HEADER, fg="white", bd=0, font=("Arial", 12),
            activebackground="#ff3333", activeforeground="white", command=self.quit_app, width=4)
        btn_close.pack(side="right")

        # Chat Area
        self.chat_frame = tk.Frame(self.main_frame, bg=COLOR_BG, padx=10, pady=5)
        self.chat_frame.pack(expand=True, fill="both")

        self.chat = tk.Text(self.chat_frame, wrap="word", bg=COLOR_CHAT_BG, fg=COLOR_TEXT_MAIN, 
            font=("Consolas", 11), bd=0, highlightthickness=0, padx=15, pady=15, insertbackground=COLOR_ACCENT)
        self.chat.pack(expand=True, fill="both")

        # Controls
        self.controls = tk.Frame(self.main_frame, bg=COLOR_BG, pady=10)
        self.controls.pack(fill="x", side="bottom")

        self.status = tk.Label(self.controls, text="SYSTEM READY", bg=COLOR_BG, fg=COLOR_TEXT_DIM, font=("Consolas", 9), anchor="w")
        self.status.pack(fill="x", padx=20, pady=(0, 10))

        self.options_row = tk.Frame(self.controls, bg=COLOR_BG)
        self.options_row.pack(pady=5)

        self.audio_mode = tk.StringVar(value="mic")
        self._create_radio("MIC", "mic")
        self._create_radio("SYS", "system")

        self.chk_click_through_var = tk.BooleanVar(value=False)
        self.chk_click_through = tk.Checkbutton(self.options_row, text="GHOST", variable=self.chk_click_through_var,
            command=self.toggle_click_through_ui, bg=COLOR_BG, fg=COLOR_TEXT_MAIN, selectcolor=COLOR_BG,
            activebackground=COLOR_BG, activeforeground=COLOR_ACCENT, font=("Consolas", 10))
        self.chk_click_through.pack(side="left", padx=15)

        self.btn_toggle = tk.Button(self.controls, text="[ INITIALIZE RECORDING ]", command=self.toggle,
            bg=COLOR_ACCENT, fg="#000000", font=("Consolas", 11, "bold"), relief="flat", bd=0,
            padx=20, pady=10, activebackground="white", activeforeground="black")
        self.btn_toggle.pack(pady=10)

    def _create_radio(self, text, val):
        rb = tk.Radiobutton(self.options_row, text=text, variable=self.audio_mode, value=val,
            bg=COLOR_BG, fg=COLOR_TEXT_MAIN, selectcolor=COLOR_BG, activebackground=COLOR_BG,
            activeforeground=COLOR_ACCENT, font=("Consolas", 10))
        rb.pack(side="left", padx=10)

    # --- LOGIC ---
    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def do_move(self, event):
        x = self.winfo_x() + event.x - self.offset_x
        y = self.winfo_y() + event.y - self.offset_y
        self.geometry(f"+{x}+{y}")

    def quit_app(self):
        self.destroy()

    def enable_privacy_shield(self):
        try:
            hwnd = windll.user32.GetParent(self.winfo_id())
            windll.user32.SetWindowDisplayAffinity(hwnd, 17)
        except: pass

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
            hwnd = windll.user32.GetParent(self.winfo_id())
            GetWindowLong = windll.user32.GetWindowLongPtrW if sizeof(c_long) == 8 else windll.user32.GetWindowLongW
            SetWindowLong = windll.user32.SetWindowLongPtrW if sizeof(c_long) == 8 else windll.user32.SetWindowLongW
            
            style = GetWindowLong(hwnd, -20)
            if enable:
                new_style = style | 0x00080000 | 0x00000020
                self.attributes('-alpha', self.stealth_alpha) 
                self.status.config(text=">> GHOST MODE ACTIVE", fg=COLOR_RECORD)
                self.btn_toggle.config(state="disabled", bg="#444444")
            else:
                new_style = style & ~0x00000020
                self.attributes('-alpha', self.active_alpha)
                self.status.config(text="SYSTEM READY", fg=COLOR_TEXT_DIM)
                self.btn_toggle.config(state="normal", bg=COLOR_ACCENT)

            SetWindowLong(hwnd, -20, new_style)
            self.click_through_active = enable
            self.chk_click_through_var.set(enable) 
            self.after(10, self.enable_privacy_shield)
        except Exception as e: print(e)

    def toggle_click_through_ui(self):
        self.set_click_through(self.chk_click_through_var.get())

    def toggle_click_through_hotkey(self):
        self.after(0, lambda: self.set_click_through(not self.click_through_active))

    def toggle_recording_hotkey(self):
        self.after(0, self.toggle)

    def toggle(self):
        self.recording = not self.recording
        mode = self.audio_mode.get()
        self.on_toggle(self.recording, mode)

        if self.recording:
            self.btn_toggle.config(text="[ STOP RECORDING ]", bg=COLOR_RECORD, fg="white")
            self.status.config(text=f">> RECORDING DATA ({mode.upper()})...", fg=COLOR_RECORD)
            self.attributes('-alpha', 1.0)
            self.enable_privacy_shield()
        else:
            self.btn_toggle.config(text="[ INITIALIZE RECORDING ]", bg=COLOR_ACCENT, fg="black")
            self.status.config(text="PROCESSING COMPLETE", fg=COLOR_TEXT_DIM)
            if not self.click_through_active: self.attributes('-alpha', self.active_alpha)

    def add_chat(self, user, ai):
        self.chat.mark_set("msg_start", "end-1c")
        self.chat.insert("end", f"\nUSER >> {user}\n", "user_tag")
        self.chat.insert("end", f"FOX  >> {ai}\n", "ai_tag")
        self.chat.insert("end", " " + "-"*50 + " \n", "separator")
        self.chat.tag_config("user_tag", foreground=COLOR_ACCENT)
        self.chat.tag_config("ai_tag", foreground=COLOR_TEXT_MAIN)
        self.chat.tag_config("separator", foreground="#333333")
        self.chat.see("msg_start")

    def set_status(self, text):
        self.status.config(text=text)