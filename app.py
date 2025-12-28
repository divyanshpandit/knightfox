'''import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
from core.recorder import Recorder
from core.stt import SpeechToText
from core.gemini import GeminiAI
from core.memory import Memory
from ui.window import AppWindow

recorder = Recorder()
stt = SpeechToText()
ai = GeminiAI()
memory = Memory()

def get_api_key():                                                                                                                              
    root = tk.Tk()
    root.withdraw()
    
    key = simpledialog.askstring(
        title="KnightFox Security", 
        prompt="Please paste your Google Gemini API Key:\n(It will not be saved permanently)",
        parent=root,
        show='*'
    )
    
    root.destroy()
    if key:
        # The Critical Fix: Remove spaces/quotes
        print(key)
        return key.strip().replace('"', '').replace("'", "")
    return None

def handle_toggle(is_recording: bool, mode: str = "mic"):
    if is_recording:
        def on_auto_stop():
            print("Auto-stopping...")
            window.btn_toggle.invoke()

        recorder.start(mode=mode, on_silence_func=on_auto_stop)
        
        window.set_status(f"🎙 Recording ({mode})…")

    else:
        audio = recorder.stop()
        
        if audio is None and not recorder.frames:
            window.set_status("Ready")
            return

        window.set_status("🧠 Thinking…")

        def process():
            try:
                print("[1] Listening...")
                text = stt.transcribe(audio)

                if not text or not text.strip():
                    window.set_status("No speech detected")
                    return

                window.add_chat(text, "") 
                window.set_status("⚡ Gemini is typing...")

                full_response = ""
                
                window.chat.insert("end", "AI: ")
                
                for chunk in ai.ask_stream(text, memory.get()):
                    full_response += chunk
                    
                    window.chat.insert("end", chunk)
                    window.chat.see("end")

                window.chat.insert("end", "\n\n")

                memory.update(text, full_response)
                window.set_status("Ready")

            except Exception as e:
                print(f"[ERROR] {e}")
                window.set_status("Error")
                window.add_chat("System", str(e))

        threading.Thread(target=process, daemon=True).start()

if __name__ == "__main__":
    user_key = get_api_key()

    if not user_key:
        print("No API Key provided. Exiting.")
    else:
        if ai.configure(user_key):
            window = AppWindow(handle_toggle)
            window.mainloop()
        else:
            print("Failed to configure Gemini. Check your key.")'''
import threading
import tkinter as tk
from tkinter import simpledialog
import sys

from core.recorder import Recorder
from core.stt import SpeechToText
from core.gemini import GeminiAI
from core.memory import Memory
from ui.window import AppWindow
import google.generativeai as genai

recorder = Recorder()
stt = SpeechToText()
ai = GeminiAI()
memory = Memory()
def init_gemini(api_key):
    genai.configure(api_key=api_key)

def get_api_key():
    root = tk.Tk()
    root.withdraw()
    
    key = simpledialog.askstring(
        title="KnightFox Security", 
        prompt="Please paste your Google Gemini API Key:\n(Ctrl+V to paste)",
        parent=root,
        show='*'
    )
    
    root.destroy()
    
    if key:
        
        print(key)
        return key.strip().replace('"', '').replace("'", "")
    return None

def handle_toggle(is_recording: bool, mode: str = "mic"):
    if is_recording:
        def on_auto_stop():
            window.btn_toggle.invoke()

        recorder.start(mode=mode, on_silence_func=on_auto_stop)
        window.set_status(f"🎙 Recording ({mode})…")

    else:
        audio = recorder.stop()
        if audio is None and not recorder.frames:
            window.set_status("Ready")
            return

        window.set_status("🧠 Thinking…")

        def process():
            try:
                print("[1] Listening...")
                text = stt.transcribe(audio)

                if not text or not text.strip():
                    window.set_status("No speech detected")
                    return

                window.add_chat(text, "") 
                window.set_status("⚡ Gemini is typing...")

                full_response = ""
                window.chat.insert("end", "AI: ", "ai_tag")
                
                for chunk in ai.ask_stream(text, memory.get()):
                    full_response += chunk
                    window.chat.insert("end", chunk)

                window.chat.insert("end", "\n\n")
                memory.update(text, full_response)
                window.set_status("Ready")

            except Exception as e:
                print(f"[ERROR] {e}")
                window.set_status("Error")
                window.add_chat("System", str(e))

        threading.Thread(target=process, daemon=True).start()

if __name__ == "__main__":
    api_key = get_api_key()
    init_gemini(api_key)   
    ai.init_model()

    if not api_key:
        print("No API Key provided. Exiting.")
        sys.exit()
    else:
        
        window = AppWindow(handle_toggle)
        window.mainloop()
        '''else:
            print("Failed to configure Gemini. Check your key.")   '''     