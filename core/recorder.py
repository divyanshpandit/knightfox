import soundcard as sc
import numpy as np
import threading
import time

class Recorder:
    def __init__(self):
        self.frames = []
        self.recording = False
        self.thread = None
        self.on_silence_callback = None
        self.silence_threshold = 0.01
        self.silence_limit = 3.0

        
        try:
            self.mic_source = sc.default_microphone()
            print(f"[Recorder] Mic found: {self.mic_source.name}")
        except:
            self.mic_source = None

        try:
            speaker = sc.default_speaker()
            self.sys_source = sc.get_microphone(id=str(speaker.name), include_loopback=True)
            print(f"[Recorder] System found: {speaker.name} (Loopback)")
        except:
            self.sys_source = None

    def start(self, mode="mic", on_silence_func=None):
        """
        mode: 'mic' or 'system'
        """
        if self.recording:
            return

        self.frames = []
        self.recording = True
        self.on_silence_callback = on_silence_func

        
        if mode == "system" and self.sys_source:
            current_mic = self.sys_source
            print("[Recorder] Using SYSTEM AUDIO")
        else:
            current_mic = self.mic_source
            print("[Recorder] Using MICROPHONE")

        def record():
            try:
                with current_mic.recorder(samplerate=48000) as rec:
                    last_sound_time = time.time()
                    
                    while self.recording:
                        data = rec.record(numframes=1024)
                        self.frames.append(data.copy())

                        # Silence Detection
                        volume = np.max(np.abs(data))
                        if volume > self.silence_threshold:
                            last_sound_time = time.time()
                        elif time.time() - last_sound_time > self.silence_limit:
                            print("[Recorder] Silence detected.")
                            self.recording = False
                            if self.on_silence_callback:
                                self.on_silence_callback()
                            break
            except Exception as e:
                print(f"[Recorder Error] {e}")
                self.recording = False

        self.thread = threading.Thread(target=record, daemon=True)
        self.thread.start()

    def stop(self):
        if not self.recording and not self.frames:
            return None

        self.recording = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)

        if len(self.frames) == 0:
            return None

        audio = np.concatenate(self.frames, axis=0)
        if audio.ndim > 1:
            audio = audio.mean(axis=1)

        return audio.astype("float32")