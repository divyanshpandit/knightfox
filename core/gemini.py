'''import google.generativeai as genai

class GeminiAI:
    def __init__(self):
        self.model = None

    def configure(self, api_key):
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
            return True
        except Exception as e:
            print(f"Configuration Error: {e}")
            return False

    def ask_stream(self, text, history):
        if not self.model:
            yield "[System] Error: API Key not configured."
            return

        try:
            chat = self.model.start_chat(history=history)
            response = chat.send_message(text, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            print(f"[Gemini Error] {e}")
            yield f"I encountered an error: {e}"'''
import google.generativeai as genai

class GeminiAI:
    def __init__(self):
        self.model = None
        self.chat= None
    def init_model(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash-lite")
        self.chat = self.model.start_chat(history=[])
    '''def configure(self, api_key):
        try:
            # SAFETY: Remove any accidental spaces or quotes from the key
            clean_key = str(api_key).strip().replace('"', '').replace("'", "")
            
            genai.configure(api_key=clean_key)
            
            # Use the standard flash model (fast & cheap)
            self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
            return True
        except Exception as e:
            print(f"Configuration Error: {e}")
            return False'''

    '''def ask_stream(self, text, history):
        if not self.model:
            yield "[System] Error: API Key not configured."
            return

        try:
            chat = self.model.start_chat(history=history)
            response = chat.send_message(text, stream=True)
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            print(f"[Gemini Error] {e}")
            yield f"I encountered an error: {e}"'''
    def ask_stream(self, text, history):
        try:
            response = self.chat.send_message(text, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"[Gemini Error] {e}"

