
import google.generativeai as genai

class GeminiAI:
    def __init__(self):
        # We do NOT set the key here anymore.
        self.model = None

    def configure(self, api_key):
        """
        Sets the API key and initializes the model.
        Called by app.py after the user enters their key.
        """
        try:
            genai.configure(api_key=api_key)
            # Initialize the model only after we have the key
            self.model = genai.GenerativeModel('gemini-2.0-flash-lite-001')
            return True
        except Exception as e:
            print(f"Configuration Error: {e}")
            return False

    def ask_stream(self, text, history):
        """
        Yields text chunk-by-chunk instead of waiting for the full answer.
        """
        if not self.model:
            yield "[System] Error: API Key not configured."
            return

        try:
            # Create a temporary chat session with history
            chat = self.model.start_chat(history=history)
            
            # Request streaming response
            response = chat.send_message(text, stream=True)
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            print(f"[Gemini Error] {e}")
            yield f"I encountered an error: {e}"
