import speech_recognition as sr
import numpy as np

class SpeechToText:
    def __init__(self):
        print("[STT] Using Google Web Speech API (Online & Free)...")
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio_data, samplerate=48000):
        # 1. Convert numpy array (float32) to raw PCM audio (int16)
        # Google needs standard audio format, not numpy arrays
        audio_int16 = (audio_data * 32767).astype(np.int16)
        
        # 2. Create an AudioData object that the library understands
        audio_bytes = audio_int16.tobytes()
        audio_obj = sr.AudioData(audio_bytes, samplerate, 2) # 2 bytes width = 16-bit

        try:
            # 3. Send to Google (Free API)
            text = self.recognizer.recognize_google(audio_obj)
            return text
        except sr.UnknownValueError:
            return "" # Google didn't understand the audio
        except sr.RequestError:
            print("[STT] Internet Error")
            return ""