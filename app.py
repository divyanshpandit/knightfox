
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
from core.recorder import Recorder
from core.stt import SpeechToText
from core.gemini import GeminiAI
from core.memory import Memory
from ui.window import AppWindow

# --- Core components ---
recorder = Recorder()
stt = SpeechToText()
ai = GeminiAI()
memory = Memory()

def get_api_key():
    """
    Creates a hidden window to securely ask for the API Key.
    """
    root = tk.Tk()
    root.withdraw() # Hide the main window background
    
    key = simpledialog.askstring(
        title="KnightFox Security", 
        prompt="Please paste your Google Gemini API Key:\n(It will not be saved permanently)",
        parent=root,
        show='*' # Optional: masking the input if you prefer privacy while pasting
    )
    
    root.destroy()
    return key

def handle_toggle(is_recording: bool, mode: str = "mic"):
    if is_recording:
        def on_auto_stop():
            print("Auto-stopping...")
            window.btn_toggle.invoke()

        # PASS THE MODE TO RECORDER
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
                # 1. Transcribe (User -> Text)
                print("[1] Listening...")
                text = stt.transcribe(audio)

                if not text or not text.strip():
                    window.set_status("No speech detected")
                    return

                # Display User's Message immediately
                window.add_chat(text, "") 
                window.set_status("⚡ Gemini is typing...")

                # 2. STREAMING RESPONSE
                full_response = ""
                
                # We start the AI line with "AI: " so we can append to it
                window.chat.insert("end", "AI: ")
                
                # Loop through chunks as they arrive (Real-time)
                # Pass the history from memory
                for chunk in ai.ask_stream(text, memory.get()):
                    full_response += chunk
                    
                    # Update UI INSTANTLY
                    window.chat.insert("end", chunk)
                    window.chat.see("end") # Auto-scroll down

                # Add a newline after done
                window.chat.insert("end", "\n\n")

                # 3. Update Memory
                memory.update(text, full_response)
                window.set_status("Ready")

            except Exception as e:
                print(f"[ERROR] {e}")
                window.set_status("Error")
                window.add_chat("System", str(e))

        threading.Thread(target=process, daemon=True).start()

# --- MAIN EXECUTION START ---
if __name__ == "__main__":
    # 1. Ask for the API Key first
    user_key = get_api_key()

    if not user_key:
        print("No API Key provided. Exiting.")
    else:
        # 2. Configure the AI
        if ai.configure(user_key):
            # 3. If successful, Launch the Window
            window = AppWindow(handle_toggle)
            window.mainloop()
        else:
            print("Failed to configure Gemini. Check your key.")