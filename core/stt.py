import speech_recognition as sr
import numpy as np

class SpeechToText:
    def __init__(self):
        print("[STT] Using Google Web Speech API (Online & Free)...")
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio_data, samplerate=48000):
        
        
        audio_int16 = (audio_data * 32767).astype(np.int16)
        
        
        audio_bytes = audio_int16.tobytes()
        audio_obj = sr.AudioData(audio_bytes, samplerate, 2) 

        try:
            
            text = self.recognizer.recognize_google(audio_obj)
            return text
        except sr.UnknownValueError:
            return "" 
        except sr.RequestError:
            print("[STT] Internet Error")
            return ""
